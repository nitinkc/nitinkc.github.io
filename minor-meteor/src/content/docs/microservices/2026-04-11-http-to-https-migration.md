---
title: Migrating HTTP APIs to HTTPS in Spring Boot - Planning & Implementation
date: 2026-04-11 10:00:00
categories:
- Microservices
tags:
- Spring Boot
- Security
- HTTP
- HTTPS
- API Migration
- Certificates
---

{% include toc title="Index" %}

# Overview

Converting HTTP APIs to HTTPS is one of the most critical security decisions in API management. 
This guide focuses on the **planning, communication, and practical implementation** of HTTP-to-HTTPS migration 
for Spring Boot applications. 

For detailed information on SSL/TLS certificates, keystores, and trust management fundamentals, see the [SSL/TLS Certificates & Trust Management Guide]({% post_url /microservices/2025-09-22-ssl-certificates-keystores-complete-guide %}).

For complete Spring Boot SSL/TLS configuration patterns, see the [Spring Boot SSL/TLS Configuration Guide]({% post_url /microservices/2025-09-22-spring-boot-ssl-tls-configuration %}).

---

# Phase 1: Planning & Assessment

## 1. Impact Analysis Checklist

Before starting migration, assess the following:

| Area | Considerations | Action |
|:-----|:---------------|:-------|
| **API Clients** | How many applications consume this API? | Inventory all consumers |
| **Environment** | Do all environments need migration simultaneously? | Plan staged approach |
| **Certificates** | Do you have valid certificates for all domains? | Procure/generate certs |
| **Backward Compatibility** | Can you maintain HTTP during transition? | Plan dual-port support |
| **Performance** | Will TLS handshake impact latency? | Benchmark and measure |
| **Downtime** | Can the API have scheduled downtime? | Plan rolling deployment |
| **Dependencies** | What downstream services depend on this API? | Update their configurations |
| **Certificates Authority** | Self-signed, internal CA, or public CA? | Determine trust model |


## 3. Decision Points

### Single Port vs. Dual Port Migration

**Dual Port Approach (Recommended for Safety)**
- API runs on both `:8080` (HTTP) and `:8443` (HTTPS)
- Allows gradual client migration
- Lower risk of breaking integrations

**Single Port Approach (Hard Cutover)**
- Only HTTPS on `:8443`
- Requires all clients ready simultaneously
- Higher risk but simpler operations

# Phase 3: Implementation

## Basic Setup: Simple GET API with HTTP and HTTPS

### Step 1: Create a Simple Controller

```java
@RestController
@RequestMapping("/api/v1")
@Slf4j
public class DemoApiController {
    
    @GetMapping("/health")
    public ResponseEntity<ApiResponse> health() {
        return ResponseEntity.ok(new ApiResponse(
            "success", 
            "API is healthy", 
            System.currentTimeMillis()
        ));
    }
    
    @PostMapping("/echo")
    public ResponseEntity<ApiResponse> echo(@RequestBody EchoRequest request) {
        return ResponseEntity.ok(new ApiResponse(
            "success",
            "Echo: " + request.getMessage(),
            System.currentTimeMillis()
        ));
    }
}

@Data
@AllArgsConstructor
class ApiResponse {
    private String status;
    private String message;
    private Long timestamp;
}

@Data
class EchoRequest {
    private String message;
}
```

### Step 2: Configure Dual HTTP/HTTPS Ports (application.yml)

```yaml
# HTTPS Configuration (Primary)
server:
  port: 8443
  ssl:
    enabled: true
    key-store: classpath:keystore.p12
    key-store-password: changeit
    key-store-type: PKCS12
    key-alias: myserver
    protocol: TLS
    enabled-protocols:
      - TLSv1.2
      - TLSv1.3

# HTTP Configuration (Secondary - for migration period)
server:
  tomcat:
    redirect-context-root: false

# Optional: HTTP to HTTPS redirect configuration
spring:
  profiles:
    active: prod

# Logging
logging:
  level:
    org.springframework.security: DEBUG
    javax.net.ssl: DEBUG
```

### Step 3: Enable HTTP-to-HTTPS Redirect with Dual Connectors

