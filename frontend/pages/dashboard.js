import React, { useState } from 'react';
import { financialApi } from '../lib/api';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const [userId, setUserId] = useState('');
  const [financialData, setFinancialData] = useState({
    monthly_income: 50000,
    annual_income: 600000,
    monthly_expenses: 30000,
    annual_expenses: 360000,
    existing_savings: 200000,
    existing_investments: 500000,
    debt_amount: 100000,
    age: 32,
    risk_profile: 'Moderate'
  });
  
  const [analysisResults, setAnalysisResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFinancialData({
      ...financialData,
      [name]: isNaN(value) ? value : parseFloat(value)
    });
  };

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const results = await financialApi.fullAnalysis(financialData, [
        { goal_name: 'House', target_amount: 5000000, target_year: 2030, priority: 1 },
        { goal_name: 'Retirement', target_amount: 10000000, target_year: 2054, priority: 1 },
        { goal_name: 'Car', target_amount: 1500000, target_year: 2026, priority: 2 }
      ]);
      setAnalysisResults(results.data);
    } catch (error) {
      console.error('Error:', error);
      alert('Error performing analysis');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">FinGuru Dashboard</h1>

        {/* Input Form */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">Your Financial Profile</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <input
              type="number"
              name="age"
              placeholder="Age"
              value={financialData.age}
              onChange={handleInputChange}
              className="border rounded px-4 py-2"
            />
            <input
              type="number"
              name="annual_income"
              placeholder="Annual Income"
              value={financialData.annual_income}
              onChange={handleInputChange}
              className="border rounded px-4 py-2"
            />
            <input
              type="number"
              name="annual_expenses"
              placeholder="Annual Expenses"
              value={financialData.annual_expenses}
              onChange={handleInputChange}
              className="border rounded px-4 py-2"
            />
            <select
              name="risk_profile"
              value={financialData.risk_profile}
              onChange={handleInputChange}
              className="border rounded px-4 py-2"
            >
              <option>Conservative</option>
              <option>Moderate</option>
              <option>Aggressive</option>
            </select>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Analyze My Finances'}
          </button>
        </div>

        {/* Results */}
        {analysisResults && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Money Health Score */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h3 className="text-xl font-bold mb-4">Money Health Score</h3>
              <div className="text-5xl font-bold text-blue-600 mb-2">
                {analysisResults.money_health_score?.total_score || 0}
              </div>
              <p className="text-gray-600">/100</p>
            </div>

            {/* Tax Savings */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h3 className="text-xl font-bold mb-4">Tax Savings</h3>
              <div className="text-5xl font-bold text-green-600 mb-2">
                ₹{(analysisResults.tax_analysis?.potential_tax_savings || 0).toLocaleString('en-IN')}
              </div>
              <p className="text-gray-600">Annual potential</p>
            </div>

            {/* Risk Profile */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h3 className="text-xl font-bold mb-4">Risk Profile</h3>
              <div className="text-2xl font-bold text-purple-600 mb-2">
                {analysisResults.risk_profile?.risk_profile}
              </div>
              <p className="text-gray-600">Score: {analysisResults.risk_profile?.risk_score}</p>
            </div>

            {/* Financial Plan */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h3 className="text-xl font-bold mb-4">Recommended SIP</h3>
              <div className="text-3xl font-bold text-orange-600 mb-2">
                ₹{(Object.values(analysisResults.financial_plan?.sip_recommendations || {})[0]?.monthly_sip || 0).toLocaleString('en-IN')}
              </div>
              <p className="text-gray-600">Monthly</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
