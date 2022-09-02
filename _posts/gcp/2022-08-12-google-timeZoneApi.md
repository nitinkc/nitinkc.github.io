---
# layout: static
title:  "Google TimeZone API"
date:   2022-08-15 20:04:00
categories: "Spring Microservices"
tags: ["Spring Microservices", Spring Boot, GCP]
---

# Find Latitude and Longitude


Required dependency for accessing the API via Java/Spring

```sh
implementation 'com.google.maps:google-maps-services:2.1.0'
```

[TimeZone API Documentation](https://developers.google.com/maps/documentation/timezone/requests-timezone)

[Github project](https://github.com/googlemaps/google-maps-services-java)

```java
public TimeZone getTimeZone(Pair<String,String> latLng){
        //Find timezone from TimeZoneAPI
        GeoApiContext context = new GeoApiContext.Builder()
                .apiKey("API KEY")
                .build();
        LatLng location = new LatLng(Double.valueOf(latLng.getLeft()), Double.valueOf(latLng.getRight()));
        TimeZone tz = null;
        try {
            tz = TimeZoneApi.getTimeZone(context, location).await();
        } catch (ApiException | InterruptedException | IOException e) {
            e.printStackTrace();
        }
        return tz;
    }

```
From the invoking method, the response can be collected with java.util.TimeZone

```java
//Time Zone from Google
TimeZone timeZone = getTimeZone(Pair.of(latitude, longitude));
System.out.prinln(timeZone.getID());
System.out.prinln(timeZone.getDisplayName());
```

### Known Issues

Returning wrong timezone info for places near timezone border
[https://stackoverflow.com/questions/55941600/google-time-zone-api-returned-wrong-time-zone-info-for-lat-long](https://stackoverflow.com/questions/55941600/google-time-zone-api-returned-wrong-time-zone-info-for-lat-long)

## Alternate Node js API's for TimeZone

[https://npm.io/package/tz-lookup](https://npm.io/package/tz-lookup)
```js
var tzlookup = require("tz-lookup");

console.log(tzlookup(42.7235, -73.6931)); // prints "America/New_York"
```


[https://www.npmjs.com/package/geo-tz](https://www.npmjs.com/package/geo-tz)
```javascript
const { find } = require('geo-tz')

    console.log(find(47.650499, -122.350070))  // ['America/Los_Angeles']
```

