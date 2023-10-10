# installation

## ntv_pandas package

The `ntv_pandas` package includes

- `pandas_ntv_connector` module
  - functions `read_json` and `to_json` to convert JSON data and pandas entities
  - function `as_def_type` to convert a Series or DataFrame with default `dtype` and `equals` to extend pandas `equals` method
  - child classes of `NTV.json_ntv.ntv.NtvConnector` abstract class:
    - `DataFrameConnec`: 'tab'   connector
    - `SeriesConnec`:    'field' connector
  - an utility class with static methods : `PdUtil`
- configuration files:
  - `ntv_pandas.ini` (correspondence between ntv_type and pandas dtype)
  - `ntv_table.ini` (correspondence between ntv_type and Table Schema types)

## Installation

`ntv_pandas` itself is a pure Python package. maintained on [ntv-pandas github repository](https://github.com/loco-philippe/ntv-pandas).

It can be installed with `pip`.

    pip install ntv_pandas

dependency:

- `json_ntv`: support the NTV format,
- `shapely`: for the location data,
- `pandas`
