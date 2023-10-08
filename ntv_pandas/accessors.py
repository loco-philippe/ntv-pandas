# -*- coding: utf-8 -*-
"""
Created on Sun Oct 8 2023

@author: philippe@loco-labs.io


Accessor methods bound to pd.Series.npd, pd.DataFrame.npd
"""
import pandas as pd
from pandas_ntv_connector import to_json, as_def_type

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

    def to_json(self, **kwargs):
        """Accessor for method `pandas_ntv_connector.to_json` invoked as
        `pd.DataFrame.npd.to_json`"""
        return to_json(self._obj, **kwargs)

    def as_def_type(self):
        """Accessor for method `pandas_ntv_connector.as_def_type` invoked as
        `pd.DataFrame.npd.as_def_type`"""
        return as_def_type(self._obj)


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
