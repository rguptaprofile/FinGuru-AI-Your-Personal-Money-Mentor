# FinGuru Frontend - React/Next.js Setup

## Prerequisites
- Node.js 16+
- npm or yarn
- Code editor (VS Code recommended)

## Installation Steps

### 1. Install Dependencies
```bash
npm install
```

### 2. Setup Environment
```bash
cp .env.example .env.local
# Edit .env.local with API URL
```

### 3. Run Development Server
```bash
npm run dev
```

### 4. Open Browser
Navigate to http://localhost:3000

## Available Pages

### `/` - Landing Page
- Project overview
- Feature cards
- Call to action

### `/dashboard` - Main Dashboard
- Financial input form
- Money Health Score display
- Chart visualizations
- Tax analysis results
- SIP recommendations

### `/chat` - AI Chat Interface
- Real-time chat with AI advisor
- Message history
- Quick advice feature

## Project Structure
```
frontend/
├── pages/
│   ├── index.js              # Landing page
│   ├── dashboard.js          # Main dashboard
│   ├── chat.js               # Chat interface
│   └── api.js                # API client
├── lib/
│   └── api.js                # API utilities
├── components/               # React components
├── package.json
├── next.config.js
└── .env.example
```

## Building for Production
```bash
npm run build
npm run start
```

## Technologies Used
- React 18+
- Next.js 14
- Tailwind CSS
- Recharts (for visualizations)
- Axios (for API calls)
