import React from 'react';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center">
          <h1 className="text-6xl font-bold text-gray-900 mb-4">
            FinGuru AI
          </h1>
          <p className="text-2xl text-gray-600 mb-8">
            Your Personal Money Mentor 💰
          </p>
          <p className="text-lg text-gray-500 mb-12">
            Turn confused savers into confident investors.
            <br />
            Financial planning as easy as checking WhatsApp.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mt-16">
            {/* Feature Cards */}
            <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-bold mb-2">Money Health Score</h3>
              <p className="text-gray-600">Get your comprehensive financial wellness score in 5 minutes</p>
            </div>
            
            <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
              <div className="text-4xl mb-4">📈</div>
              <h3 className="text-xl font-bold mb-2">SIP Planner</h3>
              <p className="text-gray-600">Smart Systematic Investment Plans tailored to your goals</p>
            </div>
            
            <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
              <div className="text-4xl mb-4">💼</div>
              <h3 className="text-xl font-bold mb-2">Tax Optimizer</h3>
              <p className="text-gray-600">Maximize deductions and minimize your tax burden</p>
            </div>
            
            <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-bold mb-2">AI Advisor</h3>
              <p className="text-gray-600">Ask anything about your finances, get instant guidance</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