```java
@Configuration
public class HttpsRedirectConfig {
    
    /**
     * For migration period: Allow both HTTP and HTTPS
     * HTTP requests to specific paths will redirect to HTTPS
     * This is the recommended approach for safe migration
     */
    @Bean
    public ServletWebServerFactory servletContainer() {
        TomcatServletWebServerFactory tomcat = new TomcatServletWebServerFactory();
        
        // Add HTTP connector that redirects to HTTPS
        tomcat.addAdditionalTomcatConnectors(createHttpConnector());
        
        return tomcat;
    }
    
    /**
     * HTTP Connector - will redirect to HTTPS
     * Port 8080: Available during migration period
     * Will be removed after all clients migrate
     */
    private Connector createHttpConnector() {
        Connector connector = new Connector(TomcatServletWebServerFactory.DEFAULT_PROTOCOL);
        connector.setScheme("http");
        connector.setPort(8080);
        connector.setSecure(false);
        connector.setRedirectPort(8443); // Redirect to HTTPS port
        
        // Optional: Only redirect specific paths
        // Other paths could still be served over HTTP if needed
        
        return connector;
    }
    
    /**
     * Optional: Configure redirect rules if you want selective enforcement
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // For production, enforce HTTPS on all endpoints
        http.requiresChannel()
            .anyRequest()
            .requiresSecure();
        
        return http.build();
    }
}
```

### Step 4: Generate/Import Certificates

#### Option A: Self-Signed Certificate (Development)

```bash
# Generate PKCS12 keystore with self-signed certificate
keytool -genkeypair \
  -alias myserver \
  -keyalg RSA \
  -keysize 2048 \
  -keystore keystore.p12 \
  -storetype PKCS12 \
  -storepass changeit \
  -dname "CN=localhost,OU=Development,O=MyOrg,L=City,ST=State,C=US" \
  -validity 365

# Place in src/main/resources/
```

#### Option B: Use Existing Certificate from CA

```bash
# If you have certificate from CA:
# 1. You'll have: certificate.crt, private-key.key

# Convert to PKCS12 format
openssl pkcs12 -export \
  -in certificate.crt \
  -inkey private-key.key \
  -out keystore.p12 \
  -name myserver \
  -passout pass:changeit

# Place in src/main/resources/
```

# Phase 4: Testing HTTP and HTTPS Endpoints

## Using cURL for Testing

### Test HTTP Endpoint (During Migration)

```bash
# Should return 301 redirect or 200 OK (depending on config)
curl -v http://localhost:8080/api/v1/health

# Follow redirect automatically
curl -L http://localhost:8080/api/v1/health
```

### Test HTTPS Endpoint (Production)

```bash
# Test with self-signed cert (ignore verification)
curl -k -v https://localhost:8443/api/v1/health

# Test with proper certificate verification
curl --cacert truststore.crt https://localhost:8443/api/v1/health
```

### Test POST Request

```bash
# HTTP (during migration)
curl -X POST http://localhost:8080/api/v1/echo \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello from HTTP"}' \
  -L

# HTTPS (self-signed)
curl -k -X POST https://localhost:8443/api/v1/echo \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello from HTTPS"}'
```

## Using Java RestTemplate for Testing

```java
@Service
public class ApiMigrationTest {
    
    private final RestTemplate insecureRestTemplate;
    
    @Autowired
    public ApiMigrationTest(RestTemplate insecureRestTemplate) {
        this.insecureRestTemplate = insecureRestTemplate;
    }
    
    /**
     * Test HTTP endpoint during migration
     */
    public void testHttpEndpoint() {
        String httpUrl = "http://localhost:8080/api/v1/health";
        
        try {
            ResponseEntity<ApiResponse> response = insecureRestTemplate.getForEntity(
                httpUrl,
                ApiResponse.class
            );
            
            System.out.println("HTTP Status: " + response.getStatusCode());
            System.out.println("Response: " + response.getBody());
        } catch (Exception e) {
            System.err.println("HTTP test failed: " + e.getMessage());
        }
    }
    
    /**
     * Test HTTPS endpoint
     */
    public void testHttpsEndpoint() {
        String httpsUrl = "https://localhost:8443/api/v1/health";
        
        try {
            ResponseEntity<ApiResponse> response = insecureRestTemplate.getForEntity(
                httpsUrl,
                ApiResponse.class
            );
            
            System.out.println("HTTPS Status: " + response.getStatusCode());
            System.out.println("Response: " + response.getBody());
        } catch (Exception e) {
            System.err.println("HTTPS test failed: " + e.getMessage());
        }
    }
    
    /**
     * Test POST with payload
     */
    public void testPostEndpoint() {
        String url = "https://localhost:8443/api/v1/echo";
        EchoRequest request = new EchoRequest();
        request.setMessage("Test message");
        
        ResponseEntity<ApiResponse> response = insecureRestTemplate.postForEntity(
            url,
            request,
            ApiResponse.class
        );
        
        System.out.println("POST Response: " + response.getBody());
    }
}
```

