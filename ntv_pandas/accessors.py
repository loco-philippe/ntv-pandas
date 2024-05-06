# -*- coding: utf-8 -*-
"""
Created on Sun Oct 8 2023

@author: philippe@loco-labs.io


Accessor methods bound to pd.Series.npd, pd.DataFrame.npd
"""
import pandas as pd
from tab_analysis import AnaDataset
from ntv_numpy import Xdataset
from ntv_pandas.pandas_ntv_connector import to_json, as_def_type, equals
from ntv_pandas.pandas_ntv_connector import to_analysis, check_relation

try:
    # delete the accessor to avoid warning
    del pd.DataFrame.npd
except AttributeError:
    pass


@pd.api.extensions.register_dataframe_accessor("npd")
class NpdDataFrameAccessor:
    """Accessor class for methods invoked as `pd.DataFrame.npd.*`"""

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def analysis(self, distr=False):
        """Accessor for method `tab_analysis.AnaDataset` applied with
        `pandas_ntv_connector.to_analysis` invoked as `pd.DataFrame.npd.analysis`"""
        return AnaDataset(to_analysis(self._obj, distr))

    def check_relation(self, parent, child, typecoupl, value=True):
        ''' Accessor for method `pandas_ntv_connector.check_relation` invoket as
        `pd.DataFrame.npd.check_relation`'''
        return check_relation(self._obj, parent, child, typecoupl, value)

    def to_json(self, **kwargs):
        """Accessor for method `pandas_ntv_connector.to_json` invoked as
        `pd.DataFrame.npd.to_json`

        *parameters*

        - **pd_array** : Series or Dataframe to convert
        - **encoded** : boolean (default: False) - if True return a JSON text else a JSON value
        - **header** : boolean (default: True) - if True the JSON data is included as
        value in a {key:value} object where key is ':field' for Series or ':tab' for DataFrame
        - **table** : boolean (default False) - if True return TableSchema format
        - **index** : boolean (default True) - if True the index Series is included"""
        return to_json(self._obj, **kwargs)

    def as_def_type(self):
        """Accessor for method `pandas_ntv_connector.as_def_type` invoked as
        `pd.DataFrame.npd.as_def_type`"""
        return as_def_type(self._obj)

    def equals(self, other):
        """Accessor for method `pandas_ntv_connector.equals` invoked as
        `pd.DataFrame.npd.equals`"""
        return equals(self._obj, other)

    def to_xarray(self, **kwargs):
        """Accessor for method `Xdataset.from_dataframe.to_xarray` invoked as
        `pd.DataFrame.npd.to_xarray`.

        *Parameters*

        - dims: list of string (default None) - order of dimensions to apply
        - **dataset** : Boolean (default True) - if False and a single data_var,
        return a sc.DataArray
        - **datagroup** : Boolean (default True) - if True, return a sc.DataGroup
        which contains the sc.DataArray/sc.Dataset and the other data else only
        sc.DataArray/sc.Dataset"""
        return Xdataset.from_dataframe(self._obj, **kwargs).to_xarray(**kwargs)

    def to_scipp(self, **kwargs):
        """Accessor for method `Xdataset.from_dataframe.to_scipp` invoked as
        `pd.DataFrame.npd.to_scipp`.

        *Parameters*

        - dims: list of string (default None) - order of dimensions to apply
        - **dataset** : Boolean (default True) - if False and a single data_var,
        return a DataArray
        - **datagroup** : Boolean (default True) - if True return a DataGroup with
        metadata and data_arrays
        - **ntv_type** : Boolean (default True) - if True add ntv-type to the name"""
        return Xdataset.from_dataframe(self._obj, **kwargs).to_scipp(**kwargs)


try:
    # delete the accessor to avoid warning
    del pd.Series.npd
except AttributeError:
    pass


@pd.api.extensions.register_series_accessor("npd")
class NpdSeriesAccessor:
    """Accessor class for methods invoked as `pd.Series.npd.*`"""

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def to_json(self, **kwargs):
        """Accessor for method `pandas_ntv_connector.to_json` invoked as
        `pd.Series.npd.to_json`"""
        return to_json(self._obj, **kwargs)

    def as_def_type(self):
        """Accessor for method `pandas_ntv_connector.as_def_type` invoked as
        `pd.Series.npd.as_def_type`"""
        return as_def_type(self._obj)

    def equals(self, other):
        """Accessor for method `pandas_ntv_connector.equals` invoked as
        `pd.DataFrame.npd.equals`"""
        return equals(self._obj, other)
