# -*- coding: utf-8 -*-
"""
***NTV-pandas Package***

Created on Sept 2023

@author: philippe@loco-labs.io

This package contains the following classes and functions:

- `ntv-pandas.ntv_pandas.pandas_ntv_connector` :

    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.DataFrameConnec`
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.SeriesConnec`
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.PdUtil`
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.to_json`
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.read_json`
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.analysis`
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.as_def_type`
    - `ntv-pandas.ntv_pandas.pandas_ntv_connector.equals`

- `ntv-pandas.ntv_pandas.accessors` :
    
    - `ntv-pandas.ntv_pandas.accessors.NpdSeriesAccessor`
    - `ntv-pandas.ntv_pandas.accessors.NpdDataFrameAccessor`  
"""
from ntv_pandas.pandas_ntv_connector import DataFrameConnec, SeriesConnec, read_json
from ntv_pandas.pandas_ntv_connector import to_json, as_def_type, equals, to_analysis
from ntv_pandas.pandas_ntv_connector import from_xarray, from_scipp
import ntv_pandas.accessors

#path = Path(ntv_pandas.pandas_ntv_connector.__file__).parent

#print('package :', __package__)