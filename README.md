# FinGuru AI - Your Personal Money Mentor 💰

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/finguru?style=social)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/react-18%2B-blue.svg)](https://reactjs.org)

## 🎯 Problem Statement

**95% of Indians don't have a financial plan.** Financial advisors charge ₹25,000+ per year and serve only High Net-worth Individuals (HNIs). 

FinGuru is an **AI-powered personal finance mentor** that turns confused savers into confident investors. We make financial planning **as accessible as checking WhatsApp** — instantly, personally, and affordably.

## ✨ Key Features

### 1. 💯 Money Health Score
Get a comprehensive financial wellness score across 6 dimensions in just 5 minutes:
- **Emergency Preparedness**: Do you have enough cash reserves?
- **Insurance Coverage**: Are your financial dependents protected?
- **Investment Diversification**: Is your portfolio well-balanced?
- **Debt Health**: How sustainable is your debt level?
- **Tax Efficiency**: Are you optimizing your tax burden?
- **Retirement Readiness**: Are you on track for retirement?

### 2. 📈 SIP Planner (Systematic Investment Plan)
Generate month-by-month financial roadmaps with:
- Monthly SIP recommendations per goal
- Asset allocation strategies
- Timeline-based investment plans
- Expected return calculations
- Inflation-adjusted targets

### 3. 💼 Tax Optimizer
Upload Form 16 or input salary structure. AI identifies:
- All deductions you're missing (Section 80C, 80D, 80E, 80G)
- Old vs. New tax regime comparison
- HRA optimization strategies
- NPS contribution recommendations
- Tax-saving investments ranked by risk profile
- **Potential annual tax savings: ₹10,000 - ₹2,00,000+**

### 4. 📊 AI Financial Advisor Chat
Ask anything about your finances:
- Investment strategy consultation
- Life event financial planning
- Budget optimization
- Insurance needs assessment
- Debt management guidance
- Retirement planning tips

### 5. 🎯 FIRE Path Planner (Coming Soon)
User inputs:
- Age, income, expenses, existing investments, goals
- AI builds complete financial roadmap including:
  - Emergency fund targets
  - Insurance gaps
  - Tax-saving moves
  - Month-by-month investment plan

### 6. 😊 Life Event Financial Advisor (Coming Soon)
Get personalized advice for:
- Bonus received
- Inheritance planning
- Marriage financial planning
- New baby expenses
- Home purchase
- Career change

## 🏗️ System Architecture

### Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React/Next.js)                │
│  ├─ Dashboard        │  Chat Interface  │  User Profile    │
│  ├─ Money Health     │  Investment Plans │  Tax Analysis    │
│  └─ Onboarding       │  Real-time Charts │  Goal Tracking   │
└────────────┬──────────────────────────────────────────────────┘
             │ HTTP/REST API (Base URL: /api)
             ↓
┌─────────────────────────────────────────────────────────────┐
│              Backend API (FastAPI + Python)                   │
│  ├─ User Routes      │  Financial Routes │  Chat Routes    │
│  ├─ Agent Routes     │  Authentication   │  Data Validation │
│  └─ Webhook Routes   │  Error Handling   │  Logging         │
└────────────┬──────────────────────────────────────────────────┘
             │
    ┌────────┼────────┐
    ↓        ↓        ↓
┌──────┐ ┌──────┐ ┌──────────┐
│ AI   │ │ Data │ │ External │
│Agents│ │Store │ │ Services │
└──────┘ └──────┘ └──────────┘
  │
  ├─ Money Health Agent
  ├─ Financial Planning Agent
  ├─ Tax Optimization Agent
  └─ Risk Analysis Agent

Four Specialized AI Agents (Multi-Agent System):
┌────────────────────────────────────────────┐
│ 💰 Money Health Agent                       │
│ • Financial Wellness Assessment             │
│ • 6-Dimension Scoring                       │
│ • Weakness Identification                   │
│ • Priority Action Recommendations           │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ 📊 Financial Planning Agent                 │
│ • Goal-Based Planning                       │
│ • SIP Calculations                          │
│ • Asset Allocation                          │
│ • Investment Vehicle Recommendations        │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ 💼 Tax Optimization Agent                   │
│ • Tax Regime Comparison                     │
│ • Deduction Identification                  │
│ • Savings Calculation                       │
│ • NPS & Insurance Recommendations           │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│ 🎯 Risk Analysis Agent                      │
│ • Risk Appetite Profiling                   │
│ • Investment Recommendations                │
│ • Portfolio Allocation                      │
│ • Market Volatility Guidance                │
└────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | React 18 + Next.js | Modern, fast UI with SSR |
| **Backend** | FastAPI + Python 3.9+ | High-performance API, async support |
| **AI/LLM** | OpenAI GPT-4 / Gemini | Advanced reasoning and recommendations |
| **Database** | MongoDB / Firebase | Flexible schema for financial data |
| **Authentication** | JWT + NextAuth | Secure user sessions |
| **Charts** | Recharts | Interactive financial visualizations |
| **Styling** | Tailwind CSS | Responsive, modern UI design |
| **State Management** | Zustand | Lightweight state management |
| **Deployment** | Docker + Cloud Run | Scalable containerization |

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- OpenAI API Key (or Gemini API Key)
- MongoDB instance (or Firebase)

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/finguru.git
cd finguru
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Backend `.env` file should contain:**
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
BACKEND_URL=http://localhost:8000
DATABASE_URL=mongodb://localhost:27017/finguru
FRONTEND_URL=http://localhost:3000
```

**Start Backend Server:**
```bash
python -m uvicorn app.main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

#### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Create .env.local file
cp .env.example .env.local

# Edit .env.local
nano .env.local
```

**Frontend `.env.local` should contain:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

**Start Development Server:**
```bash
npm run dev
# or
yarn dev
```

Frontend will be available at: `http://localhost:3000`

## 📖 API Documentation

### Base URL
```
http://localhost:8000/api
```

### User Endpoints

#### Register User
```http
POST /users/register
Content-Type: application/json

{
  "name": "Rahul Gupta",
  "email": "rahul@example.com",
  "age": 32,
  "gender": "M",
  "phone": "+91-98765-43210"
}
```

#### Add Financial Data
```http
POST /users/financial-input
Content-Type: application/json

{
  "user_id": "user_123",
  "monthly_income": 50000,
  "annual_income": 600000,
  "monthly_expenses": 30000,
  "annual_expenses": 360000,
  "existing_savings": 200000,
  "existing_investments": 500000,
  "debt_amount": 100000,
  "emergency_fund_target": 180000,
  "risk_profile": "Moderate"
}
```

### Financial Analysis Endpoints

#### Money Health Score
```http
POST /financial/money-health-score
Content-Type: application/json

{
  "monthly_expenses": 30000,
  "existing_savings": 200000,
  "annual_income": 600000,
  "debt_amount": 100000,
  "existing_investments": 500000,
  "age": 32
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_score": 68,
    "score_breakdown": {
      "emergency_preparedness": 20,
      "insurance_coverage": 15,
      "investment_diversification": 10,
      "debt_health": 12,
      "tax_efficiency": 15,
      "retirement_readiness": 8
    },
    "recommendations": [
      "Build emergency fund to 6 months of expenses",
      "Diversify investments across asset classes",
      "Optimize tax savings through SIP and insurance"
    ]
  }
}
```

#### Tax Analysis
```http
POST /financial/tax-analysis
Content-Type: application/json

{
  "annual_income": 600000,
  "age": 32,
  "sip_annual": 150000,
  "insurance_premium": 50000,
  "health_insurance": 30000,
  "rent_paid": 240000,
  "city": "Bangalore"
}
```

### Chat Endpoints

#### Send Message
```http
POST /chat/chat
Content-Type: application/json

{
  "user_id": "user_123",
  "message": "How much should I invest monthly for retirement?"
}
```

**Response:**
```json
{
  "status": "success",
  "user_id": "user_123",
  "user_message": "How much should I invest monthly for retirement?",
  "assistant_response": "Based on your age and income, I'd recommend investing ₹15,000-20,000 monthly in a combination of equity and debt mutual funds through SIP. This can help you build a corpus of ₹1+ crore by retirement..."
}
```

## 💡 USPs (Winning Edge)

1. **Hyper-Personalized AI Advice**
   - Not generic - tailored to your specific situation, tax bracket, and goals
   - Multi-agent system ensures diverse perspectives

2. **India-Centric Financial Planning**
   - Understands Indian tax laws, investment vehicles, and life events
   - Recommends SIP, NPS, ULIP, Insurance, and other Indian instruments
   - Considers HRA, Section 80C/80D deductions, etc.

3. **Accessible & Affordable**
   - WhatsApp-like simplicity
   - No ₹25,000/year advisor fee
   - Available 24/7

4. **Comprehensive Financial Analysis**
   - 6-dimension Money Health Score
   - Tax savings identification (₹10,000 - ₹2,00,000+ annually)
   - SIP planning with specific recommendations
   - Investment portfolio analysis

5. **Real-Time Guidance**
   - Instant responses to financial questions
   - Life event triggered planning
   - Market-aware recommendations

## 📊 Impact Model

### Quantified Benefits (Conservative Estimates)

#### Scenario: 1,000 Users

| Metric | Impact | Annual Value |
|--------|--------|--------------|
| Average Tax Savings | ₹50,000/user | **₹5 Crore** |
| Better Investment Returns | 2% extra | **₹10 Crore** |
| Time Saved (vs Advisor) | 10 hours/user | Invaluable |
| User Base (Year 1) | 1,000 users | Growing 50%/month |

#### Individual User Impact Example

**User Profile:**
- Age: 32, Salaried
- Annual Income: ₹600,000
- Current Expenses: ₹360,000
- Existing Savings: ₹200,000

**FinGuru Impact (Annual):**
- Tax Savings: ₹50,000 (via 80C max, NPS, HRA optimization)
- Better Investment Returns: ₹30,000 (via SIP optimization + risk profiling)
- Time Saved: 10 hours (vs ₹500/hour advisor)
- **Total Annual Value: ₹80,000+**

### Addressable Market

- **Total Indian Investors**: 14+ Crore
- **Salaried Professionals Needing Help**: 3 Crore
- **Accessible Market (FinFirst)**: 50 Lakh
- **TAM at ₹100/user/month**: ₹600 Crore

## 🎯 Core Features (MVP)

✅ **Implemented:**
1. Money Health Score (6-dimension)
2. SIP Planner with goal-based calculations
3. Tax Optimizer (Old vs New regime)
4. AI Financial Advisor Chat
5. Risk Profile Assessment

🚀 **Coming Soon:**
1. FIRE Path Planner (month-by-month roadmap)
2. Life Event Financial Advisor
3. MF Portfolio X-Ray (CAMS/KFintech upload)
4. Couple's Money Planner
5. Voice & Hindi Support
6. Portfolio Rebalancing Alerts

## 📁 Project Structure

```
finguru/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── money_health_agent.py      # Financial wellness scoring
│   │   │   ├── financial_planning_agent.py # SIP & goal planning
│   │   │   ├── tax_agent.py                # Tax optimization
│   │   │   └── risk_agent.py               # Risk profiling
│   │   ├── models/
│   │   │   ├── user.py                    # User schemas
│   │   │   └── financial.py               # Financial schemas
│   │   ├── routes/
│   │   │   ├── user_routes.py             # User management
│   │   │   ├── financial_analysis_routes.py
│   │   │   ├── agent_routes.py
│   │   │   └── chat_routes.py             # AI chat interface
│   │   ├── main.py                        # FastAPI app
│   │   └── __init__.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── pages/
│   │   ├── index.js                       # Landing page
│   │   ├── dashboard.js                   # Main dashboard
│   │   ├── chat.js                        # Chat interface
│   │   └── api.js                         # API client
│   ├── lib/
│   │   └── api.js                         # API utilities
│   ├── components/
│   │   ├── Header.js
│   │   ├── Sidebar.js
│   │   └── Charts.js
│   ├── package.json
│   ├── next.config.js
│   └── .env.example
│
├── docs/
│   ├── ARCHITECTURE.md                    # System design
│   ├── API_DOCUMENTATION.md               # API reference
│   ├── DEPLOYMENT.md                      # Deployment guide
│   └── PITCH.md                           # Pitch deck notes
│
├── .github/
│   └── workflows/
│       └── deploy.yml                     # CI/CD pipeline
│
├── docker-compose.yml                     # Local development
├── Dockerfile                             # Production deployment
├── README.md                              # This file
└── LICENSE
```

## 🔧 Configuration

### Environment Setup

**Backend Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Model to use (gpt-4 recommended)
- `DATABASE_URL`: MongoDB connection string
- `FRONTEND_URL`: Frontend URL for CORS

**Frontend Variables:**
- `NEXT_PUBLIC_API_URL`: Backend API base URL

## 📱 Usage Examples

### 1. Money Health Score
```python
# Request
POST /api/financial/money-health-score
{
  "age": 32,
  "annual_income": 600000,
  "monthly_expenses": 30000,
  "existing_savings": 200000
}

# Response
{
  "total_score": 68,
  "dimensions": {
    "emergency": 20,
    "insurance": 15,
    "diversification": 10
  }
}
```

### 2. SIP Planning
```python
# Request
POST /api/financial/financial-plan
{
  "user_data": {...},
  "goals": [
    {"name": "House", "amount": 5000000, "year": 2030},
    {"name": "Retirement", "amount": 10000000, "year": 2054}
  ]
}

# Response
{
  "sip_recommendations": {
    "House": {"monthly_sip": 25000, "duration": 72},
    "Retirement": {"monthly_sip": 15000, "duration": 360}
  }
}
```

### 3. Tax Savings
```python
# Request
POST /api/financial/tax-analysis
{
  "annual_income": 600000,
  "sip_annual": 150000
}

# Response
{
  "old_regime_tax": 35000,
  "new_regime_tax": 42000,
  "potential_savings": 50000,
  "recommendations": [...]
}
```

## 💻 Development

### Running Tests
```bash
cd backend
pytest tests/
```

### Code Quality
```bash
# Format code
black app/

# Lint
pylint app/

# Type checking
mypy app/
```

## 🚢 Deployment

### Docker Deployment
```bash
# Build image
docker build -t finguru-backend .

# Run container
docker run -p 8000:8000 --env-file .env finguru-backend
```

### Cloud Deployment (Google Cloud Run)
```bash
# Deploy backend
gcloud run deploy finguru-backend --source .

# Deploy frontend (Vercel)
vercel deploy
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## 📊 Performance & Scalability

- **API Response Time**: < 500ms for most endpoints
- **Concurrent Users**: 10,000+ with Cloud Run auto-scaling
- **Database**: MongoDB with proper indexing for < 100ms queries
- **Chat Response**: ~2-3 seconds (LLM latency)

## 🔐 Security

- JWT authentication for all protected endpoints
- CORS enabled for frontend domain only
- Environment variables for sensitive data
- Rate limiting on chat endpoint (100 req/min per user)
- Data encryption in transit (HTTPS only)
- No sensitive data in logs

## 📞 Support & Contact

- **Email**: support@finguru.ai
- **WhatsApp**: Link to chatbot
- **Twitter**: @FinGuruAI
- **GitHub Issues**: Bug reports & feature requests

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- FastAPI for the backend framework
- React & Next.js for the frontend
- Indian financial community for insights

## 🚀 Future Roadmap

### Q1 2024
- ✅ MVP with Money Health Score
- ✅ Tax Optimizer launch
- ✅ Basic AI Chat

### Q2 2024
- 🔄 FIRE Path Planner
- 🔄 Life Event Advisor
- 🔄 Mobile app (React Native)

### Q3 2024
- 🔲 Voice Support (Hindi + English)
- 🔲 MF Portfolio X-Ray
- 🔲 Couple's Money Planner

### Q4 2024
- 🔲 International expansion (Singapore, UAE)
- 🔲 Advanced ML models for recommendations
- 🔲 Integration with discount brokers

## ⭐ Show Your Support

If you find FinGuru helpful, please star this repository!

---

**Made with ❤️ to make financial planning accessible to every Indian**

**FinGuru - Your Personal Money Mentor 💰**
