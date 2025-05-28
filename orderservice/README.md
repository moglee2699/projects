# 🛒 OrderService – Spring Boot Microservice

This is a simple Spring Boot microservice named `orderservice` that provides basic shopping basket functionality using in-memory storage. It includes REST endpoints to add, view, and remove items from a basket, and to checkout.

---

## 📦 Features

- ✅ RESTful API Endpoints
- ✅ In-memory HashMap storage (no database)
- ✅ Swagger/OpenAPI Documentation
- ✅ Dockerfile for containerization
- ✅ Kubernetes YAML + Helm Chart for deployment
- ✅ Postman Collection for API testing
- ✅ CI/CD pipeline with GitLab
- ✅ Unit and Cucumber BDD tests

---

## 🚀 API Endpoints

| Method | Endpoint              | Description                 |
|--------|------------------------|-----------------------------|
| POST   | `/basket/add`          | Add an item to the basket   |
| GET    | `/basket/view`         | View all basket items       |
| DELETE | `/basket/remove/{id}`  | Remove an item by ID        |
| POST   | `/checkout`            | Checkout all basket items   |

---

## 📖 Swagger Documentation

Once the application is running, access the API docs at:

🔗 [http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html)

---

## 🧪 Running Locally

### Prerequisites
- Java 17+
- Maven 3+
- Docker (optional)

### Run with Maven

```bash
mvn spring-boot:run
````

---

## 🐳 Docker

### Build Docker Image

```bash
docker build -t orderservice .
```

### Run Docker Container

```bash
docker run -p 8080:8080 orderservice
```

---

## ☸️ Kubernetes Deployment

### Apply Kubernetes Manifest

```bash
kubectl apply -f k8s/orderservice-deployment.yaml
```

### Expose Service

```bash
kubectl expose deployment orderservice --type=LoadBalancer --port=8080
```

---

## ⛵ Helm Chart

Helm chart is located under `charts/orderservice/`.

To deploy with Helm:

```bash
helm install orderservice ./charts/orderservice
```

To uninstall:

```bash
helm uninstall orderservice
```

---

## 🧪 Testing

### Run Unit Tests (Junit)

```bash
mvn test
```

### Run Cucumber Tests

```bash
mvn verify
```

---

## 🔁 GitLab CI/CD Pipeline

The GitLab CI/CD pipeline automates:

* Build
* Unit Tests
* Docker Image Creation
* Optional Kubernetes Deployment

Pipeline file: `.gitlab-ci.yml`

---

## 📬 Postman Collection

A ready-to-use Postman collection and environment file are available in the `/postman` directory.

### Files:

* `orderservice.postman_collection.json`
* `orderservice_environment.postman_environment.json`

### To Test with Postman:

1. Import both files into Postman.
2. Use `orderservice` environment.
3. Hit `Send` on each request to test.

### To Run with Newman (CLI):

```bash
newman run postman/orderservice.postman_collection.json \
  -e postman/orderservice_environment.postman_environment.json
```

---

## 📂 Project Structure

```bash
orderservice/
├── src/
│   ├── main/
│   │   ├── java/com/orderservice/...
│   │   └── resources/
│   │       └── application.properties
│   ├── test/
│   │   ├── java/...
│   │   └── cucumber/
├── postman/
│   ├── orderservice.postman_collection.json
│   └── orderservice_environment.postman_environment.json
├── Dockerfile
├── k8s/
│   └── orderservice-deployment.yaml
├── charts/
│   └── orderservice/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           └── deployment.yaml
├── .gitlab-ci.yml
└── README.md
```

---

## 🙋‍♂️ Contact

For questions, feedback, or contributions — feel free to open an issue or pull request on GitHub.
