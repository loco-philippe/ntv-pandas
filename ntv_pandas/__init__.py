# -*- coding: utf-8 -*-
"""
***NTV-pandas Package***

Created on Sept 2023

@author: philippe@loco-labs.io

This package contains the following classes and functions:

- `ntv-pandas.ntv_pandas.pandas_ntv_connector` :
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.DataFrameConnec`
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.SeriesConnec`
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.to_json`
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.read_json`
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.as_def_type`


# NTV-pandas : A semantic, compact and reversible JSON-pandas converter

# Why a NTV-pandas converter ?

pandas provide JSON converter but three limitations are present:
- the JSON-pandas converter take into account a few data types,
- the JSON-pandas converter is not always reversible (round type)
- external dtype (e.g. TableSchema type) are not included

# main features

The NTV-pandas converter uses the [semantic NTV format]
(https://loco-philippe.github.io/ES/JSON%20semantic%20format%20(JSON-NTV).htm) 
to include a large set of data types in a JSON representation.
The converter integrates:
- all the pandas `dtype` and the data-type associated to a JSON representation,
- an always reversible conversion,
- a full compatibility with TableSchema specification

# example

In the example below, a DataFrame with several data types is converted to JSON.

The DataFrame resulting from this JSON is identical to the initial DataFrame (reversibility).

With the existing JSON interface, this conversion is not possible.

*data example*
```python
In [1]: from shapely.geometry import Point
        from datetime import date
        import pandas as pd
        import ntv_pandas as npd

In [2]: data = {'index':           [100, 200, 300, 400, 500, 600],
                'dates::date':     pd.Series([date(1964,1,1), date(1985,2,5), date(2022,1,21), date(1964,1,1), date(1985,2,5), date(2022,1,21)]),
                'value':           [10, 10, 20, 20, 30, 30],
                'value32':         pd.Series([12, 12, 22, 22, 32, 32], dtype='int32'),
                'res':             [10, 20, 30, 10, 20, 30],
                'coord::point':    pd.Series([Point(1,2), Point(3,4), Point(5,6), Point(7,8), Point(3,4), Point(5,6)]),
                'names':           pd.Series(['john', 'eric', 'judith', 'mila', 'hector', 'maria'], dtype='string'),
                'unique':          True }

In [3]: df = pd.DataFrame(data).set_index('index')

In [4]: df
Out[4]:
              dates::date  value  value32  res coord::point   names  unique
        index
        100    1964-01-01     10       12   10  POINT (1 2)    john    True
        200    1985-02-05     10       12   20  POINT (3 4)    eric    True
        300    2022-01-21     20       22   30  POINT (5 6)  judith    True
        400    1964-01-01     20       22   10  POINT (7 8)    mila    True
        500    1985-02-05     30       32   20  POINT (3 4)  hector    True
        600    2022-01-21     30       32   30  POINT (5 6)   maria    True
```

*JSON representation*

```python
In [5]: df_to_json = npd.to_json(df)
        pprint(df_to_json, compact=True, width=120)
Out[5]:
        {':tab': {'coord::point': [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0], [3.0, 4.0], [5.0, 6.0]],
                  'dates::date': ['1964-01-01', '1985-02-05', '2022-01-21', '1964-01-01', '1985-02-05', '2022-01-21'],
                  'index': [100, 200, 300, 400, 500, 600],
                  'names::string': ['john', 'eric', 'judith', 'mila', 'hector', 'maria'],
                  'res': [10, 20, 30, 10, 20, 30],
                  'unique': [True, True, True, True, True, True],
                  'value': [10, 10, 20, 20, 30, 30],
                  'value32::int32': [12, 12, 22, 22, 32, 32]}}
```

*Reversibility*

```python
In [5]: df_from_json = npd.read_json(df_to_json)
        print('df created from JSON is equal to initial df ? ', df_from_json.equals(df))

Out[5]: df created from JSON is equal to initial df ?  True
```


"""
from ntv_pandas.pandas_ntv_connector import DataFrameConnec, SeriesConnec, read_json, to_json, as_def_type


#print('package :', __package__)