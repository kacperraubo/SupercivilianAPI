# ArcGIS API Documentation

### Getting shelters within a range of a point

In order to get shelters within a range of a point, we need to append the following query
parameters to the base URL:
- `where` - A `SQL` where clause, which in this cause should be `1=1` because we do not want to filter by any columns on the table.
- `geometryType` - The type of geometry to use for the query. In this case, we use `esriGeometryPoint`, which represents a point.
- `spatialRel` - The spatial relationship to use for the query. In this case, we use `esriSpatialRelIntersects`, which means that the API will return any features that overlap with the point.
- `geometry` - The point to use for the query. This is the point from which we want to search for shelters, in the format `longitude,latitude`.
- `inSR` - The spatial reference of the point. In this case, we use `4326`. See [here](https://spatialreference.org/ref/epsg/4326/) for more information.
- `distance` - The distance within which to search for shelters. This is the radius of the circle within which we want to search for shelters, in meters.
- `units` - The units of the distance. In this case, we use `esriSRUnit_Meter`, which represents meters.
- `outFields` - The fields to return. In this case, we use `*`, which means that the API will return all fields in the table.
- `returnGeometry` - Whether to return the geometry of the features. In this case, we use `true`, which means that the API will return the geometry of the features under the `geometry` field.
- `orderByFields` - The fields to order the results by. In this case, we use `ObjectId2 ASC`, which means that the API will return the results in ascending order of the `ObjectId2` field.
- `resultRecordCount` - The number of results to return. In this case, we use an empty string, which means that the API will return all results.
- `resultType` - The type of results to return. In this case, we use `standard`, which means that the API will return the results in a standard format.
- `multipatchOption` - The option to use for multipatch features. In this case, we use `xyFootprint`, which means that the API will return the results for each part of a multipatch feature.
- `f` - The format of the results to return. In this case, we use `pjson`, which means that the API will return the results in a `json` format.


### Example response

Query:
```
https://services-eu1.arcgis.com/HE4WRthd9CIPj0R8/ArcGIS/rest/services/schrony_csv/FeatureServer/0/query?where=1=1&geometryType=esriGeometryPoint&geometry=21.0122287,52.2296756&inSR=4326&distance=1000&units=esriSRUnit_Meter&outFields=*&returnGeometry=true&f=pjson
```

```json
{
    "objectIdFieldName": "ObjectId2",
    "uniqueIdField": {
        "name": "ObjectId2",
        "isSystemMaintained": true
    },
    "globalIdFieldName": "",
    "geometryType": "esriGeometryPoint",
    "spatialReference": {
        "wkid": 102100,
        "latestWkid": 3857
    },
    "fields": [
        {
            "name": "ObjectID",
            "type": "esriFieldTypeInteger",
            "alias": "ObjectID",
            "sqlType": "sqlTypeInteger",
            "domain": null,
            "defaultValue": null
        },
        {
            "name": "Rodzaj_inw",
            "type": "esriFieldTypeString",
            "alias": "Rodzaj inwentaryzacji",
            "sqlType": "sqlTypeNVarchar",
            "length": 4000,
            "domain": null,
            "defaultValue": null,
            "description": "{\"value\":\"Zasady przerowadzenia spisu z natury. W ramach realizacji spisu powszechnego budowli ochronnych realizowano dwie drogi: a) rozpoznanie z urzędnikiem, b) rozpoznanie operacyjne. \\nAd a) - obiekt widnieje w spisie urzędowym - prace inwentaryzacyjne realizowane przez urzędnika oraz strażaka.\\nAd b) - obiekt traktowany jest jako miejsce doraźnego schronienia - inwentaryzacja realizowana w ramach rozpoznania operacyjnego przez strażaka.\\n\",\"fieldValueType\":\"\"}"
        }
        // ... more fields
    ],
    "features": [
        {
            "attributes": {
                "ObjectID": 215542,
                "Rodzaj_inw": "[1] - Ropoznanie operacyjne",
                "Możliwoś": "[1] - droga pożarowa",
                "Powierzchn": 5000,
                "Pojemnoś_": 3333,
                "Subiektywn": 8,
                "Rodzaj_obi": "[3] - MDS",
                "Przeznacze": "[1] - M",
                "Województ": "MAZOWIECKIE",
                "Powiat": "Warszawa",
                "Adres": "Marszałkowska - Al. Jerozolimskie, 00-693 Warszawa",
                "x": 21.0117278584427,
                "y": 52.2298239083584,
                "ObjectId2": 95948
            },
            "geometry": {
                "x": 2339014.845888682,
                "y": 6841787.716929453
            }
        },
        {
            "attributes": {
                "ObjectID": 202001,
                "Rodzaj_inw": "[1] - Ropoznanie operacyjne",
                "Możliwoś": "[2] - inna droga utwardzona",
                "Powierzchn": 3944,
                "Pojemnoś_": 2629,
                "Subiektywn": 5,
                "Rodzaj_obi": "[3] - MDS",
                "Przeznacze": "[1] - M",
                "Województ": "MAZOWIECKIE",
                "Powiat": "Warszawa",
                "Adres": "Marszałkowska 94/98, 00-510 Warszawa",
                "x": 21.0130293,
                "y": 52.2294616,
                "ObjectId2": 94846
            },
            "geometry": {
                "x": 2339159.7217001375,
                "y": 6841721.868599337
            }
        }
        // ... more features
    ]
}
```
