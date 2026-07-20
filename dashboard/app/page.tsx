"use client";

import { useState } from "react";

const stats = [
  { label: "Templates", value: "37", icon: "📄", color: "bg-blue-50 text-blue-700" },
  { label: "AI Agents", value: "6", icon: "🤖", color: "bg-green-50 text-green-700" },
  { label: "Policies", value: "4", icon: "📋", color: "bg-yellow-50 text-yellow-700" },
  { label: "Score Criteria", value: "7", icon: "⚖️", color: "bg-purple-50 text-purple-700" },
];

const phases = [
  { icon: "📋", title: "1. Registreren", desc: "Verwerkingsactiviteiten registreren met automatische DPIA/FRIA-detectie", color: "border-blue-500" },
  { icon: "⚖️", title: "2. Beoordelen", desc: "Risico-analyse met 37 evidence-based templates en RAG-gestuurde analyse", color: "border-green-500" },
  { icon: "🛡️", title: "3. Mitigeren", desc: "Geprioriteerde maatregelen met juridische basis en workflow-automatisering", color: "border-yellow-500" },
  { icon: "📊", title: "4. Monitoren", desc: "Continue compliance-monitoring met real-time scoring en wetswijzigingsdetectie", color: "border-purple-500" },
];

export default function DashboardPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-[#1a365d] mb-2">Dashboard</h1>
      <p className="text-gray-500 mb-8">Living Compliance Engine — Real-time compliance monitoring</p>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((stat) => (
          <div key={stat.label} className={`${stat.color} rounded-xl p-6`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium opacity-75">{stat.label}</p>
                <p className="text-3xl font-bold mt-1">{stat.value}</p>
              </div>
              <span className="text-3xl">{stat.icon}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Phases */}
      <h2 className="text-xl font-bold text-[#1a365d] mb-4">Continue Compliance Cyclus</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {phases.map((phase) => (
          <div key={phase.title} className={`bg-white rounded-xl p-6 shadow-sm border-l-4 ${phase.color}`}>
            <span className="text-2xl">{phase.icon}</span>
            <h3 className="font-semibold text-[#1a365d] mt-3">{phase.title}</h3>
            <p className="text-sm text-gray-500 mt-2">{phase.desc}</p>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <h2 className="text-xl font-bold text-[#1a365d] mb-4">Quick Actions</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <a href="/compliance" className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow border border-gray-100">
          <span className="text-2xl">⚖️</span>
          <h3 className="font-semibold text-[#1a365d] mt-3">Compliance Score</h3>
          <p className="text-sm text-gray-500 mt-1">Bereken real-time compliance score</p>
        </a>
        <a href="/agents" className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow border border-gray-100">
          <span className="text-2xl">🤖</span>
          <h3 className="font-semibold text-[#1a365d] mt-3">DPIA Agent</h3>
          <p className="text-sm text-gray-500 mt-1">Genereer volledige DPIA met AI</p>
        </a>
        <a href="/policies" className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow border border-gray-100">
          <span className="text-2xl">📋</span>
          <h3 className="font-semibold text-[#1a365d] mt-3">Policy Evaluatie</h3>
          <p className="text-sm text-gray-500 mt-1">Evalueer compliance policies</p>
        </a>
      </div>

      {/* API Status */}
      <div className="mt-8 bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-lg font-bold text-[#1a365d] mb-4">API Endpoints</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
          <div className="flex items-center gap-2">
            <span className="w-16 font-mono text-xs bg-green-100 text-green-700 px-2 py-1 rounded">GET</span>
            <code className="text-gray-600">/api/v1/templates/</code>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-16 font-mono text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">POST</span>
            <code className="text-gray-600">/api/v1/agents/dpia/run</code>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-16 font-mono text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">POST</span>
            <code className="text-gray-600">/api/v1/compliance/score</code>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-16 font-mono text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">POST</span>
            <code className="text-gray-600">/api/v1/policies/evaluate</code>
          </div>
        </div>
      </div>
    </div>
  );
}
