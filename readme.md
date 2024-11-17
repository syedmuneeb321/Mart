

# **AI Mart Platform**

This project is a multi-service online mart API built using modern **microservices architecture**. Each service runs in its container and communicates asynchronously via Kafka. The services include user management, product catalog, order processing, inventory, payment, and notification systems.

---

## **Services Overview**

1. **Product Service**: Manages product catalog (CRUD operations).
2. **User Service**: Handles user authentication, registration, and profiles.
3. **Order Service**: Processes and tracks customer orders.
4. **Inventory Service**: Manages stock levels and updates inventory.
5. **Payment Service**: Processes local (PayFast) and international (Stripe) payments.
6. **Notification Service**: Sends order-related notifications.

---

## **Architecture Components**

### **Primary Components**
- **Microservices**:
  Each service is built and runs in its container with a dedicated PostgreSQL database.

- **Event-Driven Communication**:
  Uses **Kafka** as the message broker for asynchronous communication.

- **Database**:
  Each service has its own PostgreSQL instance, following the database-per-service pattern.

### **Supporting Components**
- **Kafka UI**: A web interface to monitor and manage Kafka topics and messages.
- **Docker Volumes**: Ensures persistent storage for PostgreSQL databases.
- **Bridge Network**: Connects all containers for seamless communication.

---

## **Setup Instructions**

### **Prerequisites**
Ensure you have the following installed:
- **Docker**
- **Docker Compose**

---

### **How to Run the Platform**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/syedmuneeb321/ai-mart-platform.git
   cd ai-mart-platform
   ```

2. **Start All Services**:
   ```bash
   docker-compose up --build
   ```

3. **Access Kafka UI** (Optional):
   Open Kafka UI at [http://localhost:8080](http://localhost:8080) to monitor Kafka topics and events.

---

## **Service Endpoints**

| **Service**         | **Port** | **Description**                    |
|----------------------|----------|------------------------------------|
| **User Service**     | `8000`   | User management API               |
| **Product Service**  | `8005`   | Product catalog management API    |
| **Order Service**    | `8003`   | Order processing API              |
| **Inventory Service**| `8007`   | Inventory management API          |
| **Payment Service**  | `8008`   | Payment processing API            |
| **Notification**     | `8009`   | Notification system API           |
| **Kafka Broker**     | `9092`   | Message broker for events         |
| **Kafka UI**         | `8080`   | Web interface to manage Kafka     |

---

## **Environment Variables**

Each PostgreSQL service is configured with the following environment variables:
- `POSTGRES_USER=ziakhan`
- `POSTGRES_PASSWORD=my_password`
- `POSTGRES_DB=mydatabase`

---

## **How Services Communicate**

1. **Microservices**:
   Each service communicates with its database and publishes/consumes messages via Kafka.

2. **Event Communication**:
   Kafka handles inter-service messaging. For example:
   - **Order Service** publishes an event when an order is created.
   - **Inventory Service** consumes the event to update stock levels.
   - **Notification Service** sends an order confirmation notification.

3. **JSON for Data Exchange**:
   All services use JSON for message serialization and API responses.

---

## **Docker Compose Overview**

### **Key Configuration**
- **Volumes**:
  Persistent storage is managed for PostgreSQL databases using Docker volumes.
- **Networks**:
  A shared bridge network connects all services.

### **Start Kafka & Services**
To bring up Kafka and all services:
```bash
docker-compose up --build
```

### **Kafka UI**
You can monitor Kafka events at [http://localhost:8080](http://localhost:8080).

---

## **Future Enhancements**
1. Add CI/CD pipelines for automated testing and deployment.
2. Implement centralized logging and monitoring.
3. Scale services dynamically based on traffic.

---
