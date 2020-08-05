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

import opentimelineio as otio
import pytest

from otio_cookelensmetadata import adapter


def test_record_type():
    header_type = "rt.header.lens.shading"
    header_record_type = adapter.RecordType.from_string(header_type)
    assert header_record_type.root == "rt"
    assert header_record_type.raw_category == "header"
    assert header_record_type.identifier == ["lens", "shading"]

    temporal_type = "rt.temporal.lens.gyro.raw"
    temporal_record_type = adapter.RecordType.from_string(temporal_type)
    assert temporal_record_type.root == "rt"
    assert temporal_record_type.raw_category == "temporal"
    assert temporal_record_type.identifier == ["lens", "gyro", "raw"]

    bogus_type = "rt.bogus.lens.whoknows.derived"
    bogus_record_type = adapter.RecordType.from_string(bogus_type)
    assert bogus_record_type.root == "rt"
    assert bogus_record_type.raw_category == "bogus"
    assert bogus_record_type.identifier == ["lens", "whoknows", "derived"]


def test_invalid_record_type():
    with pytest.raises(ValueError):
        adapter.RecordType.from_string("")


def test_record_type_to_string():
    rt = adapter.RecordType(raw_category="header", identifier=["one", "two"])
    assert str(rt) == "rt.header.one.two"


def test_category():
    rt = adapter.RecordType(raw_category="header", identifier=["one", "two"])
    assert rt.category is adapter.RecordType.Category.HEADER

    bogus_rt = adapter.RecordType(raw_category="bogus", identifier=["one", "two"])
    assert bogus_rt.category is adapter.RecordType.Category.UNKNOWN

    rt = adapter.RecordType()
    rt.category = adapter.RecordType.Category.TEMPORAL
    assert rt.category is adapter.RecordType.Category.TEMPORAL
    assert rt.raw_category == "temporal"

    rt.raw_category = "bogus"
    assert rt.category is adapter.RecordType.Category.UNKNOWN


@pytest.mark.parametrize(
    "is_dropframe,expected",
    [(False, "13:30:09:09"), (True, "13;30;09;09")],
)
def test_decode_tc(is_dropframe, expected):
    tc_dict = {
        "hh": 13,
        "mm": 30,
        "ss": 9,
        "ff": 9,
    }
    tc_string = adapter._decode_timecode(tc_dict, is_dropframe)

    assert tc_string == expected


def test_from_filepath(sample_lmd_path):
    marker_bin = adapter.read_from_file(sample_lmd_path)
    assert isinstance(marker_bin, otio.schema.SerializableCollection)


def test_from_file_data(sample_lmd_data):
    marker_bin = adapter.read_from_string(sample_lmd_data)
    assert isinstance(marker_bin, otio.schema.SerializableCollection)
