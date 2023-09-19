# -*- coding: utf-8 -*-
"""
Created on Feb 27 2023

@author: Philippe@loco-labs.io

The `pandas_ntv_connector` module is part of the `ntv-pandas.ntv_pandas` package 
([specification document](
https://loco-philippe.github.io/ES/JSON%20semantic%20format%20(JSON-NTV).htm)).

A NtvConnector is defined by:
- clas_obj: str - define the class name of the object to convert
- clas_typ: str - define the NTVtype of the converted object
- to_obj_ntv: method - converter from JsonNTV to the object
- to_json_ntv: method - converter from the object to JsonNTV

It contains :

- functions `read_json` and `to_json` to convert JSON data and pandas entities

- the child classes of `NTV.json_ntv.ntv.NtvConnector` abstract class:
    - `DataFrameConnec`: 'tab'   connector
    - `SeriesConnec`:    'field' connector
    
"""
import datetime
import json
import configparser
from pathlib import Path
import pandas as pd
import numpy as np

import json_ntv
from json_ntv.ntv import Ntv, NtvConnector, NtvList, NtvSingle
from json_ntv.ntv_connector import ShapelyConnec

def to_json(pd_array, **kwargs):
    ''' convert pandas Series or Dataframe to JSON text or JSON Value.
    
    *parameters*
    
    - **pd_array** : Series or Dataframe to convert
    - **text** : boolean (default: False) - if True return a JSON text else a JSON value
    - **header** : boolean (default: True) - if True the JSON data is included as
    value in a {key:value} object where key is ':field' for Series or ':tab' for DataFrame
    ''' 
    option = {'text': False, 'header': True} | kwargs
    if isinstance(pd_array, pd.Series):
        jsn = SeriesConnec.to_json_ntv(pd_array)[0]
        head = ':field'
    else:
        jsn = DataFrameConnec.to_json_ntv(pd_array)[0]
        head = ':tab'
    if option['header']:      
        jsn = { head: jsn}
    if option['text']:
        return json.dumps(jsn)
    return jsn
    
def read_json(js, **kwargs):
    ''' convert JSON text or JSON Value to pandas Series or Dataframe.
    
    *parameters*
    
    - **js** : JSON text or JSON value to convert
    - **extkeys**: list (default None) - keys to use if not present in ntv_value
    - **decode_str**: boolean (default False) - if True, string values are converted
    in object values
    - **leng**: integer (default None) - leng of the Series (used with single codec value)
    - **alias**: boolean (default False) - if True, convert dtype in alias dtype
    - **annotated**: boolean (default False) - if True, ntv_codec names are ignored
    - **series**: boolean (default False) - used only without header. If True 
    JSON data is converted into Series else DataFrame
    ''' 
    option = {'extkeys': None, 'decode_str': False, 'leng': None, 'alias': False,
              'annotated':False, 'series':False} | kwargs
    jso = json.loads(js) if isinstance(js, str) else js
    ntv = Ntv.from_obj(jso)
    if ntv.type_str == 'field':
        return SeriesConnec.to_obj_ntv(ntv.ntv_value, **option)
    if ntv.type_str == 'tab':
        return DataFrameConnec.to_obj_ntv(ntv.ntv_value, **option)
    if option['series']:
        return SeriesConnec.to_obj_ntv(ntv, **option)
    return DataFrameConnec.to_obj_ntv(ntv.ntv_value, **option)

def as_def_type(pd_array):
    '''convert a Series or DataFrame with default dtype'''
    if isinstance(pd_array, pd.Series):
        return pd_array.astype(SeriesConnec.deftype.get(pd_array.dtype.name, pd_array.dtype.name))
    return pd.DataFrame({col: as_def_type(pd_array[col]) for col in pd_array.columns})
        
