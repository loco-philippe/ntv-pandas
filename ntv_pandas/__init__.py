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

from ntv_pandas.pandas_ntv_connector import DataFrameConnec as DataFrameConnec
from ntv_pandas.pandas_ntv_connector import SeriesConnec as SeriesConnec
from ntv_pandas.pandas_ntv_connector import read_json as read_json
from ntv_pandas.pandas_ntv_connector import equals as equals
from ntv_pandas.pandas_ntv_connector import as_def_type as as_def_type
from ntv_pandas.pandas_ntv_connector import to_json as to_json
from ntv_pandas.pandas_ntv_connector import to_analysis as to_analysis
from ntv_pandas.pandas_ntv_connector import from_xarray as from_xarray
from ntv_pandas.pandas_ntv_connector import from_scipp as from_scipp
from ntv_pandas.pandas_accessors import NpdDataFrameAccessor as NpdDataFrameAccessor

# path = Path(ntv_pandas.pandas_ntv_connector.__file__).parent

# print('package :', __package__)
