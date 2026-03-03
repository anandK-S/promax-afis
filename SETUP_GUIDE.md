# 🚀 Pro-Max AFIS - Setup & Deployment Guide

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 20+** - [Download](https://nodejs.org/)
- **Docker & Docker Compose** - [Download](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download](https://git-scm.com/downloads)
- **PostgreSQL 15+** (if not using Docker)
- **Redis 7.2+** (if not using Docker)

### System Requirements
- **Minimum RAM**: 4GB (8GB recommended)
- **Minimum Storage**: 20GB free space
- **Operating System**: Linux, macOS, or Windows (with WSL2)

---

## 📦 Quick Start with Docker (Recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/promax-afis.git
cd promax-afis
```

### Step 2: Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
nano .env
```

**Critical settings to update:**
- `SECRET_KEY` - Generate with: `openssl rand -hex 32`
- `JWT_SECRET_KEY` - Generate with: `openssl rand -hex 32`
- `DATABASE_URL` - Update if using external PostgreSQL
- `REDIS_URL` - Update if using external Redis

### Step 3: Start All Services

```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 4: Initialize Database

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# Create initial admin user
docker-compose exec backend python -m app.scripts.create_admin_user
```

### Step 5: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Celery Monitor (Flower)**: http://localhost:5555

---

## 💻 Manual Setup (Development)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy environment file
cp ../.env.example .env

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp ../.env.example .env

# Start development server
npm run dev
```

### Start Celery Workers

```bash
cd backend

# Start Celery worker (in terminal 1)
celery -A app.tasks.celery_app worker --loglevel=info

# Start Celery beat scheduler (in terminal 2)
celery -A app.tasks.celery_app beat --loglevel=info
```

---

## 🗄️ Database Setup

### Create PostgreSQL Database (Manual)

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE promax_db;

-- Create user (optional)
CREATE USER promax_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE promax_db TO promax_user;

-- Enable TimescaleDB extension
\c promax_db
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

### Run Migrations

```bash
# From backend directory
alembic upgrade head
```

### Create Initial Admin User

```bash
# Create admin user script
python -m app.scripts.create_admin_user
```

---

## 🔧 Configuration

### Backend Configuration (.env)

```env
# Application
APP_NAME=Pro-Max AFIS
APP_VERSION=1.0.0
ENVIRONMENT=production  # or development
DEBUG=False  # Set to True for development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/promax_db

# Security
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# ML Models
ML_MODEL_PATH=./ml-models/trained_models
WHISPER_MODEL_SIZE=base

# Feature Flags
ENABLE_VOICE_FEATURES=True
ENABLE_ML_PREDICTIONS=True
```

### Frontend Configuration (.env)

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENABLE_VOICE=True
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm test

# Run E2E tests
npm run test:e2e

# Run with coverage
npm run test:coverage
```

---

## 🚢 Production Deployment

### Docker Production Deployment

```bash
# Use production docker-compose file
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/promax-backend
```

### Environment Variables for Production

```env
# SECURITY: Always set these in production
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=use-openssl-rand-hex-32-to-generate
JWT_SECRET_KEY=use-openssl-rand-hex-32-to-generate

# Database: Use strong passwords
DATABASE_URL=postgresql://user:STRONG_PASSWORD@db-host:5432/promax_db

# Redis: Use authentication
REDIS_URL=redis://:REDIS_PASSWORD@redis-host:6379/0

# SSL/TLS: Enable HTTPS
CORS_ORIGINS=https://yourdomain.com
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Check what's using the port
lsof -i :8000  # For backend
lsof -i :3000  # For frontend
lsof -i :5432  # For PostgreSQL
lsof -i :6379  # For Redis

# Kill the process
kill -9 <PID>
```

#### 2. Database Connection Failed

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U postgres -h localhost -p 5432

# Check DATABASE_URL in .env file
```

#### 3. Redis Connection Failed

```bash
# Check Redis is running
redis-cli ping

# Should return: PONG
```

#### 4. Permission Denied

```bash
# Fix file permissions
chmod -R 755 .
chown -R $USER:$USER .

# For Docker
sudo chown -R 1000:1000 ./data
```

#### 5. ML Models Not Loading

```bash
# Download required ML models
cd ml-models
python download_models.py

# Or train models from scratch
python train_models.py
```

---

## 📊 Monitoring & Logging

### View Application Logs

```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Application logs
tail -f backend/logs/app.log

# Celery logs
docker-compose logs -f celery-worker
```

### Monitor with Flower (Celery)

```bash
# Access Flower dashboard
# http://localhost:5555

# Or start Flower manually
celery -A app.tasks.celery_app flower --port=5555
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/api/v1/health

# Frontend health
curl http://localhost:3000

# Database health
docker-compose exec postgres pg_isready
```

---

## 🔒 Security Best Practices

1. **Never commit .env files** to version control
2. **Use strong secrets** - Generate with `openssl rand -hex 32`
3. **Enable HTTPS** in production with SSL certificates
4. **Update dependencies** regularly
5. **Use firewall rules** to restrict access
6. **Enable rate limiting** on API endpoints
7. **Regular backups** of database and data

---

## 📈 Performance Optimization

### Backend Optimization

1. **Database Indexing**: Ensure indexes on frequently queried columns
2. **Redis Caching**: Enable caching for frequently accessed data
3. **Connection Pooling**: Tune database pool size
4. **Async Processing**: Use Celery for long-running tasks
5. **CDN**: Serve static assets via CDN

### Frontend Optimization

1. **Code Splitting**: Lazy load routes and components
2. **Image Optimization**: Compress and optimize images
3. **Bundle Analysis**: Analyze and reduce bundle size
4. **Service Workers**: Enable offline caching
5. **CDN**: Serve assets via CDN

---

## 📞 Support & Resources

### Documentation
- [API Documentation](http://localhost:8000/api/docs)
- [README.md](./README.md)
- [Architecture Guide](./docs/architecture.md)

### Community
- [GitHub Issues](https://github.com/yourusername/promax-afis/issues)
- [Discussions](https://github.com/yourusername/promax-afis/discussions)

### Contact
- Email: support@promax-afis.com
- Documentation: https://docs.promax-afis.com

---

## 🎯 Next Steps

1. **Configure your environment** - Update .env files
2. **Run database migrations** - `alembic upgrade head`
3. **Create admin user** - Run create_admin_user script
4. **Test the application** - Access http://localhost:3000
5. **Deploy to production** - Follow deployment guide
6. **Set up monitoring** - Configure logging and alerts
7. **Customize branding** - Update frontend with your branding

---

**Happy Building! 🚀**

For detailed information, refer to the [README.md](./README.md) file.