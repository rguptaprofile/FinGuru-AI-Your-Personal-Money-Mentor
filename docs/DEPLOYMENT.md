# FinGuru - Deployment Guide

## 🌐 Deployment Options

### Option 1: Local Development (Perfect for Testing)

#### Quick Start
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python -m uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

---

### Option 2: Docker Deployment (Production-Ready)

#### Build & Run with Docker

**1. Build Docker Image**
```bash
cd backend
docker build -t finguru-backend:latest .
```

**2. Create docker-compose.yml**
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
    volumes:
      - mongo-data:/data/db

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=mongodb://admin:password123@mongodb:27017/finguru
      - FRONTEND_URL=http://localhost:3000
    depends_on:
      - mongodb
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api
    depends_on:
      - backend

volumes:
  mongo-data:
```

**3. Run with Docker Compose**
```bash
docker-compose up -d
# Access: http://localhost:3000
```

---

### Option 3: Vercel + Google Cloud Run (Production)

#### Step 1: Deploy Frontend (Vercel)

**1. Push code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/finguru.git
git push -u origin main
```

**2. Deploy to Vercel**
- Go to https://vercel.com
- Click "Import Project"
- Select your GitHub repository
- Configure environment variables:
  ```
  NEXT_PUBLIC_API_URL=https://your-backend.cloudrrun.app/api
  ```
- Click "Deploy"

#### Step 2: Deploy Backend (Google Cloud Run)

**1. Setup Google Cloud Account**
```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project your-project-id
```

**2. Create Dockerfile**
```dockerfile
FROM python:3.9

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**3. Build & Push to Container Registry**
```bash
# Build image
docker build -t gcr.io/your-project-id/finguru-backend:latest .

# Push to Google Container Registry
docker push gcr.io/your-project-id/finguru-backend:latest
```

**4. Deploy to Cloud Run**
```bash
gcloud run deploy finguru-backend \
  --image gcr.io/your-project-id/finguru-backend:latest \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-...,DATABASE_URL=mongodb+srv://... \
  --allow-unauthenticated
```

**5. Update Vercel Configuration**
- Update `NEXT_PUBLIC_API_URL` in Vercel to your Cloud Run URL

---

### Option 4: AWS Deployment (Alternative)

#### Backend on AWS Lambda

```bash
# Requirements
pip install zappa

# Deploy
zappa init
zappa deploy production

# Update API endpoint  
zappa update production
```

#### Frontend on AWS Amplify

```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize
amplify init

# Deploy
amplify publish
```

---

## 🗄️ Database Setup

### MongoDB Atlas (Cloud MongoDB)

**1. Create Account**
- Go to https://www.mongodb.com/cloud/atlas
- Sign up for free tier

**2. Create Cluster**
- Click "Create Database"
- Select M0 (Free tier)
- Choose region
- Create cluster (5-10 minutes)

**3. Get Connection String**
- Click "Connect"
- Select "Connect your application"
- Copy connection string: `mongodb+srv://username:password@cluster.mongodb.net/finguru`

**4. Update Backend .env**
```
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/finguru
```

### MongoDB Indexes (For Performance)

```javascript
// In MongoDB Atlas, run these indexes:

db.users.createIndex({ "email": 1 }, { unique: true })
db.financial_data.createIndex({ "user_id": 1 })
db.goals.createIndex({ "user_id": 1, "created_at": -1 })
db.chat_history.createIndex({ "user_id": 1, "created_at": -1 })
```

---

## 🔐 Environment Variables

### Backend (.env)
```
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Database
DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/finguru
DB_NAME=finguru

# URLs
BACKEND_URL=https://finguru-backend.cloudrrun.app
FRONTEND_URL=https://finguru.vercel.app

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256

# Environment
ENVIRONMENT=production
DEBUG=False
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://finguru-backend.cloudrrun.app/api
NEXT_PUBLIC_APP_NAME=FinGuru
```

---

## 🔍 Health Checks

### Verify Backend is Running
```bash
curl http://localhost:8000/health
# Response: { "status": "healthy", "service": "FinGuru Backend" }

curl http://localhost:8000/docs
# Opens Swagger API documentation
```

### Verify Frontend is Running
```bash
curl http://localhost:3000
# Returns HTML of landing page
```

---

## 🚨 Common Issues & Fixes

### MongoDB Connection Error
```
Error: "Failed to connect to MongoDB"

Solution:
1. Check DATABASE_URL is correct
2. Whitelist your IP in MongoDB Atlas
3. Verify username/password
4. Check network connectivity
```

### OpenAI API Error
```
Error: "Invalid API Key"

Solution:
1. Regenerate API key from platform.openai.com
2. Ensure API key has proper permissions
3. Check rate limits (if exceeded, wait 1 minute)
```

### CORS Error
```
Error: "Access to XMLHttpRequest has been blocked by CORS policy"

Solution:
1. Check FRONTEND_URL in backend .env
2. Ensure CORS middleware is enabled
3. Update CORS origins if needed
```

### Port Already in Use
```
Error: "Address already in use"

Solution:
# Find process using port 8000
lsof -i :8000
#
Kill it
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

---

## 📊 Monitoring & Logging

### View Logs (Cloud Run)
```bash
gcloud run logs read finguru-backend --limit 50
```

### Setup Error Tracking (Sentry)
```python
# In app/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### Database Monitoring (MongoDB Atlas)
- Dashboard shows performance metrics
- Query performance insights
- Backup status
- Connection activity

---

## 🔄 CI/CD Pipeline

### GitHub Actions (Automated Deployment)

**Create .github/workflows/deploy.yml:**
```yaml
name: Deploy FinGuru

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build and deploy backend
      run: |
        docker build -t finguru-backend .
        docker push gcr.io/${{ secrets.GCP_PROJECT }}/finguru-backend
        gcloud run deploy finguru-backend --image gcr.io/${{ secrets.GCP_PROJECT }}/finguru-backend
    
    - name: Deploy frontend
      run: |
        cd frontend
        npm install
        npm run build
        vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

---

## ✅ Production Checklist

- [ ] Database backups configured
- [ ] SSL/HTTPS enabled
- [ ] Environment variables secured (not in code)
- [ ] Rate limiting enabled
- [ ] Logging & monitoring setup
- [ ] CI/CD pipeline configured
- [ ] Load testing completed
- [ ] Disaster recovery plan ready
- [ ] Security audit completed
- [ ] Documentation updated

---

## 📱 Testing Deployment

### Test Money Health Score
```bash
curl -X POST http://localhost:8000/api/financial/money-health-score \
  -H "Content-Type: application/json" \
  -d '{
    "monthly_expenses": 30000,
    "existing_savings": 200000,
    "annual_income": 600000,
    "debt_amount": 100000,
    "existing_investments": 500000,
    "age": 32
  }'
```

### Test Chat
```bash
curl -X POST http://localhost:8000/api/chat/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "message": "How much should I invest monthly?"
  }'
```

---

## 🎯 Performance Targets

| Metric | Target | How to Monitor |
|--------|--------|----------------|
| API Response Time | < 500ms | Cloud Run metrics |
| Chat Response | < 3s | Application logs |
| Uptime | 99.5% | Cloud Run status |
| Error Rate | < 0.1% | Sentry/Cloud Logging |
| Peak Users | 10,000+ | Load testing |

---

## 📞 Support & Troubleshooting

- **Documentation**: Check docs/ folder
- **API Docs**: `/docs` endpoint
- **Issues**: Report on GitHub
- **Email**: support@finguru.ai

---

**Successfully Deployed! Your FinGuru backend is now running.** 🚀
