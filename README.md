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