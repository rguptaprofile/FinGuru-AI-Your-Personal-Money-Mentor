# FinGuru Backend - Python Setup Guide

## Prerequisites
- Python 3.9+
- pip or conda
- Virtual environment tool

## Installation Steps

### 1. Create Virtual Environment
```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. Run Backend
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 5. Access API
- API: http://localhost:8000/api
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure
```
backend/
├── app/
│   ├── agents/               # AI agents
│   ├── models/               # Data models
│   ├── routes/               # API endpoints
│   └── main.py               # FastAPI app
├── requirements.txt
├── .env.example
└── README.md
```

## Available Endpoints
- `POST /api/users/register` - Register new user
- `POST /api/financial/money-health-score` - Get financial wellness score
- `POST /api/financial/tax-analysis` - Tax optimization
- `POST /api/financial/financial-plan` - Create financial plan
- `POST /api/chat/chat` - Chat with AI advisor

For complete API docs, visit http://localhost:8000/docs
