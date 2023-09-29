Version 0.x
===========

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