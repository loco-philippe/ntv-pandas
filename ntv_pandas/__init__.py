# -*- coding: utf-8 -*-
"""
***JSON-NTV Package***

Created on Fri Dec 24 15:21:14 2021

@author: philippe@loco-labs.io

This package contains the following classes:

- `NTV.json_ntv.namespace` :
    - `NTV.json_ntv.namespace.Namespace`
    - `NTV.json_ntv.namespace.NtvType`

        
- `NTV.json_ntv.ntv` :
    - `NTV.json_ntv.ntv.NtvSingle`
    - `NTV.json_ntv.ntv.NtvList`
    - `NTV.json_ntv.ntv.Ntv` (abstract class)

- `NTV.json_ntv.ntv_patch` :
    
    - `NTV.json_ntv.ntv_patch.NtvOp`
    - `NTV.json_ntv.ntv_patch.NtvPatch`

- `NTV.json_ntv.ntv_comment` :
    
    - `NTV.json_ntv.ntv_comment.NtvComment`

- `NTV.json_ntv.ntv_util` :
    
    - `NTV.json_ntv.ntv_util.NtvTree`
    - `NTV.json_ntv.ntv_util.NtvJsonEncoder`
    - `NTV.json_ntv.ntv_util.NtvError`
    - `NTV.json_ntv.ntv_util.NtvConnector` (abstract class)    
          
- `NTV.json_ntv.pandas_ntv_connector` :
    
    - `NTV.json_ntv.pandas_ntv_connector.DataFrameConnec`
    - `NTV.json_ntv.pandas_ntv_connector.SeriesConnec`
    
    
- `NTV.json_ntv.ntv_connector` :
    
    - `NTV.json_ntv.ntv_connector.DataFrameConnec`
    - `NTV.json_ntv.ntv_connector.SeriesConnec`
    - `NTV.json_ntv.ntv_connector.NfieldConnec`
    - `NTV.json_ntv.ntv_connector.SfieldConnec`
    - `NTV.json_ntv.ntv_connector.NdatasetConnec`
    - `NTV.json_ntv.ntv_connector.SdatasetConnec`
    - `NTV.json_ntv.ntv_connector.MermaidConnec`
    - `NTV.json_ntv.ntv_connector.CborConnec`
    - `NTV.json_ntv.ntv_connector.ShapelyConnec` 
       
# 0 - Abstract

Today, the semantic level of shared data remains low. It is very often limited 
to the type of data defined in the exchange formats (strings for CSV formats; 
numbers, strings, arrays and objects for JSON formats).

The proposed consists of adding a type and a name to the data exchanged (see also the 
[JSON-NTV specification](https://github.com/loco-philippe/NTV/blob/main/documentation/JSON-NTV-standard.pdf)).

With this evolution any data, whatever its semantic level, can be identified, 
shared and interpreted in a consistent way.
The implementation of a type with a nested structure facilitates its appropriation.
Finally, compatibility with existing JSON structures allows progressive deployment.

# 1 - NTV structure

The constructed entities (called NTV for *named typed value*) are therefore a triplet
 with one mandatory element (the value in JSON format) and two optional elements (name, type).
>
> *For example, the location of Paris can be represented by:*
> - *a name: "Paris",*
> - *a type: the coordinates of a point according to the GeoJSON format,*
> - *a value: [ 2.3522, 48.8566]*

The easiest way to add this information is to use a JSON-object with a single member
 using the syntax [JSON-ND](https://github.com/glenkleidon/JSON-ND) for the first 
 term of the member and the JSON-value for the second term of the member.
>
> *For the example above, the JSON representation is:*    
> *```{ "paris:point" : [2.3522, 48.8566] }```*

With this approach, three NTV entities are defined:
- a primitive entity which is not composed of any other entity (NTV-single),
- two structured entities: an unordered collection of NTV entities (NTV-set) and
 an ordered sequence of NTV entities (NTV-list).
      
as well as two JSON formats:
- simple format when the name and the type are not present (this is the usual case of CSV data),
- named format when the name or type is present (see example above for an NTV-single
entity and below for a structured entity).
>
> *Example of an entity composed of two other entities:*
> - *```{ "cities::point": [[2.3522, 48.8566], [4.8357, 45.7640]] }``` for an NTV-list entity*
> - *```{ "cities::point": { "paris":[2.3522, 48.8566], "lyon":[4.8357, 45.7640] } }``` 
for an NTV-set entity*
>
> *Note: This syntax can also be used for CSV file headers*

The type incorporates a notion of `namespaces` that can be nested.
> *For example, the type: "ns1.ns2.type" means that:*
> - *ns1. is a namespace defined in the global namespace,*
> - *ns2. is a namespace defined in the ns1 namespace.,*
> - *type is defined in the ns2 namespace.*    
    
This structuring of type makes it possible to reference any type of data that has
 a JSON representation and to consolidate all the shared data structures within the
 same tree of types.


"""
from ntv_pandas.pandas_ntv_connector import DataFrameConnec, SeriesConnec, read_json, to_json, as_def_type


#print('package :', __package__)