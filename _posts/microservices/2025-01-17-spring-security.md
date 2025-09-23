---
categories: Microservices
date: 2024-12-05 15:00:00
tags:
- Spring Boot
title: Spring Security
---

{% include toc title="Index" %}


Spring Security is a framework focused on providing authentication, authorization, and other security features for Java applications.
- Comprehensive support for authentication and authorization.
- Protection against common vulnerabilities (e.g., CSRF, session fixation).
- Integration with OAuth2 for Single Sign-On (SSO).
- Security for REST APIs, including stateless authentication mechanisms like JWT.

`pom.xml`

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

# Authentication vs. Authorization

**Authentication**:
The process of verifying the identity of a user.
- **Example**: Logging in with a username and password.

**Authorization**:
Determines whether an authenticated user has permission to access a resource.
- **Example**: Granting access to the admin dashboard only to users with the `ADMIN` role.


#  Core Components

### 3.1 SecurityContext and SecurityContextHolder
- `SecurityContext`: Holds security information (e.g., authenticated user details).
- `SecurityContextHolder`: A static holder for the `SecurityContext`. Used to access security details programmatically.

### 3.2 Authentication Object
- Represents the principal (user) and their credentials.
- Common implementations: `UsernamePasswordAuthenticationToken`, `OAuth2Authentication`.



## 5. Key Concepts

### 5.1 Filters in Spring Security
The security filter chain intercepts requests and applies security logic.

- `UsernamePasswordAuthenticationFilter`: Handles form-based login.
- `OncePerRequestFilter`: Custom filters can extend this class.

### 5.2 Password Encoding
Always encode passwords before storing them.

Example using `BCryptPasswordEncoder`:
```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
}
```

---

## 6. Common Use Cases

### 6.1 Basic Authentication
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                .anyRequest().authenticated()
                .and()
            .formLogin();
    }
}
```

### 6.2 JWT Authentication
1. Generate a JWT upon successful login.
2. Validate the token for each request.

Key classes:
- `JwtAuthenticationFilter`
- `JwtTokenProvider`

---

## 7. Annotations in Spring Security

### 7.1 `@PreAuthorize` and `@PostAuthorize`
Used for method-level security:

```java
@PreAuthorize("hasRole('ADMIN')")
public void adminMethod() {
    // Code here
}
```

### 7.2 `@Secured`
An alternative to `@PreAuthorize`:

```java
@Secured("ROLE_ADMIN")
public void adminMethod() {
    // Code here
}
```

---

## 8. Handling CSRF
CSRF (Cross-Site Request Forgery) protection is enabled by default.

To disable:
```java
@Override
protected void configure(HttpSecurity http) throws Exception {
    http
        .csrf().disable();
}
```

---

## 9. OAuth2 Integration
Use Spring Security’s OAuth2 support for SSO.

Example configuration:
```properties
spring.security.oauth2.client.registration.google.client-id=your-client-id
spring.security.oauth2.client.registration.google.client-secret=your-client-secret
```

---

## 10. Common Interview Questions

1. Explain the difference between authentication and authorization.
2. How does Spring Security handle CSRF?
3. How do you secure a REST API with JWT in Spring Boot?
4. What is the role of `SecurityContextHolder`?
5. Explain the purpose of `UserDetailsService`.
6. How do you implement role-based access control in Spring Security?
7. What are some best practices for securing a Spring Boot application?

---

## 11. Best Practices

1. Always encode passwords using `PasswordEncoder`.
2. Use HTTPS to encrypt communication.
3. Avoid exposing sensitive endpoints.
4. Implement proper exception handling for security events.
5. Use a security audit tool to identify vulnerabilities.

---

# Security as a Separate Service (API Call)