class DataFrameConnec(NtvConnector):
    '''NTV connector for pandas DataFrame.
    
    Two static methods are included:
    
    - to_listidx: convert a DataFrame in categorical data 
    - decode_ntv_tab: Generate a tuple data from a NTVvalue
    '''

    clas_obj = 'DataFrame'
    clas_typ = 'tab'

    @staticmethod
    def to_obj_ntv(ntv_value, **kwargs):  # reindex=True, decode_str=False):
        ''' convert json ntv_value into a DataFrame.

        *Parameters*

        - **index** : list (default None) - list of index values,
        - **alias** : boolean (default False) - if True, alias dtype else default dtype
        - **annotated** : boolean (default False) - if True, NTV names are not included.'''
        series = SeriesConnec.to_series

        ntv = Ntv.fast(ntv_value)
        lidx = [list(DataFrameConnec.decode_ntv_tab(ntvf))
                for ntvf in ntv]
        leng = max([idx[6] for idx in lidx])
        option = kwargs | {'leng': leng}
        no_keys = []
        for ind in range(len(lidx)):
            no_keys.append(not lidx[ind][3]
                           and not lidx[ind][4] and not lidx[ind][5])
            NtvConnector.init_ntv_keys(ind, lidx, leng)
            lidx[ind][2] = Ntv.fast(Ntv.obj_ntv(lidx[ind][2], typ=lidx[ind][1],
                                                single=len(lidx[ind][2]) == 1))
        list_series = [series(lidx[ind][2], lidx[ind][0],
                              None if no_keys[ind] else lidx[ind][4], **option)
                       for ind in range(len(lidx))]
        dfr = pd.DataFrame({ser.name: ser for ser in list_series})
        if 'index' in dfr.columns:
            dfr = dfr.set_index('index')
            dfr.index.rename(None, inplace=True)
        return dfr

    @staticmethod
    def to_json_ntv(value, name=None, typ=None):
        ''' convert a DataFrame (value, name, type) into NTV json (json-value, name, type).

        *Parameters*

        - **typ** : string (default None) - type of the NTV object,
        - **name** : string (default None) - name of the NTV object
        - **value** : DataFrame values'''
        df2 = value.reset_index()
        jsn = Ntv.obj([SeriesConnec.to_json_ntv(DataFrameConnec._unic(df2[col]))[0]
                       for col in df2.columns]).to_obj()
        return (jsn, name, DataFrameConnec.clas_typ if not typ else typ)

    @staticmethod
    def to_listidx(dtf):
        ''' convert a DataFrame in categorical data (list of dict for each column
        with keys : 'codec', 'name, 'keys' and length of the DataFrame)'''
        return ([SeriesConnec.to_idx(ser) for name, ser in dtf.items()], len(dtf))

    @staticmethod
    def _unic(srs):
        ''' return simple value if the Series contains a single value'''
        return srs[:1] if np.array_equal(srs.values, [srs.values[0]] * len(srs)) else srs

    @staticmethod
    def decode_ntv_tab(field):
        '''Generate a tuple data from a Ntv tab value (bytes, string, json, Ntv object)

        *Returns*

        - **tuple** : name, dtype, codec, parent, keys, coef, leng
            name (None or string): name of the Field
            dtype (None or string): type of data
            codec (list): list of Field codec values
            parent (None or int): Field parent or None
            keys (None or list): Field keys
            coef (None or int): coef if primary Field else None
            leng (int): length of the Field
        '''
        ntv = Ntv.obj(field)
        typ = ntv.type_str if ntv.ntv_type else None
        nam = ntv.name
        if isinstance(ntv, NtvSingle):
            return (nam, typ, [ntv.to_obj(simpleval=True)], None, None, None, 1)
        val = [ntv_val.to_obj() for ntv_val in ntv]
        if len(ntv) < 2 or len(ntv) > 3 or isinstance(ntv[0], NtvSingle):
            return (nam, typ, val, None, None, None, len(ntv))

        ntvc = ntv[0]
        leng = max(len(ind) for ind in ntv)
        typc = ntvc.type_str if ntvc.ntv_type else None
        valc = ntvc.to_obj(simpleval=True)
        if len(ntv) == 3 and isinstance(ntv[1], NtvSingle) and \
                isinstance(ntv[1].val, (int, str)) and not isinstance(ntv[2], NtvSingle) and \
                isinstance(ntv[2][0].val, int):
            return (nam, typc, valc, ntv[1].val, ntv[2].to_obj(), None, leng)
        if len(ntv) == 2 and len(ntv[1]) == 1 and isinstance(ntv[1].val, (int, str)):
            return (nam, typc, valc, ntv[1].val, None, None, leng)
        if len(ntv) == 2 and len(ntv[1]) == 1 and isinstance(ntv[1].val, list):
            leng = leng * ntv[1][0].val
            return (nam, typc, valc, None, None, ntv[1][0].val, leng)
        if len(ntv) == 2 and len(ntv[1]) > 1 and isinstance(ntv[1][0].val, int):
            return (nam, typc, valc, None, ntv[1].to_obj(), None, leng)
        return (nam, typ, val, None, None, None, len(ntv))


