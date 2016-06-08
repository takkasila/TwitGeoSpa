# TwitGeoSpa
Geospatial analysis and simulation using Twitter data


## Utility tools
- ### Finding country and province name with lat, lon  
  - #### Using Google Geocode API  
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

  - #### Using Quadtree datastructure of provinces  
    Without regrad of require no internet connection, this method also come with speed of [Quadtree](https://en.wikipedia.org/wiki/Quadtree) search `O(log(n))`. You will need to provide proper quadtree of province in area of your search. See [below](https://github.com/takkasila/TwitGeoSpa#quadtree) on how to create your own quadtree.  
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

- ### Quadtree  
  ![](https://raw.githubusercontent.com/takkasila/TwitGeoSpa/master/QGIS/Thailand_provinces_qtree.png)  
  **file**: `/Province/quad_tree.py`  
  Above is a render of quadtree of provinces in Thailand `/Province/thailand_province_qtree_struct.csv` with scan area of 10 km square. There are two steps on creating your own quadtree.  

  1. #### Scan  
      **file**: `/Province/province_grid.py`  
      Insert latitude and longitude of area you want to scan in rectangular form. This process might take a lot of time depends on how precise you want your quadtree will be (scan grid size), how large you want to cover and how fast your internet is (because we're using Geocode API). This will result grid of provinces in csv form `/Provinces/GridProvinces.csv`

  2. #### Read and Export
      **file**: `/Province/province_qtree.py`  
      Input your result of scanning province grids from the first step. Then program will result quadtree file datastructure contains node and edge of tree in csv format `/Province/thailand_province_qtree_struct.csv`. For general use, export format can be found in `/Province/quad_tree.py`.

