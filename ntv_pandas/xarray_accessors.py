# -*- coding: utf-8 -*-
"""
Created on Thu May 16 11:02:14 2024

@author: a lab in the Air
"""

import xarray as xr

from ntv_numpy import Xdataset
from ntv_pandas.pandas_ntv_connector import to_json, as_def_type, equals
from ntv_pandas.pandas_ntv_connector import to_analysis, check_relation

try:
    # delete the accessor to avoid warning
    del xr.Dataset.npd
except AttributeError:
    pass

@xr.register_dataset_accessor("npd")
class NpdDatasetAccessor:
    """Accessor class for methods invoked as `xr.Dataset.npd.*`"""
    
    def __init__(self, xarray_obj):
        self._obj = xarray_obj

    def to_dataframe(self, **kwargs):
        """Accessor for method `Xdataset.from_xarray.to_dataframe` invoked as
        xr.Dataset.npd.to_dataframe`.

        *Parameters*

        - **dims**: list of string (default None) - order of dimensions to apply
        - **dataset** : Boolean (default True) - if False and a single data_var,
        return a xr.DataArray
        - **info** : Boolean (default True) - if True, add json representation
        of 'relative' Xndarrays and 'data_arrays' Xndarrays in attrs"""
        return Xdataset.from_xarray(self._obj, **kwargs).to_dataframe(**kwargs)
