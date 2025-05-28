---

# OrderService

A simple Spring Boot microservice for managing shopping baskets and checkout operations.

---

## Features

* Add items to basket (`POST /basket/add`)
* View current basket items (`GET /basket/view`)
* Remove item from basket (`DELETE /basket/remove/{id}`)
* Checkout basket (`POST /checkout`)
* In-memory storage of basket items using `HashMap`
* Swagger API documentation (to be added)

---

## Project Structure

```
orderservice/
├── src/main/java/com/example/orderservice/
│   ├── controller/          # REST controllers
│   ├── model/               # Data models
│   ├── service/             # Business logic
│   └── config/              # Configuration (SwaggerConfig to be added)
├── src/main/resources/
│   └── application.properties
├── Dockerfile              # Docker containerization (to be added)
├── k8s/                    # Kubernetes deployment files (to be added)
├── helm-chart/             # Helm chart for Kubernetes (to be added)
├── pom.xml                 # Maven build file
└── README.md               # This file
```

---

## Getting Started

### Prerequisites

* Java 17 or higher
* Maven 3.6+
* Docker (optional, for containerization)
* Kubernetes & Helm (optional, for deployment)

### Build and Run

```bash
# Build the application
mvn clean package

# Run locally
java -jar target/orderservice-0.0.1-SNAPSHOT.jar
```

### API Documentation

Swagger UI will be available at:
`http://localhost:8080/swagger-ui.html` (once SwaggerConfig is added)

---

## Future Improvements

* Add Swagger configuration for API docs
* Create Dockerfile for containerization
* Add Kubernetes deployment manifests and Helm charts for easy deployment

---

## Author

Abishai Srinivasan
