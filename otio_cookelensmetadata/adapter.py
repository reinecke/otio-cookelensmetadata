# Copyright 2020 Netflix, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, List, Mapping

import opentimelineio as otio
import yaml

# Imports the most efficient loader available
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


# The namespace key for OTIO metadata dictionaries
META_NAMESPACE = "LMF"

# Constants for special document keys
DROP_FRAME_KEY = "DropFrame"
FRAME_RATE_KEY = "FrameRate"
RECORD_TYPE_KEY = "RecordType"
TIMECODE_KEY = "Timecode"


class CookeLensMetadataError(otio.exceptions.OTIOError):
    """Base Exception type for this adapter"""


class MissingFieldError(CookeLensMetadataError):
    """
    Raised when a necessary field listed as required in the spec is misisng.
    """


@dataclass
class RecordType:
    class Category(Enum):
        HEADER = "header"
        TEMPORAL = "temporal"
        UNKNOWN = "unknown"

    root: str = "rt"
    raw_category: str = "unknown"
    identifier: List[str] = field(default_factory=list)

    def __str__(self):
        return ".".join([self.root, self.raw_category] + self.identifier)

    @property
    def category(self) -> Category:
        try:
            return self.Category(self.raw_category)
        except ValueError:
            return self.Category.UNKNOWN

    @property
    def is_kinematic(self) -> bool:
         kinematic_strings = ["magnetometer", "accelerometer", "gyro"]
         return any(substring in str(self) for substring in kinematic_strings)

    @category.setter
    def category(self, new_category: Category):
        self.raw_category = new_category.value

    @classmethod
    def from_string(cls, record_type: str):
        if not record_type:
            raise ValueError("Unparsable RecordType: {}".format(record_type))

        components = record_type.split(".")
        root = components[0]
        if len(components) > 1:
            category = components[1]
        if len(components) > 2:
            identifier = components[2:]

        return cls(root, category, identifier)


def _decode_timecode(
    tc_dict: Mapping[str, int], is_dropframe=False
) -> otio.opentime.RationalTime:
    """
    Decodes the timecode dict from yaml and returns a RationalTime.
    """
    delim = ";" if is_dropframe else ":"
    tc_elems = (tc_dict["hh"], tc_dict["mm"],  tc_dict["ss"],  tc_dict["ff"])
    tc_string = delim.join("{:02d}".format(elem) for elem in tc_elems)

    return tc_string


def _normalize_rate( in_rate: float 
) -> float:
    """
    Normalizes a frame rate float to one of the standard rates
    """
    return round(in_rate * 1001)/1001


