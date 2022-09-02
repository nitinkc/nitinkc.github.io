---
# layout: static
title:  "Google GeoCoding API"
date:   2022-08-12 20:04:00
categories: "Spring Microservices"
tags: ["Spring Microservices", Spring Boot, GCP]
---

# Find Latitude and Longitude


Required dependency for accessing the API via Java/Spring

```sh
implementation 'com.google.maps:google-maps-services:2.1.0'
```

[GeoCodingAPI Documentation](https://developers.google.com/maps/documentation/geocoding/requests-geocoding)

```java
public GeocodingResult[] getLatLngFromGeoAPI(String address){
    GeoApiContext context = new GeoApiContext.Builder()
            .apiKey("API KEY")
            .build();

    GeocodingResult[] results = new GeocodingResult[0];
    try {
        results = GeocodingApi.geocode(context, address).await();//pass postal address
    } catch (ApiException | InterruptedException | IOException e ) {
        e.printStackTrace();
    }

    // Invoke .shutdown() after making requests
    context.shutdown();

    return results;
}

```
From the invoking method, extract the latitude and longitude from the GeoCodingResult Array

GeocodingResult -> Geometry -> LatLng -> has double lat & double lng;
USe 
```java
GeocodingResult[] results = getLatLngFromGeoAPI(address);
Gson gson = new GsonBuilder().setPrettyPrinting().create();

 if (results.length != 0) {
    //log.info(address);

    String latitude = gson.toJson(results[0].geometry.location.lat);
    String longitude = gson.toJson(results[0].geometry.location.lng);
 }
```