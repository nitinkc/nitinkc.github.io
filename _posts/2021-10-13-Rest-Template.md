]

HttpHeaders httpsHeaders = new HttpHeaders();
httpsHeaders.setContentType(MediaType.APPLICATION_JSON_UTF8);

HttpEntity<Object> httpEntity = new HttpEntity<>(requestDTO, httpsHeaders);

String url = "any/{parameterized}/url";
MyDto result = restTemplate.exchange(url,
                HttpMethod.POST, httpEntity, new ParameterizedTypeReference<MyDto>(){}).getBody();


Scenario : PUT save data into a DB by calling a microservice Synchronously with the data on the HTTP Request Body
