# FinGuru AI - Quick Start Guide

## 🚀 Start in 5 Minutes!

### Option 1: Using Docker (Recommended)
```bash
# 1. Install Docker: https://docs.docker.com/get-docker/

# 2. Clone and navigate
cd finguru

# 3. Create .env file
cp backend/.env.example backend/.env

# 4. Add your OpenAI API key to backend/.env
OPENAI_API_KEY=sk-your-api-key-here

# 5. Start everything with one command
docker-compose up

# 6. Open in browser
Backend:  http://localhost:8000 (API Docs at /docs)
Frontend: http://localhost:3000
```

### Option 2: Manual Setup (For Development)

#### Backend Terminal
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Edit .env with your OpenAI API key
# Then run:
python -m uvicorn app.main:app --reload --port 8000
```

#### Frontend Terminal
```bash
cd frontend
npm install
npm run dev

# Open http://localhost:3000
```

---

## 📊 Testing the Application

### Test 1: Money Health Score
```bash
# Browser Method:
curl -X POST http://localhost:8000/api/financial/money-health-score \
  -H "Content-Type: application/json" \
  -d '{
    "age": 32,
    "monthly_expenses": 30000,
    "existing_savings": 200000,
    "annual_income": 600000,
    "debt_amount": 100000,
    "existing_investments": 500000
  }'

# Expected Response:
{
  "status": "success",
  "data": {
    "total_score": 68,
    "score_breakdown": {
      "emergency_preparedness": 20,
      "insurance_coverage": 15,
      ...
    }
  }
}
```

### Test 2: Tax Analysis
```bash
curl -X POST http://localhost:8000/api/financial/tax-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "annual_income": 600000,
    "sip_annual": 150000,
    "insurance_premium": 50000,
    "age": 32
  }'
```

### Test 3: Chat with AI
```bash
curl -X POST http://localhost:8000/api/chat/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_test_123",
    "message": "How much should I invest for retirement?"
  }'
```

---

## 📚 Available Features

### 1. Money Health Score (⭐ Start Here)
- Navigate to Dashboard
- Enter your financial data
- Get instant wellness score across 6 dimensions
- See personalized recommendations

### 2. Tax Analysis
- Input annual income and deductions
- Get old vs new tax regime comparison
- Discover tax-saving opportunities (₹50,000+ potential!)

### 3. Financial Planning
- Set financial goals (House, Car, Retirement, etc.)
- Get SIP recommendations
- View asset allocation strategy

### 4. AI Chat
- Ask any financial question
- Get instant, personalized advice
- See chat history stored for reference

---

## 📁 Project Structure
```
finguru/
├── backend/           # FastAPI + Python (Port 8000)
├── frontend/          # React/Next.js (Port 3000)
├── docs/              # Documentation
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 🔑 Required API Keys

1. **OpenAI API Key** (Required)
   - Get from: https://platform.openai.com/api-keys
   - Add to: `backend/.env` as `OPENAI_API_KEY=sk-...`

2. **MongoDB** (Optional, uses local instance default)
   - For production: https://www.mongodb.com/cloud/atlas
   - Update: `DATABASE_URL` in `.env`

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
python -m uvicorn app.main:app --port 8001
```

### OpenAI API Error
- Check API key is correct
- Verify you have API credits
- Check rate limits

### MongoDB Connection Error
- Ensure MongoDB is running
- Check connection string in .env
- Verify credentials if using MongoDB Atlas

---

## 📖 Full Documentation

- **README.md** - Complete project overview
- **docs/ARCHITECTURE.md** - System design & algorithms
- **docs/IMPLEMENTATION_GUIDE.md** - Building guide
- **docs/DEPLOYMENT.md** - Production deployment
- **backend/README.md** - Backend setup
- **frontend/README.md** - Frontend setup

---

## 🎯 Next Steps

1. ✅ Get OpenAI API key
2. ✅ Start with Docker Compose (one command!)
3. ✅ Test Money Health Score feature
4. ✅ Explore Tax Analysis
5. ✅ Try AI Chat feature
6. ✅ Read full documentation

---

## 💡 Pro Tips

- Use the Swagger UI at `http://localhost:8000/docs` to test APIs
- Frontend has sample data pre-filled (just click "Analyze")
- Chat remembers conversation history per user
- All calculations work offline (LLM for explanations only)

---

**🚀 You're ready to start! Happy coding!**

For help: Check docs/ folder or GitHub Issues
