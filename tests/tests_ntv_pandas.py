# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 09:57:26 2023

@author: Philippe@loco-labs.io

The `NTV.test_ntv` module contains the unit tests (class unittest) for the
`NtvSingle`, `NtvList` and `NtvSet` classes.
"""
import unittest
import datetime
from datetime import date
import csv

import pandas as pd
import ntv_pandas as npd
from shapely.geometry import Point, Polygon, LineString

from json_ntv import Ntv, from_csv, to_csv

class TestNtvTabular(unittest.TestCase):
    '''test NTV tabular'''

    def test_tab_field_pandas_ilist_Iindex(self):
        field = Ntv.obj({':field':
                         {'dates::datetime': ['1964-01-01', '1985-02-05', '2022-01-21']}})
        tab = Ntv.obj({':tab':
                       {'index':           [1, 2, 3],
                        'dates::datetime': ['1964-01-01', '1985-02-05', '2022-01-21'],
                        'value':           [10, 20, 30],
                        'value32::int32':  [10, 20, 30],
                        'res':             {'res1': 10, 'res2': 20, 'res3': 30},
                        'coord::point':    [[1, 2], [3, 4], [5, 6]],
                        'names::string':   ['john', 'eric', 'judith']}})
        sr = field.to_obj(format='obj', dicobj={
                          'field': 'SeriesConnec'})
        self.assertTrue(sr.equals(Ntv.obj(sr).to_obj(
            format='obj', dicobj={'field': 'SeriesConnec'})))
        df = tab.to_obj(format='obj', dicobj={'tab': 'DataFrameConnec'})
        # il  = tab.to_obj  (format='obj')
        # idx = field.to_obj(format='obj')
        # self.assertEqual(idx, Ntv.obj(idx).to_obj(format='obj'))
        # self.assertEqual(il, Ntv.obj(il).to_obj(format='obj'))
        self.assertTrue(df.equals(Ntv.obj(df).to_obj(
            format='obj', dicobj={'tab': 'DataFrameConnec'})))

    def test_csv(self):
        tab = Ntv.obj({':tab':
                       {'index':           [1, 2, 3],
                        'dates::datetime': ['1964-01-01', '1985-02-05', '2022-01-21'],
                        'value':           [10, 20, 30],
                        'value32::int32':  [10, 20, 30],
                        'coord::point':    [[1, 2], [3, 4], [5, 6]],
                        'names::string':   ['john', 'eric', 'judith']}})
        self.assertEqual(tab, from_csv(to_csv('test.csv', tab)))
        self.assertEqual(tab, from_csv(
            to_csv('test.csv', tab, quoting=csv.QUOTE_ALL)))
        
class TestNTVpandas(unittest.TestCase):
    '''test pandas_NTV_connector'''

    def test_series(self):
        '''test SeriesConnec'''
        # json interface ok
        srs = [  # without ntv_type, without dtype
            pd.Series([{'a': 2, 'e': 4}, {'a': 3, 'e': 5}, {'a': 4, 'e': 6}]),
            pd.Series([[1, 2], [3, 4], [5, 6]]),
            pd.Series([[1, 2], [3, 4], {'a': 3, 'e': 5}]),
            pd.Series([True, False, True]),
            pd.Series(['az', 'er', 'cd']),
            pd.Series(['az', 'az', 'az']),
            pd.Series([1, 2, 3]),
            pd.Series([1.1, 2, 3]),

            # without ntv_type, with dtype
            pd.Series([10, 20, 30], dtype='Int64'),
            pd.Series([True, False, True], dtype='boolean'),
            pd.Series([1.1, 2, 3], dtype='float64'),

            # with ntv_type only in json data (not numbers)
            pd.Series([pd.NaT, pd.NaT, pd.NaT]),
            pd.Series([datetime.datetime(2022, 1, 1), datetime.datetime(2022, 1, 2)],
                      dtype='datetime64[ns]'),
            pd.Series(pd.to_timedelta(['1D', '2D'])),
            pd.Series(['az', 'er', 'cd'], dtype='string'),

            # with ntv_type only in json data (numbers)
            pd.Series([1, 2, 3], dtype='Int32'),
            pd.Series([1, 2, 3], dtype='UInt64'),
            pd.Series([1, 2, 3], dtype='float32'),

            # with ntv_type in Series name and in json data (numbers)
            pd.Series([1, 2, 3], name='::int64'),
            # force dtype dans la conversion json
            pd.Series([1, 2, 3], dtype='Float64', name='::float64'),

            # with ntv_type in Series name and in json data (not numbers)
            pd.Series([[1, 2], [3, 4], [5, 6]], name='::array'),
            pd.Series([{'a': 2, 'e': 4}, {'a': 3, 'e': 5},
                       {'a': 4, 'e': 6}], name='::object'),
            pd.Series([None, None, None], name='::null'),
            pd.Series(["geo:13.412 ,103.866", "mailto:John.Doe@example.com"],
                      name='::uri', dtype='string'),
            pd.Series(["///path/to/file", "//host.example.com/path/to/file"],
                      name='::file', dtype='string'),

            # with ntv_type converted in object dtype (not in datetime)
            pd.Series([datetime.date(2022, 1, 1),
                       datetime.date(2022, 1, 2)], name='::date'),
            pd.Series([datetime.time(10, 21, 1),
                       datetime.time(8, 1, 2)], name='::time'),

            # with ntv_type unknown in pandas and with pandas conversion
            pd.Series([1, 2, 3], dtype='int64', name='::day'),
            pd.Series([2001, 2002, 2003], dtype='int64', name='::year'),
            pd.Series([21, 10, 55], name='::minute'),

            # with ntv_type unknown in pandas and NTV conversion
            pd.Series([Point(1, 0), Point(1, 1),
                       Point(1, 2)], name='::point'),
            # pd.Series([Polygon(), Polygon([[1.0, 2.0], [1.0, 3.0], [2.0, 4.0]]),
            pd.Series([Polygon([[1.0, 2.0], [1.0, 3.0], [2.0, 4.0]]),
                       Polygon([[1.0, 2.0], [1.0, 30.0], [30.0, 30.0], [30, 2]],
                               [[[5.0, 16.0], [5.0, 27.0], [20.0, 27.0]]])],
                      name='::polygon'),
            pd.Series([Point(1, 0), LineString([[1.0, 2.0], [1.0, 3.0]]),
                       Polygon([[1.0, 2.0], [1.0, 3.0], [2.0, 4.0]]),
                       Polygon([[1.0, 2.0], [1.0, 30.0], [30.0, 30.0], [30, 2]],
                               [[[5.0, 16.0], [5.0, 27.0], [20.0, 27.0]]])],
                      name='::geometry'),
            pd.Series([Point(1, 0), Point(1, 1), Point(1, 2),
                       Polygon([[1.0, 2.0], [1.0, 3.0], [2.0, 4.0]]),
                       Polygon([[1.0, 2.0], [1.0, 30.0], [30.0, 30.0], [30, 2]],
                               [[[5.0, 16.0], [5.0, 27.0], [20.0, 27.0]]])],
                      name='::geojson'),
        ]
        for sr in srs:
            # print(Ntv.obj(sr))
            self.assertTrue(npd.as_def_type(sr).equals(
                Ntv.obj(sr).to_obj(format='obj')))
            self.assertEqual(Ntv.obj(sr).to_obj(format='obj').name, sr.name)
            self.assertTrue(npd.as_def_type(sr).equals(
                npd.read_json(npd.to_json(sr))))
            self.assertEqual(npd.read_json(npd.to_json(sr)).name, sr.name)
            self.assertEqual(npd.read_json(
                npd.to_json(sr, table=True)).name, sr.name)
            self.assertTrue(npd.as_def_type(sr).equals(
                npd.read_json(npd.to_json(sr, table=True))))

    def test_json_sfield_full(self):
        '''test SeriesConnec'''
        # json interface ok
        for a in [{'test::int32': [1, 2, 3]},
                  {'test': [1, 2, 3]},
                  [1.0, 2.1, 3.0],
                  ['er', 'et', 'ez'],
                  [True, False, True],
                  {'::boolean': [True, False, True]},
                  {'::string': ['er', 'et', 'ez']},
                  {'test::float32': [1.0, 2.5, 3.0]},
                  {'::int64': [1, 2, 3]},
                  {'::datetime': ["2021-12-31T23:00:00.000",
                                  "2022-01-01T23:00:00.000"]},
                  {'::date': ["2021-12-31", "2022-01-01"]},
                  {'::time': ["23:00:00", "23:01:00"]},
                  {'::object': [{'a': 3, 'e': 5}, {'a': 4, 'e': 6}]},
                  {'::array': [[1, 2], [3, 4], [5, 6]]},
                  True,
                  {':boolean': True}
                  ]:
            ntv = Ntv.from_obj({':field': a})
            # print(ntv)
            self.assertEqual(Ntv.obj(ntv.to_obj(format='obj')), ntv)
            self.assertEqual(npd.to_json(npd.read_json(ntv)), ntv.to_obj())

    def test_json_sfield_default(self):
        '''test SeriesConnec'''
        # json interface ok (categorical data)
        for a in [{'test': [{'::int32': [1, 2, 3]}, [0, 1, 2, 0, 1]]},
                  {'test': [[1, 2, 3], [0, 1, 2, 0, 1]]},
                  [[1.0, 2.1, 3.0], [0, 1, 2, 0, 1]],
                  [['er', 'et', 'ez'], [0, 1, 2, 0, 1]],
                  [[True, False], [0, 1, 0, 1, 0]],
                  [{'::string': ['er', 'et', 'ez']}, [0, 1, 2, 0, 1]],
                  {'test': [{'::float32': [1.0, 2.5, 3.0]}, [0, 1, 2, 0, 1]]},
                  [{'::int64': [1, 2, 3]}, [0, 1, 2, 0, 1]],
                  [{'::datetime': ["2021-12-31T23:00:00.000",
                                   "2022-01-01T23:00:00.000"]}, [0, 1, 0, 1, 0]],
                  [{'::date': ["2021-12-31", "2022-01-01"]}, [0, 1, 0, 1, 0]],
                  [{'::time': ["23:00:00", "23:01:00"]}, [0, 1, 0, 1, 0]],
                  {'test_date': [{'::datetime': [
                      "2021-12-31T23:00:00.000", "2022-01-01T23:00:00.000"]}, [0, 1, 0, 1, 0]]},
                  [{'::boolean': [True, False]}, [0, 1, 0, 1, 0]],
                  [[True], [2]],  # periodic Series
                  {'quantity': [['1 kg', '10 kg'], [4]]}]:  # periodic Series
            ntv = Ntv.from_obj({':field': a})
            # print(ntv)
            self.assertEqual(Ntv.obj(ntv.to_obj(format='obj')), ntv)
            self.assertEqual(npd.to_json(npd.read_json(ntv)), ntv.to_obj())


class TestTablePandas(unittest.TestCase):
    '''tests DataFrameConnec TableSchema'''

    def test_dataframe(self):
        '''tests DataFrameConnec TableSchema'''
        for df in [
            pd.DataFrame({'test::date': pd.Series([date(2021, 1, 5), date(
                2021, 1, 5), date(2021, 1, 5)]), 'entiers': pd.Series([1, 2, 3])}),

        ]:
            fields = npd.to_json(df, table=True)['schema']['fields']
            rang = [field['name'] for field in fields].index('test')
            self.assertFalse(fields[rang]['type'] is None)
            self.assertTrue(
                df.equals(npd.read_json(npd.to_json(df, table=True))))


class TestExports(unittest.TestCase):
    '''test exports Xarray, scipp'''

    def test_dataframe(self):
        '''test exports Xarray, scipp'''
        fruits = {'plants':      ['fruit', 'fruit', 'fruit', 'fruit', 'vegetable',
                                  'vegetable', 'vegetable', 'vegetable'],
                  'plts':        ['fr', 'fr', 'fr', 'fr', 've', 've', 've', 've'],
                  'quantity':    ['1 kg', '10 kg', '1 kg', '10 kg', '1 kg', '10 kg',
                                  '1 kg', '10 kg'],
                  'product':     ['apple', 'apple', 'orange', 'orange', 'peppers',
                                  'peppers', 'carrot', 'carrot'],
                  'price':       [1, 10, 2, 20, 1.5, 15, 1.5, 20],
                  'price level': ['low', 'low', 'high', 'high', 'low', 'low',
                                  'high', 'high'],
                  'group':       ['fruit 1', 'fruit 10', 'fruit 1', 'veget',
                                  'veget', 'veget', 'veget', 'veget'],
                  'id':          [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
                  'supplier':    ["sup1", "sup1", "sup1", "sup2", "sup2", "sup2",
                                  "sup2", "sup1"],
                  'location':    ["fr", "gb", "es", "ch", "gb", "fr", "es", "ch"],
                  'valid':       ["ok", "ok", "ok", "ok", "ok", "ok", "ok", "ok"]}
        kwargs = {'dims': ['product', 'quantity'],
                  'info': False, 'ntv_type': False}
        df_fruits = pd.DataFrame(fruits)
        xd_fruits = df_fruits.npd.to_xarray(**kwargs)
        df_fruits_xd = npd.from_xarray(xd_fruits, ntv_type=False)
        df_fruits_xd_sort = df_fruits_xd.reset_index()[list(
            df_fruits.columns)].sort_values(list(df_fruits.columns)).reset_index(drop=True)
        df_fruits_sort = df_fruits.sort_values(
            list(df_fruits.columns)).reset_index(drop=True)
        self.assertTrue(df_fruits_xd_sort.equals(df_fruits_sort))
        # self.assertEqual(list(xd_fruits.dims), ['product', 'quantity'])
        sc_fruits = df_fruits.npd.to_scipp(**kwargs)
        df_fruits_sc = npd.from_scipp(sc_fruits, ntv_type=False)
        df_fruits_sc_sort = df_fruits_sc.reset_index()[list(
            df_fruits.columns)].sort_values(list(df_fruits.columns)).reset_index(drop=True)
        df_fruits_sort = df_fruits.sort_values(
            list(df_fruits.columns)).reset_index(drop=True)
        self.assertTrue(df_fruits_sc_sort.equals(df_fruits_sort))
        # self.assertEqual(sc_fruits.dims, ('product', 'quantity'))


if __name__ == '__main__':

    unittest.main(verbosity=2)