---

# Phase 5: Client-Side Migration Guide

## For Downstream Java/Spring Boot Clients

### Before Migration: Verify Dependencies

```xml
<!-- Ensure HTTP client library is available -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<!-- For advanced SSL handling -->
<dependency>
    <groupId>org.apache.httpcomponents</groupId>
    <artifactId>httpclient</artifactId>
</dependency>
```

### Update API Configuration

```yaml
# Before (HTTP)
api:
  base-url: http://api-server:8080

# After (HTTPS)
api:
  base-url: https://api-server:8443
```

### Update RestTemplate Configuration

**Old Code (HTTP)**
```java
@Bean
public RestTemplate restTemplate() {
    return new RestTemplate();
}
```

**New Code (HTTPS with Certificate)**
```java
@Configuration
public class ApiClientConfig {
    
    @Bean
    public RestTemplate restTemplate() throws Exception {
        // For self-signed certificates (development only)
        return createInsecureRestTemplate();
        
        // For production with proper certificates
        // return createSecureRestTemplate();
    }
    
    /**
     * For development/testing with self-signed certificates
     * WARNING: Never use in production!
     */
    private RestTemplate createInsecureRestTemplate() throws Exception {
        TrustStrategy acceptingTrustStrategy = (cert, authType) -> true;
        
        SSLContext sslContext = SSLContexts.custom()
            .loadTrustMaterial(null, acceptingTrustStrategy)
            .build();
        
        SSLConnectionSocketFactory csf = new SSLConnectionSocketFactory(
            sslContext,
            NoopHostnameVerifier.INSTANCE
        );
        
        HttpClient httpClient = HttpClients.custom()
            .setSSLSocketFactory(csf)
            .build();
        
        HttpComponentsClientHttpRequestFactory requestFactory = 
            new HttpComponentsClientHttpRequestFactory(httpClient);
        
        return new RestTemplate(requestFactory);
    }
    
    /**
     * For production with proper certificate validation
     */
    private RestTemplate createSecureRestTemplate() throws Exception {
        // Load server's CA certificate
        KeyStore trustStore = KeyStore.getInstance("PKCS12");
        trustStore.load(
            new FileInputStream("server-truststore.p12"),
            "changeit".toCharArray()
        );
        
        TrustManagerFactory tmf = TrustManagerFactory.getInstance(
            TrustManagerFactory.getDefaultAlgorithm()
        );
        tmf.init(trustStore);
        
        SSLContext sslContext = SSLContext.getInstance("TLSv1.2");
        sslContext.init(null, tmf.getTrustManagers(), null);
        
        SSLConnectionSocketFactory csf = new SSLConnectionSocketFactory(
            sslContext,
            SSLConnectionSocketFactory.getDefaultHostnameVerifier()
        );
        
        HttpClient httpClient = HttpClients.custom()
            .setSSLSocketFactory(csf)
            .build();
        
        HttpComponentsClientHttpRequestFactory requestFactory = 
            new HttpComponentsClientHttpRequestFactory(httpClient);
        
        return new RestTemplate(requestFactory);
    }
}
```

### Add API Client Service

```java
@Service
public class RemoteApiService {
    
    private final RestTemplate restTemplate;
    
    @Value("${api.base-url}")
    private String apiBaseUrl;
    
    public RemoteApiService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }
    
    public ApiResponse callHealth() {
        String url = apiBaseUrl + "/api/v1/health";
        
        try {
            ResponseEntity<ApiResponse> response = restTemplate.getForEntity(
                url,
                ApiResponse.class
            );
            
            return response.getBody();
        } catch (ResourceAccessException e) {
            System.err.println("Connection failed: " + e.getMessage());
            throw new RuntimeException("Failed to connect to remote API", e);
        }
    }
    
    public ApiResponse sendMessage(String message) {
        String url = apiBaseUrl + "/api/v1/echo";
        EchoRequest request = new EchoRequest();
        request.setMessage(message);
        
        ResponseEntity<ApiResponse> response = restTemplate.postForEntity(
            url,
            request,
            ApiResponse.class
        );
        
        return response.getBody();
    }
}
```

