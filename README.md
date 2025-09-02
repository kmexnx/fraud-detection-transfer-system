# Fraud Detection Transfer System

A sophisticated fraud detection and money transfer system built with **Python**, **FastAPI**, **PostgreSQL**, **Redis**, and deployed with **Docker** and **Kubernetes**.

## 🚀 Features

### Core Features
- **User Management**: Secure user registration, authentication, and profile management
- **Money Transfers**: Internal and external transfer capabilities
- **Real-time Fraud Detection**: ML-powered fraud analysis with multiple detection algorithms
- **Risk Assessment**: Behavioral analysis and risk scoring
- **Transfer Velocity Monitoring**: Rate limiting and suspicious activity detection
- **Audit Trail**: Comprehensive logging and fraud reporting

### Technical Features
- **Async/Await**: High-performance async operations with SQLAlchemy and FastAPI
- **Redis Caching**: Fast data retrieval and session management
- **Machine Learning**: Isolation Forest algorithm for anomaly detection
- **Database Migrations**: Alembic for database schema management
- **Containerization**: Docker and Docker Compose for easy deployment
- **Kubernetes Ready**: Production-ready Kubernetes manifests
- **Comprehensive Testing**: Unit tests and integration tests
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   PostgreSQL    │    │      Redis      │
│                 │◄──►│                 │    │                 │
│ • Authentication│    │ • Users         │    │ • Sessions      │
│ • Transfers     │    │ • Transfers     │    │ • Rate Limits   │
│ • Fraud API     │    │ • Fraud Reports │    │ • Cache         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│  Fraud Service  │    │   ML Models     │
│                 │◄──►│                 │
│ • Risk Analysis │    │ • Isolation     │
│ • Pattern Match │    │   Forest        │
│ • Behavior Scan │    │ • Anomaly Det   │
└─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Poetry or pip
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+
- Kubernetes (optional, for production deployment)

## 🛠️ Installation

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/kmexnx/fraud-detection-transfer-system.git
   cd fraud-detection-transfer-system
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the services**
   ```bash
   # Production
   docker-compose up -d
   
   # Development (includes admin tools)
   docker-compose --profile dev up -d
   ```

4. **Access the application**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Adminer (DB): http://localhost:8080
   - Redis Commander: http://localhost:8081

### Option 2: Local Development

1. **Clone and setup**
   ```bash
   git clone https://github.com/kmexnx/fraud-detection-transfer-system.git
   cd fraud-detection-transfer-system
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   poetry shell
   ```

3. **Setup environment**
   ```bash
   cp .env.example .env
   # Configure your database and Redis URLs
   ```

4. **Setup database**
   ```bash
   # Run migrations
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Option 3: Kubernetes Deployment

1. **Build and push Docker image**
   ```bash
   docker build -t fraud-detection-app:latest .
   docker tag fraud-detection-app:latest your-registry/fraud-detection-app:latest
   docker push your-registry/fraud-detection-app:latest
   ```

2. **Deploy to Kubernetes**
   ```bash
   # Create namespace
   kubectl apply -f kubernetes/namespace.yaml
   
   # Apply configurations
   kubectl apply -f kubernetes/configmap.yaml
   kubectl apply -f kubernetes/secret.yaml
   
   # Deploy services
   kubectl apply -f kubernetes/postgres-deployment.yaml
   kubectl apply -f kubernetes/redis-deployment.yaml
   kubectl apply -f kubernetes/app-deployment.yaml
   
   # Setup ingress and scaling
   kubectl apply -f kubernetes/ingress.yaml
   kubectl apply -f kubernetes/hpa.yaml
   kubectl apply -f kubernetes/network-policy.yaml
   ```

## 📚 API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/token` - Login and get access token
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout user

#### Transfers
- `POST /api/v1/transfers` - Create new transfer
- `GET /api/v1/transfers` - List user transfers
- `GET /api/v1/transfers/{id}` - Get transfer details
- `GET /api/v1/transfers/stats/summary` - Get transfer statistics

#### Fraud Detection
- `POST /api/v1/fraud/analyze` - Analyze transfer for fraud
- `GET /api/v1/fraud/reports` - Get fraud reports
- `GET /api/v1/fraud/risk-score` - Get user risk score
- `GET /api/v1/fraud/stats` - Get fraud statistics

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:password@localhost:5432/fraud_detection` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `SECRET_KEY` | JWT secret key | `your-super-secret-key-change-this-in-production` |
| `FRAUD_SCORE_THRESHOLD` | Fraud detection threshold (0-1) | `0.7` |
| `MAX_DAILY_TRANSFER_AMOUNT` | Maximum daily transfer limit | `10000.0` |
| `MAX_TRANSFER_FREQUENCY` | Max transfers per hour | `10` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | `30` |

### Fraud Detection Configuration

The system uses multiple fraud detection mechanisms:

1. **Amount Analysis**: Checks for unusually high amounts
2. **Velocity Analysis**: Monitors transfer frequency and limits
3. **Behavioral Analysis**: Analyzes user behavior patterns
4. **Pattern Matching**: Identifies known fraud patterns
5. **Machine Learning**: Uses Isolation Forest for anomaly detection

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
poetry install --with dev

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_transfers.py

# Run with verbose output
pytest -v
```

