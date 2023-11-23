# documentation

The documentation presents :

## documents

- [JSON-NTV specification](https://loco-philippe.github.io/ES/JSON%20semantic%20format%20(JSON-NTV).htm) (Json for NTV data)
- [JSON-TAB specification](https://github.com/loco-philippe/NTV/blob/main/documentation/JSON-TAB-standard.pdf) (Json for tabular data)

## Python Connectors documentation

- API
  - [dev](https://loco-philippe.github.io/ntv-pandas/ntv_pandas.html)
  - [v1.0.2](https://loco-philippe.github.io/ntv-pandas/v1.0.2/ntv_pandas.html)
  - [v1.0.1](https://loco-philippe.github.io/ntv-pandas/v1.0.1/ntv_pandas.html)
  - [v1.0.0](https://loco-philippe.github.io/ntv-pandas/v1.0.0/ntv_pandas.html)
  - [v0.1.1](https://loco-philippe.github.io/ntv-pandas/v0.1.1/ntv_pandas.html)
- Release
  - [all versions](https://github.com/loco-philippe/ntv-pandas/tree/main/docs/release.rst)

# Roadmap

- **type extension** : interval dtype and sparse format not yet included
- **table schema** : add type / format (`geojson`/`topojson`, `geopoint`/`default`, `geopoint`/`object`, `duration`/`default`, `string`/`binary`, `string`/`uuid`),
- **null JSON data** : strategy to define
- **multidimensional** : extension of the NTV format for multidimensional data (e.g. Xarray)
- **pandas type** : support for Series or DataFrame which include pandas data
- **data consistency** : controls between NTVtype and NTVvalue