# Phase 6: Certificate Management & Expiry Planning

## Certificate Monitoring

```java
@Component
@Slf4j
public class CertificateMonitoring {
    
    @Scheduled(fixedRate = 86400000) // Daily check
    public void checkCertificateExpiry() {
        try {
            KeyStore keyStore = KeyStore.getInstance("PKCS12");
            keyStore.load(
                new FileInputStream("keystore.p12"),
                "changeit".toCharArray()
            );
            
            X509Certificate cert = (X509Certificate) 
                keyStore.getCertificate("myserver");
            
            Date expiryDate = cert.getNotAfter();
            long daysUntilExpiry = 
                (expiryDate.getTime() - System.currentTimeMillis()) 
                / (1000 * 86400);
            
            if (daysUntilExpiry < 30) {
                log.error("Certificate expires in {} days - CRITICAL", daysUntilExpiry);
                // Alert administrators
            } else if (daysUntilExpiry < 90) {
                log.warn("Certificate expires in {} days", daysUntilExpiry);
            } else {
                log.info("Certificate valid for {} days", daysUntilExpiry);
            }
        } catch (Exception e) {
            log.error("Failed to check certificate expiry", e);
        }
    }
}
```

## Renewal Planning

| Timeline | Action |
|:---------|:-------|
| **90 days before** | Request new certificate from CA |
| **30 days before** | Notify all consumers of upcoming renewal |
| **7 days before** | Generate new keystore and coordinate deployment |
| **1 day before** | Final testing with new certificate |
| **On renewal day** | Deploy new keystore, monitor for errors |
| **After renewal** | Verify all clients are still connected |

---

# Common Errors & Troubleshooting

## Error 1: CERTIFICATE_VERIFY_FAILED

**Cause**: Client cannot verify server certificate

**Solution**: 
```java
// Development only: Ignore verification
TrustStrategy acceptingTrustStrategy = (cert, authType) -> true;
SSLContext sslContext = SSLContexts.custom()
    .loadTrustMaterial(null, acceptingTrustStrategy)
    .build();

// Production: Add server certificate to truststore
KeyStore trustStore = KeyStore.getInstance("PKCS12");
trustStore.load(new FileInputStream("truststore.p12"), 
    "password".toCharArray());
```

## Error 2: HOSTNAME_MISMATCH

**Cause**: Certificate hostname doesn't match request hostname

**Solution**:
```java
// Ensure certificate CN matches hostname
// Certificate: CN=api.example.com
// Request: https://api.example.com:8443/api/v1/health ✓

// Wrong: https://api-internal:8443/api/v1/health ✗
// (hostname doesn't match certificate)

// Use hostname verifier
SSLConnectionSocketFactory csf = new SSLConnectionSocketFactory(
    sslContext,
    SSLConnectionSocketFactory.getDefaultHostnameVerifier()
);
```

## Error 3: UNABLE_TO_FIND_VALID_CERTIFICATION_PATH

**Cause**: Certificate chain not trusted

**Solution**:
```bash
# Export server certificate
openssl s_client -connect api-server:8443 -showcerts > cert.pem

# Import to client truststore
keytool -import -alias server-cert -file cert.pem \
  -keystore truststore.p12 -storepass changeit
```

## Error 4: 307 Redirect Loop

**Cause**: HTTP to HTTPS redirect misconfigured

**Solution**:
```yaml
# Ensure ports are different
server:
  port: 8443  # HTTPS
  tomcat:
    redirect-context-root: false

# Create explicit redirect rule
http:
  port: 8080
  redirect-to-https: true
```


For detailed SSL/TLS configuration and advanced topics, see:
- [Spring Boot SSL/TLS Configuration Guide]({% post_url /microservices/2025-09-22-spring-boot-ssl-tls-configuration %})
- [SSL/TLS Certificates & Trust Management Guide]({% post_url /microservices/2025-09-22-ssl-certificates-keystores-complete-guide %})

