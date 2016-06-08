# TwitGeoSpa
Geospatial analysis and simulation using Twitter data


## Utility tools
### - Finding country and province name with lat, lon  
#### - Using Google Geocode API  
  This will need your [GeocodeAPI credential key](https://developers.google.com/maps/documentation/geocoding/get-api-key).  
**file**: `/Province/geo_finder.py`  
**usage**:
    
```python
from geo_finder import *
print GeoFinder.FindCountryAndProvinceByLatLon_Real(lat = 13.7563486, lon = 100.4557333)
```
    
    ```
    [u'Thailand', 'Krung Thep Maha Nakhon']
    ```

#### - Using Quadtree datastructure of provinces  
  Without regrad of require no internet connection, this method also come with speed of [Quadtree](https://en.wikipedia.org/wiki/Quadtree) search `O(log(n))`. You will need to provide proper quadtree of province in area of your search. See below how to create your own quadtree.  
**file**: `/province/geo_finder.py`
**usage**:  

    ```python
    from geo_finder import *
    geoFinder = GeoFinder('/Province/thailand_province_qtree_struct.csv')
    print geoFinder.FindProvinceByLatLon_Estimate(lat = 13.7563486, lon = 100.4557333)
    ```
    ```
    Bangkok
    ```
    