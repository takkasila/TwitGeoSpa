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
    
1. This is a numbered list.
2. I'm going to include a fenced code block as part of this bullet:

    ```
    Code
    More Code
    ```

3. We can put fenced code blocks inside nested bullets, too.
   1. Like this:

        ```c
        printf("Hello, World!");
        ```

   2. The key is to indent your fenced block by **(4 * bullet_indent_level)** spaces.
   3. Also need to put a separating newline above and below the fenced block.