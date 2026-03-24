# FinGuru Architecture Document

## 1. System Design Overview

FinGuru is built on a **multi-agent AI architecture** with a modern full-stack web application. The system processes user financial data through specialized AI agents and returns personalized recommendations.

### High-Level Architecture

```
User Interface Layer (React/Next.js)
        ↓
API Gateway (FastAPI)
        ↓
Multi-Agent System
        ├── Money Health Agent
        ├── Financial Planning Agent
        ├── Tax Optimization Agent
        └── Risk Analysis Agent
        ↓
Orchestration Layer
        ↓
LLM Integration (OpenAI GPT-4)
        ↓
Data Layer (MongoDB)
```

## 2. Multi-Agent System

### 2.1 Money Health Agent
**Purpose**: Calculate comprehensive financial wellness score

**Inputs**:
- Monthly expenses
- Emergency fund
- Annual income
- Debt amount
- Existing investments
- Age

**Calculation Methods**:
1. Emergency Preparedness = (Emergency Fund / (Monthly Expenses × 6)) × 20
2. Insurance Coverage = (Income / 100,000) × 20
3. Investment Diversification = Portfolio analysis × 20
4. Debt Health = (1 - Debt/Income ratio) × 20
5. Tax Efficiency = Deduction utilization × 20
6. Retirement Readiness = (Investments / Required Corpus) × 20

**Output**:
```json
{
  "total_score": 68,
  "score_breakdown": {
    "emergency_preparedness": 20,
    "insurance_coverage": 15,
    "investment_diversification": 10,
    "debt_health": 12,
    "tax_efficiency": 15,
    "retirement_readiness": 8
  },
  "priority_actions": ["...", "...", "..."]
}
```

### 2.2 Financial Planning Agent
**Purpose**: Create SIPs, asset allocation, and financial roadmaps

**Algorithm**:
```
For each goal:
  FV = Target Amount
  Rate = Expected Return (12% p.a.)
  Years = Target Year - Current Year
  
  Monthly SIP = FV / [((1 + Monthly Rate)^n - 1) / Monthly Rate]
  
  Allocate SIP % of income:
    > 30% income = Not feasible, reduce target
    15-30% = Good SIP rate
    < 15% = Achievable easily
```

**Asset Allocation Logic**:
```
Base Allocation by Risk:
- Conservative: 30% Equity, 50% Debt, 10% Gold, 10% Cash
- Moderate: 60% Equity, 25% Debt, 10% Gold, 5% Cash
- Aggressive: 80% Equity, 10% Debt, 5% Gold, 5% Cash

Age Adjustment Factor = (60 - Age) / 30
Adjusted Equity = Base Equity × (0.8 + 0.2 × Age Factor)
```

**Output**:
```json
{
  "sip_recommendations": {
    "House": {"monthly_sip": 25000, "duration": 72},
    "Retirement": {"monthly_sip": 15000, "duration": 360}
  },
  "asset_allocation": {
    "equity": 62,
    "debt": 21,
    "gold": 10,
    "cash": 7
  },
  "recommended_funds": [...]
}
```

### 2.3 Tax Optimization Agent
**Purpose**: Minimize tax liability through regime selection and deduction optimization

**Tax Slabs (Old Regime - FY 2024-25)**:
```
Income             Tax Rate    Calculation
₹0 - ₹3L          0%         No tax
₹3L - ₹7L         5%         (Income - 3L) × 5%
₹7L - ₹10L        20%        20,000 + (Income - 7L) × 20%
₹10L - ₹17L       30%        80,000 + (Income - 10L) × 30%
> ₹17L            45%        290,000 + (Income - 17L) × 45%
```

**Deduction Identification**:
- Section 80C (₹1.5L): SIP, Insurance, Postal Schemes
- Section 80D (₹1L): Health Insurance
- Section 80E: Education Loan Interest (no limit)
- Section 80G: Charitable Donations (50-100% deduction)
- Standard Deduction: ₹50,000

**HRA Optimization**:
```
HRA Exemption = MIN(
  HRA Received,
  50% of Salary (for metro) / 40% (non-metro),
  Rent Paid - 10% of Salary
)
```

**NPS Recommendation**:
```
Recommended NPS = MIN(
  ₹2L limit (80C + 80CCD1B),
  15% of Annual Income
)

Tax Benefit = Recommended NPS × Marginal Tax Rate
```

### 2.4 Risk Analysis Agent
**Purpose**: Profile user risk appetite and recommend investments

**Risk Score Calculation**:
```
Base Score = 50

Age Factor:
- < 30 years: +15
- 30-40 years: +10
- 40-50 years: +5
- > 50 years: -10

Emergency Fund Factor:
- >= 6 months: +10
- >= 3 months: +5
- < 3 months: -10

Debt Factor:
- Debt/Income < 50%: +10
- Debt/Income < 100%: +5
- Debt/Income > 100%: -15

Savings Rate Factor:
- > 30%: +10
- 15-30%: +5
- < 15%: -5

Risk Score = CLAMP(Base Score + Adjustments, 0, 100)
Risk Profile = 
  - Score >= 70: Aggressive
  - Score 40-70: Moderate
  - Score < 40: Conservative
```

## 3. API Architecture

### Request-Response Flow

```
Client Request
    ↓
FastAPI Router (Validates input)
    ↓
Route Handler (Route-specific logic)
    ↓
Agent Selection (Picks appropriate agent)
    ↓
Agent Processing (Runs calculations + AI)
    ↓
LLM Integration (Gets recommendations)
    ↓
Data Formatter (Structures response)
    ↓
Response to Client
```

