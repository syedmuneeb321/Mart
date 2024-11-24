# MART Project

## Purpose

The **MART** project is designed as an e-commerce platform to manage essential business operations such as user management, product management, order processing, inventory tracking, and notifications. 

The project is initially developed using a **monolithic architecture** to solidify core concepts and ensure proper feature implementation before transitioning to a **microservices architecture**. This approach allows flexibility in testing and refining the design without the overhead of distributed systems.

---

## Vision

1. **Build a Modular Monolith**: A well-structured monolithic system focusing on scalability, modularity, and code reusability.
2. **Prepare for Microservices Transition**: Ensure the application is ready to evolve into a microservices architecture, focusing on domain-driven design and loosely coupled modules.
3. **End-to-End E-commerce Solution**: Provide a robust backend capable of handling core e-commerce functionalities with extensibility for future enhancements.

---

## Features

- **User Management**: 
  - Role-based user registration (Admin, Customer, Seller).
  - User data management (name, email, password, etc.).
  
- **Product Management**:
  - Add, update, and manage products, categories, and subcategories.
  - Support for product details such as price, description, brand, and seller information.
  
- **Order Management**:
  - Handle orders and their items.
  - Track order status (Pending, Shipped, Delivered, Cancelled).
  - Payment processing.

- **Inventory Management**:
  - Manage product stocks across warehouses.
  - Track reorder levels and quantities.

- **Notifications**:
  - Notify users about order updates or critical actions.

---

## Technologies Used

- **Backend Framework**: FastAPI (Python)
- **Database**: SQLite (with SQLModel ORM for schema and interaction)
- **Security**: Passlib for password hashing
- **Dependency Management**: Poetry

---

## Directory Structure

```
Mart/
├── src/
│   ├── DB/
│   │   └── db.py               # Database connection and session management
│   ├── Model/
│   │   ├── __init__.py
│   │   └── model.py            # Core models defining database schema
│   ├── Service/
│   │   ├── __init__.py
│   │   └── service.py          # Business logic for operations
│   ├── Utils/
│   │   ├── __init__.py
│   │   └── utils.py            # Utility functions (password hashing, etc.)
│   └── main.py                 # FastAPI application entry point
├── tests/                      # Placeholder for unit tests
│   └── __init__.py
├── mart.db                     # SQLite database file
├── poetry.lock                 # Poetry dependencies lock file
├── pyproject.toml              # Project configurations
└── README.md                   # Documentation (this file)
```

---

## Installation and Setup

### Prerequisites

- Python 3.9+
- Poetry (for dependency management)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/syedmuneeb321/Mart
   cd Mart
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

4. Access the application at:
   ```
   http://127.0.0.1:8000
   ```

---

## Usage

### Database Initialization

The database tables are created automatically when the application starts, using `create_db_and_tables()` in the `DB/db.py` file.

### API Endpoints

#### User Management
- **Register User**: `POST /signup`  
  Allows new users to register with their details and roles.

#### Product Management
- **Add Product**: `POST /add-product`
- **Add Category**: `POST /add-category`
- **Add Sub-Category**: `POST /add-sub-category`
- **Get All Products**: `GET /all-product`

#### Order Management
- **Create Order**: `POST /order`
- **Add Order Items**: `POST /order-items`
- **Process Payment**: `POST /procced-payment`

#### Inventory Management
- **Add Warehouse**: `POST /warehouse`
- **Create Inventory**: `POST /inventory`

---

## Key Design Concepts

### 1. **Monolithic Structure**
   - The project follows a modular monolithic design with clear separation of concerns.
   - It simplifies development and testing at the initial stages.

### 2. **Database Relationships**
   - Well-defined relationships between entities like `User`, `Product`, `Orders`, `OrderItems`, `Inventory`, etc.
   - Designed to maintain data consistency and support complex queries.

### 3. **Transition to Microservices**
   - The project structure and modular code organization ensure that the business logic can be seamlessly migrated to independent microservices.

---

## Future Enhancements

- **Authentication and Authorization**: Add token-based authentication for secure access.
- **Microservices Architecture**: Transition to microservices to achieve scalability and high availability.
- **Performance Optimization**: Introduce caching and indexing for faster query execution.
- **Unit Testing**: Add unit tests for all core functionalities.
- **Frontend Integration**: Develop a web or mobile frontend to interact with the APIs.
- **CI/CD Integration**: Automate deployment pipelines for a smoother development lifecycle.

