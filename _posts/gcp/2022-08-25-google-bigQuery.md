---
# layout: static
title:  "Google BigQuery "
date:   2022-08-15 20:04:00
categories: "Spring Microservices"
tags: ["Spring Microservices", Spring Boot, GCP]
---

Once the data is received, convert (serialize) the results data into DTO, using defauklt jackson mapper

```java
private void convertFromBQResponseToDto(BigQueryResponse results, List<BusinessDto> list) {
    if (!CollectionUtils.isEmpty(results.getData())){
        results.getData().forEach(map -> {
            ObjectMapper mapper = new ObjectMapper(); // jackson's object mapper
            mapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false); // it's true by default
            BusinessDto pojo = mapper.convertValue(map, BusinessDto.class);

            list.add(pojo);
        });
    }
}
```

If more control is needed, then individual fields can set adn the naming can be controlled from the DTO

```java
results.getData().forEach(result -> {
            BusinessDto pojo = getBusinessDtoFromMap(result);
                list.add(pojo);
            });
```

```java
private BusinessDto getBusinessDtoFromMap(Map<String, Object> map) {
        BusinessDto pojo = BusinessDto.builder()
                .firstName((String) map.get("FIRST_NAME"))
                .lastName((String) map.get("LAST_NAME"))
                .orderNumber((Long) map.get("ORDER_NUMBER"))
                //Other Fields
                .build();
        return pojo;
    }

```

Dto with much more control
```java

@Data
@Builder
@NoArgsConstructor
//@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
        "firstName",
        "lastName",
        "orderNumber",
})
public class BusinessDto {

    @JsonProperty("firstName")
    private String firstName;
    @JsonProperty("lastName")
    private String lastName;
    @JsonProperty("orderNumber")
    private Long orderNumber;

    @JsonIgnore
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();


    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
    }


```