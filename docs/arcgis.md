# ArcGIS API Documentation

## Base URL

The base URL for the ArcGIS API is:

```
https://services-eu1.arcgis.com/HE4WRthd9CIPj0R8/ArcGIS/rest/services/schrony_csv/FeatureServer/0/query
```

### Getting shelters within a range of a point

In order to get shelters within a range of a point, we need to append the following query
parameters to the base URL:
- `where` - A `SQL` where clause, which in this case should be `1=1` because we do not want to filter by any columns on the table.
- `geometryType` - The type of geometry to use for the query. In this case, we use `esriGeometryPoint`, which represents a point.
- `spatialRel` - The spatial relationship to use for the query. In this case, we use `esriSpatialRelIntersects`, which means that the API will return any features that overlap with the point.
- `geometry` - The point to use for the query. This is the point from which we want to search for shelters, in the format `longitude,latitude`.
- `inSR` - The spatial reference of the point. In this case, we use `4326`. See [here](https://spatialreference.org/ref/epsg/4326/) for more information.
- `distance` - The distance within which to search for shelters. This is the radius of the circle within which we want to search for shelters, in meters.
- `units` - The units of the distance. In this case, we use `esriSRUnit_Meter`, which represents meters.
- `outFields` - The fields to return. In this case, we use `*`, which means that the API will return all fields in the table.
- `returnGeometry` - Whether to return the geometry of the features. In this case, we use `true`, which means that the API will return the geometry of the features under the `geometry` field.
- `orderByFields` - The fields to order the results by. In this case, we use `ObjectID ASC`, which means that the API will return the results in ascending order of the `ObjectID` field.
- `resultRecordCount` - The number of results to return. In this case, we use an empty string, which means that the API will return all results.
- `resultType` - The type of results to return. In this case, we use `standard`.
- `multipatchOption` - The option to use for multipatch features. In this case, we use `xyFootprint`.
- `f` - The format of the results to return. In this case, we use `pjson`.
