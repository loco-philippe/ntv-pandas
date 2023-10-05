# installation

## ntv_pandas package
The `ntv_pandas` package includes 
- `pandas_ntv_connector` module 
    - functions `read_json` and `to_json` to convert JSON data and pandas entities
    - child classes of `NTV.json_ntv.ntv.NtvConnector` abstract class:
        - `DataFrameConnec`: 'tab'   connector
        - `SeriesConnec`:    'field' connector
    - an utility class with static methods : `PdUtil`    
- configuration files:
    - `ntv_pandas.ini` (correspondence between ntv_type and pandas dtype)
    - `ntv_table.ini` (correspondence between ntv_type and Table Schema types)

## Installation
`ntv_pandas` itself is a pure Python package. It can be installed with pip 

    pip install ntv_pandas
    