class SeriesConnec(NtvConnector):
    '''NTV connector for pandas Series
    
    Three static methods are included:
    
    - to_idx: convert a Series in categorical data 
    - to_series: return a Series from Field data
    - read_json: return a Series from a NTVvalue
    '''
    clas_obj = 'Series'
    clas_typ = 'field'
    config = configparser.ConfigParser()
    config.read(Path(json_ntv.__file__).parent.joinpath('ntv_pandas.ini'))
    types = pd.DataFrame(json.loads(config['data']['type']), columns=json.loads(config['data']['column']))
    astype = json.loads(config['data']['astype'])
    deftype = {val: key for key, val in astype.items()}

    @staticmethod
    def to_obj_ntv(ntv_value, **kwargs):
        '''Generate a Series Object from a Ntv field object

        *Parameters*

        - **ntv_value**: Ntv object or Ntv value - value to convert in Series

        *parameters (kwargs)*

        - **extkeys**: list (default None) - keys to use if not present in ntv_value
        - **decode_str**: boolean (default False) - if True, string values are converted
        in object values
        - **index**: list (default None) - if present, add the index in Series
        - **leng**: integer (default None) - leng of the Series (used with single codec value)
        - **alias**: boolean (default False) - if True, convert dtype in alias dtype
        - **annotated**: boolean (default False) - if True, ntv_codec names are ignored
        '''
        option = {'extkeys': None, 'decode_str': False, 'leng': None,
                  'annotated':False} | kwargs
        if ntv_value is None:
            return None
        ntv = Ntv.obj(ntv_value, decode_str=option['decode_str'])

        ntv_name, typ, codec, parent, ntv_keys, coef, leng_field = \
            DataFrameConnec.decode_ntv_tab(ntv)
        if parent and not option['extkeys']:
            return None
        if coef:
            ntv_keys = NtvConnector.keysfromcoef(
                coef, leng_field//coef, option['leng'])
        elif option['extkeys'] and parent:
            ntv_keys = NtvConnector.keysfromderkeys(
                option['extkeys'], ntv_keys)
        elif option['extkeys'] and not parent:
            ntv_keys = option['extkeys']
        ntv_codec = Ntv.fast(Ntv.obj_ntv(
            codec, typ=typ, single=len(codec) == 1))
        return SeriesConnec.to_series(ntv_codec, ntv_name, ntv_keys, **kwargs)

    @staticmethod
    def to_json_ntv(value, name=None, typ=None):
        ''' convert a Series (value, name, type) into NTV json (json-value, name, type).

        *Parameters*

        - **typ** : string (default None) - type of the NTV object,
        - **name** : string (default None) - name of the NTV object
        - **value** : Series values'''

        astype = SeriesConnec.astype
        ntv_type_val = SeriesConnec._ntv_type_val
        srs = value.astype(astype.get(value.dtype.name, value.dtype.name))
        sr_name = srs.name if srs.name else ''
        ntv_name, name_type = Ntv.from_obj_name(sr_name)[:2]

        if srs.dtype.name == 'category':
            cdc = pd.Series(srs.cat.categories)
            ntv_type, cat_value = ntv_type_val(name_type, cdc)
            cat_value = NtvList(cat_value, ntv_type=ntv_type).to_obj()
            cod_value = list(srs.cat.codes)
            coef = NtvConnector.encode_coef(cod_value)
            ntv_value = [cat_value, [coef] if coef else cod_value]
            ntv_type = 'json'
        else:
            ntv_type, ntv_value = ntv_type_val(name_type, srs)
        if len(ntv_value) == 1:
            return (NtvSingle(ntv_value[0], ntv_name, ntv_type).to_obj(), name,
                    SeriesConnec.clas_typ if not typ else typ)
        return (NtvList(ntv_value, ntv_name, ntv_type).to_obj(), name,
                SeriesConnec.clas_typ if not typ else typ)

    @staticmethod
    def to_idx(ser):
        ''' convert a Series in categorical data

        *return (dict)*

        - 'codec': list of pandas categories
        - 'name': name of the series
        - 'keys': list of pandas codes
        '''
        idx = ser.astype('category')
        lis = list(idx.cat.categories)
        if lis and isinstance(lis[0], pd._libs.tslibs.timestamps.Timestamp):
            lis = [ts.to_pydatetime().astimezone(datetime.timezone.utc)
                   for ts in lis]
        return {'codec': lis, 'name': ser .name, 'keys': list(idx.cat.codes)}

    @staticmethod
    def to_series(ntv_codec, ntv_name, ntv_keys, **kwargs):
        ''' return a pd.Series from Field data (codec, name, keys)

        *Parameters*

        - **ntv_codec**: Ntv object - codec value to convert in Series values
        - **ntv_type**: string - default type to apply to convert in dtype
        - **ntv_name**: string - name of the Series

        *parameters (kwargs)*

        - **index**: list (default None) - if present, add the index in Series
        - **leng**: integer (default None) - leng of the Series (used with single codec value)
        - **alias**: boolean (default False) - if True, convert dtype in alias dtype
        - **annotated**: boolean (default False) - if True, ntv_codec names are ignored
        '''
        option = {'index': None, 'leng': None, 'alias': False,
                  'annotated': False} | kwargs
        types = SeriesConnec.types.set_index('ntv_type')
        astype = SeriesConnec.astype

        ntv_type = ntv_codec.type_str
        len_unique = option['leng'] if len(
            ntv_codec) == 1 and option['leng'] else 1
        pd_convert = ntv_type in types.index

        dtype = types.loc[ntv_type]['dtype'] if pd_convert else 'object'
        ntv_obj, pd_name, name_type = SeriesConnec._val_nam_typ(
            ntv_codec, ntv_type, ntv_name, pd_convert, option['annotated'])

        if ntv_keys:
            if pd_convert and name_type != 'array':
                categ = SeriesConnec.read_json(ntv_obj, dtype, ntv_type)
                cat_type = categ.dtype.name
                categories = categ.astype(astype.get(cat_type, cat_type))
            else:
                categories = pd.Series(ntv_obj, dtype='object')
            cat = pd.CategoricalDtype(categories=categories)
            data = pd.Categorical.from_codes(codes=ntv_keys, dtype=cat)
            srs = pd.Series(data, name=pd_name,
                            index=option['index'], dtype='category')
        else:
            data = ntv_obj * len_unique
            if pd_convert:
                srs = SeriesConnec.read_json(data, dtype, ntv_type, pd_name)
            else:
                srs = pd.Series(data, name=pd_name, dtype=dtype)
        
        if option['alias']:
            return srs.astype(astype.get(srs.dtype.name, srs.dtype.name))
        return srs.astype(SeriesConnec.deftype.get(srs.dtype.name, srs.dtype.name))

    @staticmethod 
    def read_json(data, dtype, ntv_type, pd_name=None):
        '''return a Series from a NTVvalue'''
        srs = pd.read_json(json.dumps(data), dtype=dtype,
                           typ='series')
        if not pd_name is None:
            srs = srs.rename(pd_name)
        if ntv_type == 'date':
            return pd.to_datetime(srs).dt.date
        if ntv_type == 'time':
            return pd.to_datetime(srs).dt.time
        if ntv_type in ['point', 'polygon', 'line', 'geometry']:
            return srs.apply(ShapelyConnec.to_geometry)
        if ntv_type == 'geojson':
            return srs.apply(ShapelyConnec.from_geojson)
        return srs

    @staticmethod
    def _val_nam_typ(ntv_codec, ntv_type, ntv_name, pd_convert, annotated):
        ''' return Series data from ntv data

        *parameters*

        - **ntv_codec**: Ntv object - codec value to convert in Series values
        - **ntv_type**: string - default type to apply to convert in dtype
        - **ntv_name**: string - name of the Series
        - **pd_convert**: boolean - if True, use pandas json conversion
        - **annotated**: boolean - if True, ntv_codec names are ignored

        *return (tuple)*

        - ntv_obj : list with ntv_codec json values converted to object values
        - pd_name : string with the Serie name
        - name_type : string - pandas types to be converted in 'json' Ntv-type
        '''
        types = SeriesConnec.types.set_index('ntv_type')
        if pd_convert:
            name_type = types.loc[ntv_type]['name_type'] if ntv_type != '' else ''
            pd_name = ntv_name + '::' + name_type if name_type else ntv_name
            pd_name = pd_name if pd_name else None
            if name_type == 'array':
                ntv_obj = ntv_codec.to_obj(format='obj', simpleval=True)
            else:
                ntv_obj = ntv_codec.obj_value(simpleval=annotated, json_array=False,
                                              def_type=ntv_codec.type_str, fast=True)
                ntv_obj = ntv_obj if isinstance(ntv_obj, list) else [ntv_obj]
            return (ntv_obj, pd_name, name_type)
        ntv_obj = ntv_codec.to_obj(format='obj', simpleval=True, def_type=ntv_type)
        return (ntv_obj, ntv_name + '::' + ntv_type, ntv_type)

    @staticmethod
    def _ntv_type_val(name_type, srs):
        ''' convert a simple Series into NTV data (NTV type, NTV json-value). If name_type is None and
        dtype is 'object', the NTV value is the srs values.

        *Parameters*

        - **name_type** : string - default NTV type to be used. If None, dtype is converted in NTV type,
        - **srs** : Series to be converted.'''
        types = SeriesConnec.types.set_index('name_type')
        dtype = srs.dtype.name
        if not name_type:
            types_none = types.loc[None]
            if dtype in types_none.dtype.values:
                ntv_type = types_none.set_index('dtype').loc[dtype].ntv_type
            else:
                ntv_type = 'json'
            return (ntv_type, json.loads(srs.to_json(orient='records',
                        date_format='iso', default_handler=str)))
        ntv_type = name_type
        if ntv_type in ['point', 'line', 'polygon', 'geometry']:
            return (ntv_type, srs.apply(ShapelyConnec.to_coord).to_list())
        if ntv_type == 'geojson':
            return (ntv_type, srs.apply(ShapelyConnec.to_geojson).to_list())
        if ntv_type == 'date':
            srs = srs.astype(str)
        if dtype == 'object':
            return (ntv_type, srs.to_list())
        return (ntv_type, json.loads(srs.to_json(orient='records',
                        date_format='iso', default_handler=str)))

    """@staticmethod 
    def _encode_coef(lis):
        '''Generate a repetition coefficient for periodic list'''
        if len(lis) < 2:
            return 0
        coef = 1
        while coef != len(lis):
            if lis[coef-1] != lis[coef]:
                break
            coef += 1
        if (not len(lis) % (coef * (max(lis) + 1)) and 
            lis == SeriesConnec._keys_from_coef(coef, max(lis) + 1, len(lis))):
            return coef
        return 0

    @staticmethod 
    def _keys_from_coef(coef, period, leng=None):
        ''' return a list of keys with periodic structure'''
        if not leng:
            leng = coef * period
        return None if not (coef and period) else [(ind % (coef * period)) // coef 
                                                   for ind in range(leng)]"""