def _read_from_documents(
    documents: Iterable[Mapping],
    create_clip=False,
    omit_kinematic=False
) -> otio.schema.SerializableCollection:

    if create_clip:
        clip = otio.schema.Clip(name="LMF Data")
        container = clip.markers
        lmf_global_md = clip.metadata.setdefault(META_NAMESPACE, {})
    else:
        container = otio.schema.SerializableCollection(name="LMF Data")
        lmf_global_md = container.metadata.setdefault(META_NAMESPACE, {})

    # Cache holding markers for a given timecode
    tc_to_marker_cache = {}

    min_time = None
    max_time = None
    tc_rate = None
    tc_is_dropframe = False
    for document in documents:
        md_skip_keys = set()
        try:
            record_type = RecordType.from_string(document[RECORD_TYPE_KEY])
            md_skip_keys.add(RECORD_TYPE_KEY)
        except KeyError:
            # In the LMF Records portion of the spec, it says documenta without
            # RecordType are disregarded for LMF processing.
            continue

        # If the omit_kinematic flag is set to True, skip any record type
        # containing kinematic data.
        if omit_kinematic and record_type.is_kinematic:
            continue

        # Handle pulling top-level metata for certain contexts
        if record_type.identifier == ["recorder", "info"]:
            tc_rate = document.get(FRAME_RATE_KEY)
            tc_rate = _normalize_rate( tc_rate )
            tc_is_dropframe = document.get(DROP_FRAME_KEY, False)

        category = record_type.category
        if category is RecordType.Category.HEADER:
            dest_metadata = lmf_global_md
        elif category is RecordType.Category.TEMPORAL:
            try:
                timecode_string = _decode_timecode(
                    document[TIMECODE_KEY], tc_is_dropframe
                )
                timecode_time = otio.opentime.from_timecode(
                    timecode_string, tc_rate
                )
                if max_time is None:
                    min_time = timecode_time
                    max_time = timecode_time
                else:
                    min_time = min(min_time, timecode_time)
                    max_time = max(max_time, timecode_time)
                md_skip_keys.add(TIMECODE_KEY)
            except KeyError:
                raise MissingFieldError(
                    "{} required for temporal record: {}".format(
                        TIMECODE_KEY, document
                    )
                )

            # Try to add metadata to existing markers
            try:
                marker = tc_to_marker_cache[timecode_string]
            except KeyError:
                marker = otio.schema.Marker(
                    marked_range=otio.opentime.TimeRange(
                        start_time=timecode_time
                    )
                )
                container.append(marker)
                tc_to_marker_cache[timecode_string] = marker

            dest_metadata = marker.metadata.setdefault(META_NAMESPACE, {})
        else:
            # Don't touch the records with unsupported categories, leave them
            # unharmed in an unsupported top-level dict
            unsupported_metadata = lmf_global_md.setdefault("unsupported", [])
            unsupported_metadata.append(document)
            continue

        # Generate the deeper metadata dict from the identifier elements
        for elem in record_type.identifier:
            dest_metadata = dest_metadata.setdefault(elem, {})

        # Copy the metadata over
        for md_key, value in document.items():
            if md_key in md_skip_keys:
                continue

            # Convert dates to strings for otio
            if isinstance(value, datetime.date):
                dest_metadata[md_key] = value.isoformat()
                continue

            dest_metadata[md_key] = value

    # Populate the clip time
    if create_clip and max_time is not None:
        end_time = max_time + otio.opentime.RationalTime(1, tc_rate)
        time_range = otio.opentime.TimeRange(min_time, (end_time - min_time))
        clip.source_range = time_range

        # Return a single-clip timeline
        return otio.schema.Timeline(
            tracks=[otio.schema.Track(children=[clip])]
        )

    return container


def read_from_string(input_str: str, create_clip=False, omit_kinematic=False, **kwargs):
    """
    Adapter entrypoint. By default, the adapter returns a
    :class:`SerializableCollection` of :class:`Marker` instances where the
    global metadata is placed in the collection's metadata dict and the
    contained markers have the time-sampled metadata.
    If ``create_clip`` is set ``True``, the adapter will
    generate a "dummy" clip, attach markers to that, and return a timeline
    containing the clip.
    If ``omit_kinematic`` is set ``True``, the adapter will skip
    all accelerometer, magnetometer, and gyro data in the incoming clip.
    """
    documents = yaml.load_all(input_str, Loader=Loader)

    return _read_from_documents(documents, create_clip, omit_kinematic)


def read_from_file(filepath: str, **adapter_argument_map):
    """
    Adapter entrypoint. By default, the adapter returns a
    :class:`SerializableCollection` of :class:`Marker` instances where the
    global metadata is placed in the collection's metadata dict and the
    contained markers have the time-sampled metadata.
    If ``create_clip`` is set ``True``, the adapter will
    generate a "dummy" clip, attach markers to that, and return a timeline
    containing the clip.
    If ``omit_kinematic`` is set ``True``, the adapter will skip
    all accelerometer, magnetometer, and gyro data in the incoming clip.
    """
    # The YAML loader adapts to string inputs and file inputs. Pass the opened
    # file through and let it work
    with open(filepath) as metadata_file:
        return read_from_string(metadata_file, **adapter_argument_map)
