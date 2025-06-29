## Technical Decisions

### 1. Database Choice
- **MySQL**: Chosen for production readiness and Docker compatibility
- **SQLModel**: Combines SQLAlchemy ORM with Pydantic validation
- **Connection Pooling**: Configured for efficient DB connections

### 2. Architecture
- **Layered Architecture**:
  - Domain: Pure business models
  - Infrastructure: DB implementations
  - Application: Business logic
  - API: FastAPI endpoints
- **Dependency Injection**: Used for DB sessions

### 3. Authentication & Authorization
- **JWT Implementation**: Using PyJWT for token handling
- **Protected Routes**: Auth dependencies for sensitive endpoints

### 4. Testing
- **pytest**: Test runner with 85% coverage target
- **TestClient**: For API integration tests
- **DB Isolation**: Fresh DB for each test

### 5. Docker Optimization
- **Multi-stage Build**: Smaller production image
- **Health Checks**: DB readiness checks
- **Network Isolation**: Dedicated network for containers

### 6. Error Handling
- **Custom Exceptions**: Domain-specific errors
- **HTTP Exception Mapping**: Convert domain errors to HTTP codes