import React from 'react';
import { useAuth } from '../lib/auth/auth_provider';
import UserProfile from '../components/auth/UserProfile';

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">AI Writer Dashboard</h1>
          <UserProfile />
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Welcome, {user.name}!</h2>
          <p>Select a tool to get started with your AI writing journey.</p>
          
          {/* Dashboard content would go here */}
        </div>
      </main>
    </div>
  );
}