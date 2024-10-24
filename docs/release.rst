Version x.y.z
=============

2.0.1 (2024-05-23)
--------------------
- bug #12 (python 3.10)
- enh #4 (Unification of parameters in to_xarray, to_scipp and to_dataframe)
- add CI processus (Github Workflow)
- pre-commit integration

2.0.0 (2024-05-06)
--------------------
- extension to multidimensional interfaces
    - Xarray interface (`to_xarray` method, `from_xarray` function)
    - scipp interface (`to_scipp` method, `from_scipp` function)
- ENH #4 #5 #7 #8 #9

1.1.1 (2024-01-05)
--------------------
- bug setup

1.1.0 (2024-01-04)
--------------------
- add `to_analysis` function to use `TAB-analysis`module
- add `check_relation` function to use `TAB-dataset.check_relation` method
- add pandas accessor for `to_analysis` and `check_relation`


1.0.2 (2023-11-23)
--------------------
- move `decode_ntv_tab` method in `ntv_util` module ('json_ntv')

1.0.1 (2023-10-10)
--------------------
- add User Guide
- add `equals` method (check names and cat.categories dtype)
- add pandas accessor for `to_json`, `equals` and `as_def_type`
- BUG #3: categorical with a single value

1.0.0 (2023-09-30)
--------------------
- add Table Schema interface
- Table Schema type / format supported:
    - numerical: integer/default, boolean/default, number/default
    - json: object/default, array/default, string/default, string/uri, string/email
    - datation: datetime/default, date/default, time/default, yearmonth/default, year/default
    - location: geopint/array, geojson/default
- additional type / format supported (Table Schema extension):
    - numerical: number/floatxx, integer/intxx, integer/uintxx
    - json: string/file, object/null, object/object
    - datation: date/day, date/wday, date/yday, date/week, time/hour, time/minute, time/second
    - location: geojson/geometry, geojson/polygon, geojson/line
- correspondance between `NTVtype` and `type`/ `format` in `ntv_table.ini`

0.1.1 RC1 (2023-09-19)
--------------------
- bug setup

0.1.0 RC1 (2023-09-19)
--------------------
- First release candidate
- functions `to_json`, `read_json` and `as_def_type` available
- specific methods available in the class `DataFrameConnec` and `SeriesConnec`
- correspondance between `NTVtype` and `dtype` in `ntv_pandas.ini`
- dtype supported:
    - timedelta64[ns], datetime64[ns]
    - string
    - Floatxx, UIntxx, Intxx, boolean
    - categorical
- NTVtype supported:
    - duration, period
    - datetime, date, time, dat
    - month, year, day, wday, yday, week, hour, minute, second
    - json, string, number, boolean, array, object, null
    - floatxx, uintxx, intxx
    - uri, email, file
    - point, line, polygon, geometry, geojson
    - multipoint, multiline, multipolygon, box, codeolc
    - row, field, tab, ntv
