# TwitGeoSpa
Geospatial analysis and simulation using Twitter data


## Utility tools
### - Finding country and province name with lat, lon  
  - With Google Geocode API. This will need your [GeocodeAPI credential key](https://developers.google.com/maps/documentation/geocoding/get-api-key).  
**file**: `/Province/geo_finder.py`  
**usage**:  
```python
from geo_finder import *
print GeoFinder.FindCountryAndProvinceByLatLon_Real(lat = 13.7563486, lon = 100.4557333)
```
    ```
    [u'Thailand', 'Krung Thep Maha Nakhon']
    ```

    code block outside of a list

- Main list
#     8↴
        code block
# 4↴
    - sub list

#        12↴
            code block
#     8↴
        <!-- --> # can also be used to set highlighting <!-- language: lang-none -->
#        12↴
            second code block
#     8↴
        - sub<sup>2</sup> list

#            16↴
                code block
#        12↴
            - sub<sup>3</sup> list
#                20↴
                    code block
#     8↴
        <!-- -->
#        12↴
            up two list levels