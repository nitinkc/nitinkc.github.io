---
title:  "Rest Template"
date:   2024-03-06 00:45:00
categories: [Microservices]
tags: [Spring Microservices, CRUD]
---

{% include toc title="Index" %}

Both Uri Variables and Request Entities are maps


# With UriVariables
The Uri variables needed for call like `https://api.datamuse.com/words?ml={word}&max={max}`

```java
Map<String, String> uriVariables = new HashMap<>();
uriVariables.put("word", (String) requestBody.get("word"));
uriVariables.put("max", (String) requestBody.get("max"));
```

## GET .getForEntity 

```java
ResponseEntity<WordResponse[]> response = 
        restTemplate.getForEntity(
                URL, 
                WordResponse[].class, 
                uriVariables);
```

## .exchange with Uri variables

```java
HttpHeaders headers = new HttpHeaders();
headers.setContentType(MediaType.APPLICATION_JSON);
//HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(requestBody, headers);//Not needed for uri variable type

ParameterizedTypeReference<WordResponse[]> responseType = new ParameterizedTypeReference<WordResponse[]>() {};
ResponseEntity<WordResponse[]> response = restTemplate.exchange(
        DATA_MUSE_URL_NEEDING_URI_VARIABLES, 
        HttpMethod.GET,
        null,       //RequestEntity/body is not needed, but the path params in the form of uriVariables
        responseType, 
        uriVariables);//Uri variables are needed when the URL needs
```


# With request entity
Create request header with the Request body/entity which is a map and is collected from the method parameter
```java
public List<String> getData(@RequestBody Map<String,Object> requestBody){ ... }
```

HTTP Entity is created with the headers and request body.
```java
HttpHeaders headers = new HttpHeaders();
headers.setContentType(MediaType.APPLICATION_JSON);

HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(requestBody, headers);
```

## POST with `ParameterizedTypeReference`

```java
// Create parameterized type reference for Map<String, Object>
ParameterizedTypeReference<Map<String, Object>> responseType = 
        new ParameterizedTypeReference<Map<String, Object>>() {};

// Send the POST request to the server
ResponseEntity<Map<String, Object>> responseEntity = restTemplate.exchange(
        URL, 
        HttpMethod.POST,
        requestEntity,
        responseType);
```

# Upload a file

```java
private RestTemplate restTemplate;

public Map<String, Object> uploadFile(MultipartFile file, HttpHeaders headers){

    FileMetadata fileMetadata = new FileMetadata(file);

    // Create the request body with multipart data
    MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
    body.add("file", fileMetadata);

    // Set the headers
    headers.setContentType(MediaType.MULTIPART_FORM_DATA);

    // Create the request entity with body and headers
    HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

    // Create parameterized type reference for Map<String, Object>
    ParameterizedTypeReference<Map<String, Object>> responseType = new ParameterizedTypeReference<Map<String, Object>>() {};

    // Send the POST request to the server
    ResponseEntity<Map<String, Object>> responseEntity =
            restTemplate.exchange(URL2, HttpMethod.POST,
                    requestEntity,responseType);

    // Extract and return the response body
    Map<String, Object> responseBody = responseEntity.getBody();
    if (responseBody != null) {
        // Assuming the response contains a list of strings under the key "result"
        return responseBody;
    } else {
        // Handle the case where the response body is null
        return null;
    }
}
```