### Test Categories

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test API endpoints and database operations
- **Fraud Detection Tests**: Test fraud analysis algorithms
- **Authentication Tests**: Test security and JWT handling

### Test Data

The system includes fixtures and factories for creating test data:
- User factories for different user types
- Transfer factories for various scenarios
- Fraud pattern fixtures
- Mock ML models for testing

## 🚦 Health Checks

The application provides health check endpoints:

- `GET /health` - Overall system health
- `GET /` - Basic API status

Health checks verify:
- Database connectivity
- Redis connectivity
- Application status

## 📊 Monitoring and Logging

### Logging

The application uses `loguru` for structured logging:

- **Request/Response logging**: All API calls are logged
- **Fraud detection logging**: Detailed fraud analysis logs
- **Error tracking**: Comprehensive error logging with stack traces
- **Performance metrics**: Request duration and system metrics

### Metrics

Key metrics tracked:
- Transfer volumes and frequencies
- Fraud detection rates
- API response times
- System resource usage
- User activity patterns

## 🔒 Security Features

### Authentication & Authorization
- JWT-based authentication
- Token blacklisting on logout
- Password hashing with bcrypt
- Rate limiting on authentication endpoints

### Fraud Prevention
- Real-time transaction monitoring
- Machine learning anomaly detection
- Behavioral analysis
- Geographic anomaly detection
- Velocity checking (time-based limits)

### Data Protection
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- CORS configuration
- Environment variable security

## 🚀 Production Deployment

### Docker Production Tips

1. **Multi-stage builds**: Optimize Docker image size
2. **Health checks**: Enable container health monitoring
3. **Resource limits**: Set appropriate CPU/memory limits
4. **Logging**: Configure centralized logging
5. **Secrets management**: Use proper secret management

### Kubernetes Production

1. **Resource Management**:
   ```yaml
   resources:
     requests:
       memory: "256Mi"
       cpu: "250m"
     limits:
       memory: "512Mi"
       cpu: "500m"
   ```

2. **Auto-scaling**: HPA configured for CPU and memory
3. **Network Policies**: Restrict inter-pod communication
4. **Persistent Storage**: PVC for database and ML models
5. **TLS/SSL**: Ingress with TLS termination

## 📈 Performance Optimization

### Database Optimization
- Proper indexing on frequently queried columns
- Connection pooling with SQLAlchemy
- Async database operations
- Query optimization and analysis

### Caching Strategy
- Redis for session management
- Rate limiting data caching
- User behavior caching
- ML model result caching

### API Performance
- Async/await throughout the application
- Connection pooling
- Request/response compression
- Pagination for large datasets

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install development dependencies:
   ```bash
   poetry install --with dev
   ```
4. Run tests: `pytest`
5. Check code quality: `black . && isort . && flake8`
6. Commit changes with descriptive messages
7. Create a pull request

### Code Style

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing framework

### Commit Convention

Follow conventional commits:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `test:` test additions/changes
- `refactor:` code refactoring

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

1. **Documentation**: Check this README and API docs
2. **Issues**: Create a GitHub issue for bugs or feature requests
3. **Discussions**: Use GitHub Discussions for questions

## 🗺️ Roadmap

### Upcoming Features

- [ ] Advanced ML models (Random Forest, Neural Networks)
- [ ] Real-time notifications and alerts
- [ ] Enhanced geographic fraud detection
- [ ] Mobile app API enhancements
- [ ] Blockchain transaction verification
- [ ] Advanced analytics dashboard
- [ ] Multi-currency support
- [ ] Third-party fraud service integration

### Performance Improvements

- [ ] Database sharding strategies
- [ ] Enhanced caching mechanisms
- [ ] GraphQL API option
- [ ] Microservices architecture
- [ ] Event-driven architecture with message queues

---

## 📊 System Statistics

After deployment, you can monitor:

- **Transfer Success Rate**: ~99.5% (target)
- **Fraud Detection Accuracy**: ~95% (target)
- **API Response Time**: <200ms (target)
- **System Uptime**: 99.9% (target)

---

Built with ❤️ using FastAPI, PostgreSQL, Redis, and modern Python practices.
