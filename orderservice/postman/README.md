# Postman Collection for OrderService

This repository contains a Postman collection and environment to test the `orderservice` Spring Boot microservice.

---

## Contents

- **OrderService.postman_collection.json**  
  Collection of API requests for all endpoints with URL variables and headers set.

- **OrderService.postman_environment.json**  
  Environment file containing the `baseUrl` variable (default: `http://localhost:8080`).

---

## Setup Instructions

1. **Import Files in Postman**

   - Open Postman application.
   - Click **Import** (top-left corner).
   - Upload both `OrderService.postman_collection.json` and `OrderService.postman_environment.json`.
   - This imports the API requests and environment variables.

2. **Select Environment**

   - At the top-right of Postman, open the **Environment** dropdown.
   - Choose **Localhost Environment** (sets `baseUrl` to `http://localhost:8080`).

3. **Run Your Service**

   - Start the `orderservice` microservice locally on port `8080`.
   - Ensure it is running before sending requests.

4. **Send Requests**

   - Open the **OrderService** collection.
   - Use requests like:
     - `POST /basket/add` — Add item to basket.
     - `GET /basket/view` — View basket contents.
     - `DELETE /basket/remove/{id}` — Remove item by ID.
     - `POST /checkout` — Checkout basket.

5. **Customize Requests**

   - Edit JSON bodies and URL parameters as needed.
   - The `{{baseUrl}}` variable in URLs will automatically point to your selected environment URL.

---

## Notes

- The environment variable `baseUrl` can be changed to test against other hosts or ports.
- Headers like `Content-Type` and `Accept` are pre-configured in requests.
