package com.example.orderservice.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfig {

    @Bean
    public OpenAPI orderserviceOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Order Service API")
                .description("Spring Boot microservice for managing basket and checkout")
                .version("1.0.0"));
    }
}