### Error Handling Strategy

```python
try:
    # Process request
except ValueError:
    # Missing/invalid input
    HTTP 400 Bad Request
except LLMError:
    # OpenAI API error
    HTTP 503 Service Unavailable
except Exception:
    # Unexpected error
    HTTP 500 Internal Server Error
    Log error for debugging
```

## 4. Data Models

### User Profile
```json
{
  "user_id": "user_timestamp",
  "name": "String",
  "email": "String (unique)",
  "age": "Integer",
  "gender": "String",
  "phone": "String",
  "created_at": "DateTime",
  "updated_at": "DateTime"
}
```

### Financial Input
```json
{
  "user_id": "String",
  "monthly_income": "Float",
  "annual_income": "Float",
  "monthly_expenses": "Float",
  "annual_expenses": "Float",
  "existing_savings": "Float",
  "existing_investments": "Float",
  "debt_amount": "Float",
  "emergency_fund_target": "Float",
  "risk_profile": "Enum[Conservative, Moderate, Aggressive]"
}
```

### Financial Goal
```json
{
  "goal_id": "String",
  "user_id": "String",
  "goal_name": "String (House, Car, Retirement, etc.)",
  "goal_type": "String",
  "target_amount": "Float",
  "target_year": "Integer",
  "priority": "Integer (1-3)",
  "created_at": "DateTime"
}
```

## 5. Integration Points

### LLM Integration (OpenAI)
```
Endpoint: api.openai.com/v1/chat/completions
Method: POST
Auth: Bearer {API_KEY}

System Prompt:
"You are FinGuru, an AI financial advisor specializing in Indian personal finance..."

Temperature: 0.7 (Creative but accurate)
Max Tokens: 500-1000 (Per response)
```

### Database Integration (MongoDB)
```
Collections:
- users (Indexed on: email, user_id)
- financial_data (Indexed on: user_id)
- goals (Indexed on: user_id)
- chat_history (Indexed on: user_id, created_at)
- analysis_results (Indexed on: user_id, analysis_type)
```

## 6. Performance Optimization

### Caching Strategy
```
Cache Layer (Redis):
- Money Health Score: 24 hours per user
- Tax Analysis: 7 days per user
- Risk Profile: 30 days per user
- LLM Responses: By hash of prompt

Invalidation:
- User financial update → Clear all caches
- New goal → Clear plan cache only
```

### Query Optimization
```
MongoDB Indexes:
- users: email (unique)
- financial_data: user_id
- goals: user_id, created_at
- chat_history: user_id, created_at DESC
```

### API Response Times
```
/financial/money-health-score: ~200ms (computation)
/financial/financial-plan: ~300ms (SIP calculations)
/financial/tax-analysis: ~250ms (regime comparison)
/financial/risk-profile: ~150ms (scoring)
/chat/chat: ~2-3s (LLM latency)
/full-analysis: ~4-5s (all agents)
```

## 7. Security Architecture

### Authentication Flow
```
User Login
    ↓
Generate JWT Token (HS256)
    ↓
Token stored in cookie (httpOnly, secure)
    ↓
All subsequent requests include token
    ↓
Token validation on backend
    ↓
Request authorized/denied
```

### Data Protection
```
In Transit:
- HTTPS/TLS encryption
- CORS headers validation

At Rest:
- MongoDB document-level encryption (optional)
- Sensitive fields encrypted (SSN masks, account numbers)
- No PII in logs

API Security:
- Rate limiting: 100 req/min per user
- Input validation on all endpoints
- SQL injection prevention (Pydantic models)
```

## 8. Scalability Architecture

### Horizontal Scaling
```
Load Balancer (Nginx/Cloud Load Balancer)
    ↓
API Instances (Auto-scaling group)
    ├─ Instance 1 (FastAPI)
    ├─ Instance 2 (FastAPI)
    └─ Instance n (FastAPI)
    ↓
Shared Database (MongoDB Atlas)
```

### Auto-Scaling Rules
```
Scale Up if:
- CPU > 70% for 2 minutes
- Memory > 80% for 2 minutes
- Request latency > 1s

Scale Down if:
- CPU < 20% for 10 minutes
- Memory < 30% for 10 minutes
```

## 9. Error Handling & Monitoring

### Error Classification
```
Client Errors (4xx):
- 400: Invalid input
- 401: Unauthorized
- 403: Forbidden
- 404: Not found

Server Errors (5xx):
- 502: Bad gateway
- 503: Service unavailable
- 500: Internal error

Logging Level:
- DEBUG: Development
- INFO: Important events
- WARNING: Potential issues
- ERROR: Failures
- CRITICAL: System down
```

### Monitoring Metrics
```
System Metrics:
- CPU, Memory, Disk usage
- Request/response times
- Error rates
- API availability

Business Metrics:
- Users registered/active
- Analyses performed
- Chat interactions
- Tax savings identified
```

## 10. Deployment Architecture

### Production Environment
```
Frontend Deployment:
- Vercel (Next.js hosting)
- CDN for static assets
- Automatic deployments on git push

Backend Deployment:
- Google Cloud Run (or AWS Lambda)
- Docker containers
- MongoDB Atlas (managed database)
- Firebase for authentication (optional)

CI/CD Pipeline:
- GitHub Actions
- Automated tests on PR
- Deploy on main branch merge
```

---

**Document Version**: 1.0
**Last Updated**: 2024
**Architecture**: Multi-Agent AI System
**Status**: Production Ready
