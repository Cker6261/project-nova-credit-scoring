import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

const BankDashboard = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('credit_score');
  const [filterRisk, setFilterRisk] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE}/get_users`);
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
    setLoading(false);
  };

  const getScoreColor = (score) => {
    if (score >= 750) return 'text-green-600 bg-green-100';
    if (score >= 650) return 'text-blue-600 bg-blue-100';
    if (score >= 550) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'Low Risk': return 'text-green-800 bg-green-100';
      case 'Medium Risk': return 'text-yellow-800 bg-yellow-100';
      case 'High Risk': return 'text-red-800 bg-red-100';
      default: return 'text-gray-800 bg-gray-100';
    }
  };

  const filteredAndSortedUsers = users
    .filter(user => {
      const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           user.occupation.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesRisk = filterRisk === 'all' || user.risk_category === filterRisk;
      return matchesSearch && matchesRisk;
    })
    .sort((a, b) => {
      if (sortBy === 'credit_score') return b.credit_score - a.credit_score;
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      if (sortBy === 'age') return a.age - b.age;
      if (sortBy === 'income') return b.monthly_income - a.monthly_income;
      return 0;
    });

  const stats = {
    total: users.length,
    lowRisk: users.filter(u => u.risk_category === 'Low Risk').length,
    mediumRisk: users.filter(u => u.risk_category === 'Medium Risk').length,
    highRisk: users.filter(u => u.risk_category === 'High Risk').length,
    avgScore: users.length > 0 ? Math.round(users.reduce((sum, u) => sum + u.credit_score, 0) / users.length) : 0
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading bank dashboard...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Bank Dashboard</h1>
        <p className="text-gray-600">Monitor credit scores and risk assessments across your customer base</p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-primary-600">{stats.total}</div>
          <div className="text-sm text-gray-600">Total Customers</div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-green-600">{stats.lowRisk}</div>
          <div className="text-sm text-gray-600">Low Risk</div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-yellow-600">{stats.mediumRisk}</div>
          <div className="text-sm text-gray-600">Medium Risk</div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-red-600">{stats.highRisk}</div>
          <div className="text-sm text-gray-600">High Risk</div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-purple-600">{stats.avgScore}</div>
          <div className="text-sm text-gray-600">Avg Score</div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
            <input
              type="text"
              placeholder="Search by name or occupation..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2"
            >
              <option value="credit_score">Credit Score</option>
              <option value="name">Name</option>
              <option value="age">Age</option>
              <option value="income">Income</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Risk Filter</label>
            <select
              value={filterRisk}
              onChange={(e) => setFilterRisk(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2"
            >
              <option value="all">All Risks</option>
              <option value="Low Risk">Low Risk</option>
              <option value="Medium Risk">Medium Risk</option>
              <option value="High Risk">High Risk</option>
            </select>
          </div>
          
          <div className="flex items-end">
            <button
              onClick={fetchUsers}
              className="w-full bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700"
            >
              Refresh Data
            </button>
          </div>
        </div>
      </div>

      {/* Users Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Customer Portfolio ({filteredAndSortedUsers.length} customers)
          </h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Customer
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Credit Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Risk Category
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Income
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Digital Activity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Payment History
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Employment
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredAndSortedUsers.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{user.name}</div>
                      <div className="text-sm text-gray-500">{user.occupation}</div>
                      <div className="text-xs text-gray-400">Age: {user.age}</div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(user.credit_score)}`}>
                      {user.credit_score}
                    </span>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRiskColor(user.risk_category)}`}>
                      {user.risk_category}
                    </span>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">₹{user.monthly_income.toLocaleString()}</div>
                    <div className="text-xs text-gray-500 capitalize">{user.income_level} income</div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{user.upi_transactions} UPI/month</div>
                    <div className="text-xs text-gray-500">
                      {user.has_savings_account ? '✅ Savings Acc' : '❌ No Savings'}
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm">
                      <div className={user.rent_paid_on_time ? 'text-green-600' : 'text-red-600'}>
                        {user.rent_paid_on_time ? '✅' : '❌'} Rent
                      </div>
                      <div className={user.utility_bills_paid ? 'text-green-600' : 'text-red-600'}>
                        {user.utility_bills_paid ? '✅' : '❌'} Utilities
                      </div>
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{user.employment_months} months</div>
                    <div className="text-xs text-gray-500">Education: {user.education_level}/5</div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Risk Distribution Chart (Simple) */}
      <div className="mt-8 bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Distribution</h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
              <div 
                className="bg-green-500 h-4 rounded-full" 
                style={{ width: `${(stats.lowRisk / stats.total) * 100}%` }}
              ></div>
            </div>
            <div className="text-sm font-medium">Low Risk</div>
            <div className="text-xs text-gray-500">{Math.round((stats.lowRisk / stats.total) * 100)}%</div>
          </div>
          
          <div className="text-center">
            <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
              <div 
                className="bg-yellow-500 h-4 rounded-full" 
                style={{ width: `${(stats.mediumRisk / stats.total) * 100}%` }}
              ></div>
            </div>
            <div className="text-sm font-medium">Medium Risk</div>
            <div className="text-xs text-gray-500">{Math.round((stats.mediumRisk / stats.total) * 100)}%</div>
          </div>
          
          <div className="text-center">
            <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
              <div 
                className="bg-red-500 h-4 rounded-full" 
                style={{ width: `${(stats.highRisk / stats.total) * 100}%` }}
              ></div>
            </div>
            <div className="text-sm font-medium">High Risk</div>
            <div className="text-xs text-gray-500">{Math.round((stats.highRisk / stats.total) * 100)}%</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BankDashboard;
