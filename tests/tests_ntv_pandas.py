# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 09:57:26 2023

@author: Philippe@loco-labs.io

The `NTV.test_ntv` module contains the unit tests (class unittest) for the
`NtvSingle`, `NtvList` and `NtvSet` classes.
"""
import unittest
import datetime
from datetime import date, time

import pandas as pd
import ntv_pandas as npd
from shapely.geometry import Point, Polygon
    
from json_ntv import Ntv        

class Test_NTV_pandas(unittest.TestCase):
    
    def test_series(self):
        
        # json interface ok
        srs = [# without ntv_type, without dtype
               pd.Series([{'a': 2, 'e':4}, {'a': 3, 'e':5}, {'a': 4, 'e':6}]),  
               pd.Series([[1,2], [3,4], [5,6]]),  
               pd.Series([[1,2], [3,4], {'a': 3, 'e':5}]),  
               pd.Series([True, False, True]),
               pd.Series(['az', 'er', 'cd']),
               pd.Series(['az', 'az', 'az']),
               pd.Series([1,2,3]),
               pd.Series([1.1,2,3]),
               
               # without ntv_type, with dtype
               pd.Series([10,20,30], dtype='Int64'),
               pd.Series([True, False, True], dtype='boolean'),
               pd.Series([1.1, 2, 3], dtype='float64'), 
            
               # with ntv_type only in json data (not numbers)
               pd.Series([pd.NaT, pd.NaT, pd.NaT]),
               pd.Series([datetime.datetime(2022, 1, 1), datetime.datetime(2022, 1, 2)],
                         dtype='datetime64[ns]'),
               pd.Series(pd.to_timedelta(['1D', '2D'])),
               pd.Series(['az', 'er', 'cd'], dtype='string'), 

               # with ntv_type only in json data (numbers)
               pd.Series([1,2,3], dtype='Int32'), 
               pd.Series([1,2,3], dtype='UInt64'),
               pd.Series([1,2,3], dtype='float32'),
            
               # with ntv_type in Series name and in json data (numbers)
               pd.Series([1,2,3], name='::int64'),
               pd.Series([1,2,3], dtype='Float64', name='::float64'), # force dtype dans la conversion json

               # with ntv_type in Series name and in json data (not numbers)
               pd.Series([[1,2], [3,4], [5,6]], name='::array'),  
               pd.Series([{'a': 2, 'e':4}, {'a': 3, 'e':5}, {'a': 4, 'e':6}], name='::object'),  
               pd.Series([None, None, None], name='::null'), 
               pd.Series(["geo:13.412 ,103.866", "mailto:John.Doe@example.com"], name='::uri', dtype='string'),
               pd.Series(["///path/to/file", "//host.example.com/path/to/file"], name='::file', dtype='string'),
               
               # with ntv_type converted in object dtype (not in datetime)
               pd.Series([datetime.date(2022, 1, 1), datetime.date(2022, 1, 2)], name='::date'),
               pd.Series([datetime.time(10, 21, 1), datetime.time(8, 1, 2)], name='::time'),
               
               # with ntv_type unknown in pandas and with pandas conversion               
               pd.Series([1,2,3], dtype='int64', name='::day'),
               pd.Series([2001,2002,2003], dtype='int64', name='::year'),
               pd.Series([21,10,55], name='::minute'),

               # with ntv_type unknown in pandas and NTV conversion
               pd.Series([Point(1, 0), Point(1, 1), Point(1, 2)], name='::point'),
               pd.Series([Point(1, 0), Point(1, 1), Point(1, 2),
                          Polygon([[1.0, 2.0], [1.0, 3.0], [2.0, 4.0]]),
                          Polygon([[1.0, 2.0], [1.0, 30.0], [30.0, 30.0], [30,2]],
                                  [[[5.0, 16.0], [5.0, 27.0], [20.0, 27.0]]])], 
                                  name='::geometry'),
               pd.Series([Point(1, 0), Point(1, 1), Point(1, 2),
                          Polygon([[1.0, 2.0], [1.0, 3.0], [2.0, 4.0]]),
                          Polygon([[1.0, 2.0], [1.0, 30.0], [30.0, 30.0], [30,2]],
                                  [[[5.0, 16.0], [5.0, 27.0], [20.0, 27.0]]])], 
                                  name='::geojson'),
        ]
        for sr in srs:
            #print(Ntv.obj(sr))
            self.assertTrue(npd.as_def_type(sr).equals(Ntv.obj(sr).to_obj(format='obj')))
            self.assertEqual(Ntv.obj(sr).to_obj(format='obj').name, sr.name)
            self.assertTrue(npd.as_def_type(sr).equals(npd.read_json(npd.to_json(sr))))
            self.assertEqual(npd.read_json(npd.to_json(sr)).name, sr.name)            

    def test_json_sfield_full(self):

        # json interface ok
        for a in [{'test::int32': [1,2,3]},
                  {'test': [1,2,3]},
                  [1.0, 2.1, 3.0],
                  ['er', 'et', 'ez'],
                  [True, False, True],
                  {'::boolean': [True, False, True]},
                  {'::string': ['er', 'et', 'ez']},
                  {'test::float32': [1.0, 2.5, 3.0]},
                  {'::int64': [1,2,3]},
                  {'::datetime': ["2021-12-31T23:00:00.000","2022-01-01T23:00:00.000"] },
                  {'::date': ["2021-12-31", "2022-01-01"] },
                  {'::time': ["23:00:00", "23:01:00"] },
                  {'::object': [{'a': 3, 'e':5}, {'a': 4, 'e':6}]},
                  {'::array': [[1,2], [3,4], [5,6]]},
                  True,
                  {':boolean': True}
                 ]:
            ntv = Ntv.from_obj({':field': a})
            #print(ntv)
            self.assertEqual(Ntv.obj(ntv.to_obj(format='obj')), ntv)            
            self.assertEqual(npd.to_json(npd.read_json(ntv)), ntv.to_obj())            
            
    def test_json_sfield_default(self):

        # json interface ok (categorical data)
        for a in [{'test': [{'::int32': [1, 2, 3]}, [0,1,2,0,1]]},
                  {'test': [[1, 2, 3], [0,1,2,0,1]]},
                  [[1.0, 2.1, 3.0], [0,1,2,0,1]],
                  [['er', 'et', 'ez'], [0,1,2,0,1]],
                  [[True, False], [0,1,0,1,0]],
                  [{'::string': ['er', 'et', 'ez']}, [0,1,2,0,1]],
                  {'test':[{'::float32': [1.0, 2.5, 3.0]}, [0,1,2,0,1]]},
                  [{'::int64': [1, 2, 3]}, [0,1,2,0,1]],
                  [{'::datetime': ["2021-12-31T23:00:00.000", "2022-01-01T23:00:00.000"] }, [0,1,0,1,0]],
                  [{'::date': ["2021-12-31", "2022-01-01"] }, [0,1,0,1,0]],
                  [{'::time': ["23:00:00", "23:01:00"] }, [0,1,0,1,0]],
                  {'test_date': [{'::datetime': ["2021-12-31T23:00:00.000", "2022-01-01T23:00:00.000"] }, [0,1,0,1,0]]},
                  [{'::boolean': [True, False]}, [0,1,0,1,0]],
                  [[True], [2]], # periodic Series
                  {'quantity': [['1 kg', '10 kg'], [4]]}]:  # periodic Series
            ntv = Ntv.from_obj({':field': a})
            #print(ntv)
            self.assertEqual(Ntv.obj(ntv.to_obj(format='obj')), ntv)            
            self.assertEqual(npd.to_json(npd.read_json(ntv)), ntv.to_obj())            

class Test_table_pandas(unittest.TestCase):
    
    def test_series(self):
        
        # json interface ok
        for srs in [
            pd.Series([date(2021,1,5), date(2021,1,5), date(2021,1,5)], name='test::date'),
            pd.Series([1,2,3], name='test')
               ]:
            fields = npd.to_json(srs, table=True)['schema']['fields']
            rang = [field['name'] for field in fields].index('test')
            self.assertFalse(fields[rang]['type'] is None)

    def test_dataframe(self):
        for df in [
            pd.DataFrame({'test::date': pd.Series([date(2021,1,5), date(2021,1,5)
                        , date(2021,1,5)]), 'entiers': pd.Series([1,2,3])})
               ]:
            fields = npd.to_json(df, table=True)['schema']['fields']
            rang = [field['name'] for field in fields].index('test')
            self.assertFalse(fields[rang]['type'] is None)
            self.assertTrue(df.equals(npd.read_json(npd.to_json(df, table=True))))
if __name__ == '__main__':
    
    unittest.main(verbosity=2)
