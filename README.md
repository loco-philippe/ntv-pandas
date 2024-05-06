### *NTV-pandas : A tabular analyzer and a semantic, compact and reversible converter*

<img src="https://loco-philippe.github.io/ES/ntv_pandas.png" alt="ntv-pandas" align="middle" style="height:80px;">

For more information, see the [user guide](https://loco-philippe.github.io/ntv-pandas/docs/user_guide.html) or the [github repository](https://github.com/loco-philippe/ntv-pandas).

NTV-pandas is referenced in the [pandas ecosystem](https://pandas.pydata.org/community/ecosystem.html).

# Why a NTV-pandas converter ?

pandas provide IO converters but limitations are present:

- the multidimensional structure is not taken into account,
- the converters are not always reversible (conversion round trip),
- the converters take into account few data types,
- external data types (e.g. TableSchema types) are not included.

pandas does not have a tool for analyzing tabular structures and detecting integrity errors

## main features

The converter integrates:

- interfaces with Xarray, scipp, JSON,
- all the pandas `dtype` and the data-type associated to a JSON representation,
- an always reversible conversion,
- an identification of tabular and multidimensional structure,
- a full compatibility with [Table Schema specification](http://dataprotocols.org/json-table-schema/#field-types-and-formats).

The NTV-pandas converter uses the [semantic NTV format](https://loco-philippe.github.io/ES/JSON%20semantic%20format%20(JSON-NTV).htm)
to include a large set of data types in a JSON representation.

The NTV-pandas analyzer uses the [TAB-analysis](https://github.com/loco-philippe/tab-analysis/blob/main/README.md) tool to analyze and measure the relationships between Fields in DataFrame and the [TAB-dataset](https://github.com/loco-philippe/tab-dataset/blob/main/README.md) to identify integrity errors ([example](https://github.com/loco-philippe/ntv-pandas/tree/main/example#readme)).

The multidimensional converter uses the [NTV-numpy](https://github.com/loco-philippe/ntv-numpy/blob/main/README.md) multidimensional format and interfaces.

NTV-pandas was developped originally in the [NTV project](https://github.com/loco-philippe/NTV)

## multidimensional converter example

In the example below, a Dataframe is converted to Xarray and scipp.

The DataFrame resulting from these conversions are identical to the initial DataFrame (reversibility).

```python
In [1]: import pandas as pd
        import ntv_pandas as npd

In [2]: fruits = {'plants':      ['fruit', 'fruit', 'fruit', 'fruit', 'vegetable', 'vegetable', 'vegetable', 'vegetable'],
                  'plts':        ['fr', 'fr', 'fr', 'fr', 've', 've', 've', 've'], 
                  'quantity':    ['1 kg', '10 kg', '1 kg', '10 kg', '1 kg', '10 kg', '1 kg', '10 kg'],
                  'product':     ['apple', 'apple', 'orange', 'orange', 'peppers', 'peppers', 'carrot', 'carrot'],
                  'price':       [1, 10, 2, 20, 1.5, 15, 1.5, 20],
                  'price level': ['low', 'low', 'high', 'high', 'low', 'low', 'high', 'high'],
                  'group':       ['fruit 1', 'fruit 10', 'fruit 1', 'veget', 'veget', 'veget', 'veget', 'veget'],
                  'id':          [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
                  'supplier':    ["sup1", "sup1", "sup1", "sup2", "sup2", "sup2", "sup2", "sup1"],
                  'location':    ["fr", "gb", "es", "ch", "gb", "fr", "es", "ch"],
                  'valid':       ["ok", "ok", "ok", "ok", "ok", "ok", "ok", "ok"]} 
        df_fruits = pd.DataFrame(fruits)
        df_fruits.npd.analysis(distr=True).partitions()   # return the list of partitions (a partition is a list of dimensions)
Out[2]: 
        [['plants', 'quantity', 'price level'],
         ['quantity', 'price level', 'supplier'],
         ['plants', 'location'],
         ['quantity', 'product'],
         ['supplier', 'location'],
         ['id']]

In [3]: kwargs = {'dims':['product', 'quantity'], 'datagroup': False, 'ntv_type': False, 'json_name': False}
        xd_fruits = df_fruits.npd.to_xarray(**kwargs)
        xd_fruits
Out[3]: 
        <xarray.Dataset> Size: 976B
        Dimensions:      (product: 4, quantity: 2)
        Coordinates:
        * product      (product) <U7 112B 'apple' 'carrot' 'orange' 'peppers'
        * quantity     (quantity) <U5 40B '1 kg' '10 kg'
        plants       (product) <U9 144B 'fruit' 'vegetable' 'fruit' 'vegetable'
        plts         (product) <U2 32B 'fr' 've' 'fr' 've'
        price level  (product) <U4 64B 'low' 'high' 'high' 'low'
        valid        <U2 8B 'ok'
        Data variables:
        group        (product, quantity) <U8 256B 'fruit 1' 'fruit 10' ... 'veget'
        id           (product, quantity) int64 64B 1001 1002 1007 ... 1004 1005 1006
        location     (product, quantity) <U2 64B 'fr' 'gb' 'es' ... 'ch' 'gb' 'fr'
        price        (product, quantity) float64 64B 1.0 10.0 1.5 ... 20.0 1.5 15.0
        supplier     (product, quantity) <U4 128B 'sup1' 'sup1' ... 'sup2' 'sup2'

In [4]: sc_fruits = df_fruits.npd.to_scipp(**kwargs)
        sc_fruits
Out[4]: 
        <scipp.Dataset>
        Dimensions: Sizes[product:4, quantity:2, ]
        Coordinates:
        * plants                     string  [dimensionless]  (product)  ["fruit", "vegetable", "fruit", "vegetable"]
        * plts                       string  [dimensionless]  (product)  ["fr", "ve", "fr", "ve"]
        * price level                string  [dimensionless]  (product)  ["low", "high", "high", "low"]
        * product                    string  [dimensionless]  (product)  ["apple", "carrot", "orange", "peppers"]
        * quantity                   string  [dimensionless]  (quantity) ["1 kg", "10 kg"]
        * valid                      string  [dimensionless]  ()  "ok"
        Data:
          group                      string  [dimensionless]  (product, quantity)  ["fruit 1", "fruit 10", ..., "veget", "veget"]
          id                          int64  [dimensionless]  (product, quantity)  [1001, 1002, ..., 1005, 1006]
          location                   string  [dimensionless]  (product, quantity)  ["fr", "gb", ..., "gb", "fr"]
          price                     float64  [dimensionless]  (product, quantity)  [1, 10, ..., 1.5, 15]
          supplier                   string  [dimensionless]  (product, quantity)  ["sup1", "sup1", ..., "sup2", "sup2"]       
```

Reversibility:

```python
In [5]: df_fruits_xd = npd.from_xarray(xd_fruits, **kwargs)
        df_fruits_xd_sort = df_fruits_xd.reset_index()[list(df_fruits.columns)].sort_values(list(df_fruits.columns)).reset_index(drop=True)
        df_fruits_sort = df_fruits.sort_values(list(df_fruits.columns)).reset_index(drop=True)
        df_fruits_xd_sort.equals(df_fruits_sort)
Out[5]: 
        True

In [6]: df_fruits_sc = npd.from_scipp(sc_fruits, **kwargs)
        df_fruits_sc_sort = df_fruits_sc.reset_index()[list(df_fruits.columns)].sort_values(list(df_fruits.columns)).reset_index(drop=True)
        df_fruits_sort = df_fruits.sort_values(list(df_fruits.columns)).reset_index(drop=True)
        df_fruits_sc_sort.equals(df_fruits_sort)
Out[6]: 
        True
```

## JSON converter example

In the example below, a DataFrame with multiple data types is converted to JSON (first to NTV format and then to Table Schema format).

The DataFrame resulting from these JSON conversions are identical to the initial DataFrame (reversibility).

With the existing JSON interface, these conversions are not possible.

```python
In [1]: from shapely.geometry import Point
        from datetime import date
        import pandas as pd
        import ntv_pandas as npd

In [2]: data = {'index':        [100, 200, 300, 400, 500],
                'dates::date':  [date(1964,1,1), date(1985,2,5), date(2022,1,21), date(1964,1,1), date(1985,2,5)],
                'value':        [10, 10, 20, 20, 30],
                'value32':      pd.Series([12, 12, 22, 22, 32], dtype='int32'),
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

JSON-NTV representation:

```python
In [5]: df_to_json = df.npd.to_json()
        pprint(df_to_json, compact=True, width=120, sort_dicts=False)
Out[5]: {':tab': {'index': [100, 200, 300, 400, 500],
                  'dates::date': ['1964-01-01', '1985-02-05', '2022-01-21', '1964-01-01', '1985-02-05'],
                  'value': [10, 10, 20, 20, 30],
                  'value32::int32': [12, 12, 22, 22, 32],
                  'res': [10, 20, 30, 10, 20],
                  'coord::point': [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0], [3.0, 4.0]],
                  'names::string': ['john', 'eric', 'judith', 'mila', 'hector'],
                  'unique': True}}
```

Reversibility:

```python
In [6]: print(npd.read_json(df_to_json).equals(df))
Out[6]: True
```

Table Schema representation:

```python
In [7]: df_to_table = df.npd.to_json(table=True)
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

Reversibility:

```python
In [9]: print(npd.read_json(df_to_table).equals(df))
Out[9]: True
```
