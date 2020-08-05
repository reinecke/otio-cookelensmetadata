# otio-cookelensmetadata - OTIO Adapter for Cooke /i Lens Metadata

[Cooke Optics](https://www.cookeoptics.com/) has created a
[draft specification](https://bitbucket.org/cookeoptics/cookelensmetadata/)
for lens metadata. This OpenTimelineIO adapter implements parsing these
and representing the metadata in otio.

This code is currently shared as a proof of concept and is not yet meant for any
mainstream use cases - other than getting excited about cool workflows!

## Quickstart

If you'd like to try out the adapter in a development environment, you can do
the following:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -e .
$ pip install pyside2  # OPTIONAL: Only if you want to use otioview
```

You can now use LMF `.yml` files natively in OpenTimelineIO. For example,
`otiocat -i my-LMF-test-file.yml -o my-LMF-marker-set.otio` will generate an
otio file with a `SerializableObject` as the top-level object containing
markers with the LMF record metadata.

If you'd like to use `otioview`, set the adapter flag `create_clip` to `True`,
this attaches the markers to a clip for easier viewing in `otioview`. An example
of this might look like:

`otioview -a create_clip=True my-LMF-test-file.yml`


## Developing

To develop, follow the quickstart above to set up a virtualenv with dependencies
installed and linked to your local repo.

To run the tests you'll want to first get the full content of
[lens-data-2020052713471590587226.yml](https://bitbucket.org/cookeoptics/cookelensmetadata/src/master/SampleFiles/lens-data-2020052713471590587226.yml)
and put it in `tests/sample_data/lens-data-2020052713471590587226.yml`.

I like to use curl:

```
$ curl https://bitbucket.org/cookeoptics/cookelensmetadata/raw/426174755ae456b8788
518e8b64b59b5db80ceb1/SampleFiles/lens-data-2020052713471590587226.yml > tests/sample_data/lens-data-2020052713471590587226.yml
```

Then install the test requirements in your environment:

```
$ pip install -r tests/requirements.txt
```

Then you can run `pytest` from the root dir to get the unittest results.

## Sample

The following LMF document set:

```yaml
---
RecordType: rt.header.recorder.info
Manufacturer: Ambient Recording GmbH
Model: MasterLockitPlus II
SerialNumber: MLIIxxx3
RecordDate: 2020-05-27
FrameRate: 24.0
DropFrame: false
---
RecordType: rt.header.lens.info
SerialNumber: "7065.0102"
Owner: COOKE DEMO
LensType: prime
MinFocalLength: 65.0
MaxFocalLength: 65.0
TransmissionFactor: 0.93
FirmwareVersion: "7.34"
Manufacturer: Cooke Optics Lt
Model: S7i-65
AnamorphicSqueeze: 1.0
iVersion: 3
---
RecordType: rt.header.lens.shading
LensType: spherical
alpha_1: 0.12581336498260499
alpha_2: 0.01226633507758379
alpha_3: -0.000753768952563405
beta_1: 0.5748927593231201
beta_2: 0.2656184136867523
mu_1: 0.6340188980102539
mu_2: 0.07323184609413147
mu_3: -0.06928706169128418
nu_1: 0.5157180428504944
nu_2: 0.019469689577817918
nu_3: -0.002893560566008091
sigma_1: ~
sigma_2: ~
---
RecordType: rt.header.lens.distortion
LensType: spherical
s_min: 500.0
a_nom: 47.0
f:
  - 65.14214324951172
  - 1.7906161546707154
  - 0.18333962559700013
  - 0.6837693452835083
c_x:
  - 0.0
  - 0.019257964566349984
  - -0.036516740918159488
  - 0.016662470996379854
c_y:
  - 0.0
  - -0.002460891380906105
  - -0.061148565262556079
  - 0.03879305347800255
K1:
  - 0.003968206234276295
  - 0.006302871275693178
  - -0.001324182259850204
  - 0.002760479226708412
K2:
  - -0.0022727150935679676
  - 0.0034023532643914224
  - 0.002749079605564475
  - 0.0000818250045995228
K3:
  - -0.00406430009752512
  - -0.0016328172059729696
  - -0.0008932801429182291
  - -0.001089384313672781
P1:
  - 0.00013794230471830815
  - -0.00005021776814828627
  - 0.00013637077063322067
  - -0.00005989224518998526
P2:
  - 0.000037747104215668517
  - 0.00000174504884853377
  - -0.00013667589519172907
  - 0.0001262991427211091
S1:
  - 0.8696203827857971
  - 0.8237185478210449
  - -1.94357168674469
  - 1.8002805709838868
S2:
  - -0.9447554349899292
  - -0.6812136173248291
  - 1.1339746713638306
  - -1.0275139808654786
---
RecordType: rt.header.lens.cal.accelerometer
Row_1:
  - -0.000551785109564662
  - 0.0002258910972159356
  - 0.000005715729002986336
  - -0.19677266478538514
Row_2:
  - 0.00022618577349931002
  - 0.0005531031638383865
  - 0.000007387312962237047
  - -0.014095289632678032
Row_3:
  - 0.000006813808795413934
  - -0.00000945038664212916
  - 0.0005974594969302416
  - 0.05205082148313522
---
RecordType: rt.header.lens.cal.gyro
Row_1:
  - -0.0002905404835473746
  - 0.00012045353651046753
  - 0.000008586434887547512
  - 4.4281682487490317e-11
  - -1.1357535571743238e-11
  - 2.774990306986247e-12
  - 0.013803975656628609
Row_2:
  - 0.00012031001097057015
  - 0.0002898980746977031
  - 0.00000718242108632694
  - -1.8452236266730538e-11
  - -3.607880660894125e-11
  - 1.526548505659253e-11
  - 0.03938187658786774
Row_3:
  - -0.000004768163762491895
  - -0.000001431039095223241
  - 0.00030790059827268124
  - -1.1955400558427699e-10
  - -8.378429894317918e-11
  - -4.1398087215205326e-12
  - -0.0214050505310297
---
RecordType: rt.header.lens.cal.magnetometer
Row_1:
  - 1.3834202228224513e-8
  - 5.231559185858714e-9
  - 0.0
  - 0.0
Row_2:
  - -5.231559185858714e-9
  - 1.3834202228224513e-8
  - 0.0
  - 0.0
Row_3:
  - 0.0
  - 0.0
  - 1.479034761331377e-8
  - 0.0
```

Becomes this OTIO metadata dictionary on the top-level `SerializableCollection`:

```json
{
  "LMF": {
    "lens": {
      "cal": {
        "accelerometer": {
          "Row_1": [
            -0.000551785109564662,
            0.0002258910972159356,
            5.715729002986336e-06,
            -0.19677266478538513
          ],
          "Row_2": [
            0.00022618577349931002,
            0.0005531031638383865,
            7.387312962237047e-06,
            -0.014095289632678032
          ],
          "Row_3": [
            6.813808795413934e-06,
            -9.45038664212916e-06,
            0.0005974594969302416,
            0.05205082148313522
          ]
        },
        "gyro": {
          "Row_1": [
            -0.0002905404835473746,
            0.00012045353651046753,
            8.586434887547512e-06,
            4.4281682487490315e-11,
            -1.1357535571743238e-11,
            2.774990306986247e-12,
            0.013803975656628609
          ],
          "Row_2": [
            0.00012031001097057015,
            0.0002898980746977031,
            7.18242108632694e-06,
            -1.8452236266730537e-11,
            -3.607880660894125e-11,
            1.526548505659253e-11,
            0.03938187658786774
          ],
          "Row_3": [
            -4.768163762491895e-06,
            -1.431039095223241e-06,
            0.00030790059827268124,
            -1.1955400558427698e-10,
            -8.378429894317918e-11,
            -4.1398087215205326e-12,
            -0.0214050505310297
          ]
        },
        "magnetometer": {
          "Row_1": [
            1.3834202228224513e-08,
            5.231559185858714e-09,
            0,
            0
          ],
          "Row_2": [
            -5.231559185858714e-09,
            1.3834202228224513e-08,
            0,
            0
          ],
          "Row_3": [
            0,
            0,
            1.479034761331377e-08,
            0
          ]
        }
      },
      "distortion": {
        "K1": [
          0.003968206234276295,
          0.006302871275693178,
          -0.001324182259850204,
          0.002760479226708412
        ],
        "K2": [
          -0.0022727150935679674,
          0.0034023532643914223,
          0.002749079605564475,
          8.18250045995228e-05
        ],
        "K3": [
          -0.00406430009752512,
          -0.0016328172059729695,
          -0.0008932801429182291,
          -0.001089384313672781
        ],
        "LensType": "spherical",
        "P1": [
          0.00013794230471830815,
          -5.021776814828627e-05,
          0.00013637077063322067,
          -5.989224518998526e-05
        ],
        "P2": [
          3.7747104215668514e-05,
          1.74504884853377e-06,
          -0.00013667589519172907,
          0.0001262991427211091
        ],
        "S1": [
          0.8696203827857971,
          0.8237185478210449,
          -1.94357168674469,
          1.8002805709838867
        ],
        "S2": [
          -0.9447554349899292,
          -0.6812136173248291,
          1.1339746713638306,
          -1.0275139808654785
        ],
        "a_nom": 47,
        "c_x": [
          0,
          0.019257964566349983,
          -0.036516740918159485,
          0.016662470996379852
        ],
        "c_y": [
          0,
          -0.002460891380906105,
          -0.061148565262556076,
          0.03879305347800255
        ],
        "f": [
          65.14214324951172,
          1.7906161546707153,
          0.18333962559700012,
          0.6837693452835083
        ],
        "s_min": 500
      },
      "info": {
        "AnamorphicSqueeze": 1,
        "FirmwareVersion": "7.34",
        "LensType": "prime",
        "Manufacturer": "Cooke Optics Lt",
        "MaxFocalLength": 65,
        "MinFocalLength": 65,
        "Model": "S7i-65",
        "Owner": "COOKE DEMO",
        "SerialNumber": "7065.0102",
        "TransmissionFactor": 0.93,
        "iVersion": 3
      },
      "shading": {
        "LensType": "spherical",
        "alpha_1": 0.12581336498260498,
        "alpha_2": 0.01226633507758379,
        "alpha_3": -0.000753768952563405,
        "beta_1": 0.5748927593231201,
        "beta_2": 0.2656184136867523,
        "mu_1": 0.6340188980102539,
        "mu_2": 0.07323184609413147,
        "mu_3": -0.06928706169128418,
        "nu_1": 0.5157180428504944,
        "nu_2": 0.019469689577817917,
        "nu_3": -0.002893560566008091,
        "sigma_1": null,
        "sigma_2": null
      }
    },
    "recorder": {
      "info": {
        "DropFrame": false,
        "FrameRate": 24,
        "Manufacturer": "Ambient Recording GmbH",
        "Model": "MasterLockitPlus II",
        "RecordDate": "2020-05-27",
        "SerialNumber": "MLIIxxx3"
      }
    }
  }
}
```

Note that the documents were all combined so rather than having to seek through
a set of documents to find which one contains the desired metadata field, you
can directly access what you're looking for.

## How it works

The cooke lens metadata format is broken into LMF records. Each one has has an
associated `RecordType`. An example might be: `rt.header.lens.info`. From a
high-level perspective they can be broken into two major groups:

1. Header
2. Temporal

The `header` records apply globally to the file, while the `temporal` ones exist
at specific sample times. The adapter will attach `header` record information to
the top-level `SerializableCollection` (essentially a bin), and `temporal` records
will be added to `Markers` placed in that bin.

On read, the `Timecode` value is used for the `marked_range` of the OTIO marker
and records that share a timecode are combined into the same marker.

On both `header` and `temporal` records the fields are prevented from colliding
by using the `RecordType` to namespace the metadata. So, for example,
`rt.header.lens.shading` and `rt.header.lens.distortion` can be combined into a
deep dictionary structure like:

```
{
  "lens": {
    "shading": {
      ... shading record data here ...
    },
    "distortion": {
      ... distortion record data here ...
    }
  }
}
```
