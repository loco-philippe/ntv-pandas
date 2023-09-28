### *NTV-pandas : A semantic, compact and reversible JSON-pandas converter*    

<img src="https://loco-philippe.github.io/ES/ntv_pandas.png" alt="ntv-pandas" align="middle" style="height:80px;">

# Why a NTV-pandas converter ?
pandas provide JSON converter but three limitations are present:
- the JSON-pandas converter take into account a few data types,
- the JSON-pandas converter is not always reversible (conversion round trip)
- external dtype (e.g. TableSchema type) are not included

# main features
The NTV-pandas converter uses the [semantic NTV format](https://loco-philippe.github.io/ES/JSON%20semantic%20format%20(JSON-NTV).htm) 
to include a large set of data types in a JSON representation.    
    
The converter integrates:
- all the pandas `dtype` and the data-type associated to a JSON representation,
- an always reversible conversion,
- a full compatibility with TableSchema specification

NTV-pandas was developped originally in the [json-NTV project](https://github.com/loco-philippe/NTV)

# example

In the example below, a DataFrame with several data types is converted to JSON (with NTV format and with Table Schema format).

The DataFrame resulting from those JSON conversions are identical to the initial DataFrame (reversibility).

With the existing JSON interface, those conversions are not possible.

*data example*
```python
In [1]: from shapely.geometry import Point
        from datetime import date
        import pandas as pd
        import ntv_pandas as npd

In [2]: data = {'index':        [100, 200, 300, 400, 500],
                'dates::date':  [date(1964,1,1), date(1985,2,5), date(2022,1,21), date(1964,1,1), date(1985,2,5)],
                'value':        [10, 10, 20, 20, 30],
                'value32':      [12, 12, 22, 22, 32], dtype='int32'),
                'res':          [10, 20, 30, 10, 20],
                'coord::point': [Point(1,2), Point(3,4), Point(5,6), Point(7,8), Point(3,4)],
                'names':        pd.Series(['john', 'eric', 'judith', 'mila', 'hector'], dtype='string'),
                'unique':       True }

In [3]: df = pd.DataFrame(data).set_index('index')
        df.index.name = None

In [4]: df
Out[4]:       dates::date  value  value32  res coord::point   names  unique
        100    1964-01-01     10       12   10  POINT (1 2)    john    True
        200    1985-02-05     10       12   20  POINT (3 4)    eric    True
        300    2022-01-21     20       22   30  POINT (5 6)  judith    True
        400    1964-01-01     20       22   10  POINT (7 8)    mila    True
        500    1985-02-05     30       32   20  POINT (3 4)  hector    True
```

*JSON-NTV representation*

```python
In [5]: df_to_json = npd.to_json(df)
        pprint(df_to_json, compact=True, width=120)
Out[5]: {':tab': {'index': [100, 200, 300, 400, 500],
                  'dates::date': ['1964-01-01', '1985-02-05', '2022-01-21', '1964-01-01', '1985-02-05'],
                  'value': [10, 10, 20, 20, 30],
                  'value32::int32': [12, 12, 22, 22, 32],
                  'res': [10, 20, 30, 10, 20],
                  'coord::point': [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0], [3.0, 4.0]],
                  'names::string': ['john', 'eric', 'judith', 'mila', 'hector'],
                  'unique': True}}
```

*Reversibility*

```python
In [6]: df_from_json = npd.read_json(df_to_json)
        print('df created from JSON is equal to initial df ? ', df_from_json.equals(df))
Out[6]: df created from JSON is equal to initial df ?  True
```

*Table Schema representation*

```python
In [7]: df_to_table = npd.to_json(df, table=True)
        pprint(df_to_table['data'][0], sort_dicts=False)
Out[7]: {'index': 100,
         'dates': '1964-01-01',
         'value': 10,
         'value32': 12,
         'res': 10,
         'coord': [1.0, 2.0],
         'names': 'john',
         'unique': True}

In [8]: pprint(df_to_table['schema'], sort_dicts=False)
Out[8]: {'fields': [{'name': 'index', 'type': 'integer'},
                    {'name': 'dates', 'type': 'date'},
                    {'name': 'value', 'type': 'integer'},
                    {'name': 'value32', 'type': 'integer', 'format': 'int32'},
                    {'name': 'res', 'type': 'integer'},
                    {'name': 'coord', 'type': 'geopoint', 'format': 'array'},
                    {'name': 'names', 'type': 'string'},
                    {'name': 'unique', 'type': 'boolean'}],
         'primaryKey': ['index'],
         'pandas_version': '1.4.0'}
```

*Reversibility*

```python
In [9]: print(npd.read_json(df_to_table).equals(df))
Out[9]: True
```
# installation and documentation

`ntv-pandas` itself is a pure Python package maintained on [ntv-pandas github repository](https://github.com/loco-philippe/ntv-pandas).     
     
It can be installed with `pip`. 

    pip install ntv-pandas

dependency:
- `json_ntv`: support the NTV format,
- `shapely`: for the location data,
- `pandas` 

[Documentation](https://github.com/loco-philippe/ntv-pandas/tree/main/docs/README.md)

# roadmap

- **type extension** : interval dtype and sparse format not yet included
- **table schema** : add type / format (`geojson`/`topojson`, `geopoint`/`default`, `geopoint`/`object`, `duration`/`default, `string`/`binary`, `string`/`uuid`), 
- **null JSON data** : strategy to define
- **multidimensional** : extension of the NTV format for multidimensional data (e.g. Xarray)   
- **pandas type** : support for Series or DataFrame which include pandas data
- **data consistency** : controls between NTVtype and NTVvalue
