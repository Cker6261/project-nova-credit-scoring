import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

const UserDashboard = () => {
  const [selectedUser, setSelectedUser] = useState(1); // Default to first user
  const [userData, setUserData] = useState(null);
  const [allUsers, setAllUsers] = useState([]); // Store all users for dropdown
  const [scoreData, setScoreData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showCalculator, setShowCalculator] = useState(false);
  const [editMode, setEditMode] = useState(false); // New: Edit mode state
  const [formData, setFormData] = useState({
    name: '',
    age: 25,
    occupation: '',
    income_level: 'medium',
    monthly_income: 50000,
    education_level: 3,
    upi_transactions: 30,
    rent_paid_on_time: true,
    utility_bills_paid: true,
    has_savings_account: true,
    employment_months: 24
  });

  useEffect(() => {
    fetchAllUsers(); // Fetch all users for dropdown
  }, []);

  useEffect(() => {
    if (selectedUser) {
      fetchUserData();
    }
  }, [selectedUser]);

  // New: Fetch all users for dropdown
  const fetchAllUsers = async () => {
    try {
      const response = await axios.get(`${API_BASE}/get_users`);
      setAllUsers(response.data);
      if (response.data.length > 0 && !selectedUser) {
        setSelectedUser(response.data[0].id);
      }
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const fetchUserData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE}/get_user/${selectedUser}`);
      setUserData(response.data);
      setScoreData(null); // Clear previous score data
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
    setLoading(false);
  };

  // New: Start edit mode with current user data
  const startEdit = () => {
    setFormData({
      name: userData.name,
      age: userData.age,
      occupation: userData.occupation,
      income_level: userData.income_level,
      monthly_income: userData.monthly_income,
      education_level: userData.education_level,
      upi_transactions: userData.upi_transactions,
      rent_paid_on_time: userData.rent_paid_on_time,
      utility_bills_paid: userData.utility_bills_paid,
      has_savings_account: userData.has_savings_account,
      employment_months: userData.employment_months
    });
    setEditMode(true);
  };

  const calculateScore = async (data = null) => {
    setLoading(true);
    try {
      const payload = data || {
        name: userData.name,
        age: userData.age,
        occupation: userData.occupation,
        income_level: userData.income_level,
        monthly_income: userData.monthly_income,
        education_level: userData.education_level,
        upi_transactions: userData.upi_transactions,
        rent_paid_on_time: userData.rent_paid_on_time,
        utility_bills_paid: userData.utility_bills_paid,
        has_savings_account: userData.has_savings_account,
        employment_months: userData.employment_months
      };

      const response = await axios.post(`${API_BASE}/calculate_score`, payload);
      setScoreData(response.data);
      
      // Refresh user list and data after calculation
      await fetchAllUsers();
      await fetchUserData();
      
    } catch (error) {
      console.error('Error calculating score:', error);
    }
    setLoading(false);
  };

  const handleCalculateNew = async (e) => {
    e.preventDefault();
    await calculateScore(formData);
    setShowCalculator(false);
    // Reset form
    setFormData({
      name: '',
      age: 25,
      occupation: '',
      income_level: 'medium',
      monthly_income: 50000,
      education_level: 3,
      upi_transactions: 30,
      rent_paid_on_time: true,
      utility_bills_paid: true,
      has_savings_account: true,
      employment_months: 24
    });
  };

  // New: Handle edit/update
  const handleUpdateUser = async (e) => {
    e.preventDefault();
    await calculateScore(formData);
    setEditMode(false);
  };

  const getScoreColor = (score) => {
    if (score >= 750) return 'score-excellent';
    if (score >= 650) return 'score-good';
    if (score >= 550) return 'score-fair';
    return 'score-poor';
  };

  const getScoreLabel = (score) => {
    if (score >= 750) return 'Excellent';
    if (score >= 650) return 'Good';
    if (score >= 550) return 'Fair';
    return 'Needs Improvement';
  };

  if (loading && !userData && allUsers.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">User Dashboard</h1>
        
        {/* User Selector - Updated to use dynamic user list */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select User Profile ({allUsers.length} users):
          </label>
          <select
            value={selectedUser}
            onChange={(e) => setSelectedUser(parseInt(e.target.value))}
            className="border border-gray-300 rounded-md px-3 py-2 max-h-40 overflow-y-auto"
            style={{ maxHeight: '200px' }}
          >
            {allUsers.map(user => (
              <option key={user.id} value={user.id}>
                {user.name} (ID: {user.id}) - Score: {user.credit_score}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-wrap gap-4 mb-6">
          <button
            onClick={() => calculateScore()}
            disabled={loading || !userData}
            className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50"
          >
            {loading ? 'Calculating...' : 'Recalculate Score'}
          </button>
          
          <button
            onClick={() => setShowCalculator(true)}
            className="bg-success text-white px-4 py-2 rounded-md hover:bg-green-600"
          >
            Calculate New Score
          </button>

          {/* New: Edit User Button */}
          {userData && (
            <button
              onClick={startEdit}
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
            >
              Edit User
            </button>
          )}

          {/* New: Refresh Users Button */}
          <button
            onClick={fetchAllUsers}
            className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
          >
            Refresh Users
          </button>
        </div>
      </div>

      {userData && (
        <div className="grid lg:grid-cols-2 gap-8">
          {/* User Profile Card */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Profile Information</h2>
            
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Name:</span>
                <span className="font-medium">{userData.name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Age:</span>
                <span className="font-medium">{userData.age}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Occupation:</span>
                <span className="font-medium">{userData.occupation}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Monthly Income:</span>
                <span className="font-medium">₹{userData.monthly_income.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Income Level:</span>
                <span className="font-medium capitalize">{userData.income_level}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Education Level:</span>
                <span className="font-medium">{userData.education_level}/5</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Employment Duration:</span>
                <span className="font-medium">{userData.employment_months} months</span>
              </div>
            </div>
          </div>

          {/* Financial Behavior Card */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Financial Behavior</h2>
            
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">UPI Transactions/Month:</span>
                <span className="font-medium">{userData.upi_transactions}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Rent Paid On Time:</span>
                <span className={`font-medium ${userData.rent_paid_on_time ? 'text-success' : 'text-danger'}`}>
                  {userData.rent_paid_on_time ? 'Yes' : 'No'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Utility Bills Paid:</span>
                <span className={`font-medium ${userData.utility_bills_paid ? 'text-success' : 'text-danger'}`}>
                  {userData.utility_bills_paid ? 'Yes' : 'No'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Has Savings Account:</span>
                <span className={`font-medium ${userData.has_savings_account ? 'text-success' : 'text-danger'}`}>
                  {userData.has_savings_account ? 'Yes' : 'No'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Risk Category:</span>
                <span className={`font-medium px-2 py-1 rounded text-sm ${
                  userData.risk_category === 'Low Risk' ? 'bg-green-100 text-green-800' :
                  userData.risk_category === 'Medium Risk' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {userData.risk_category}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Credit Score Display */}
      {(userData || scoreData) && (
        <div className="mt-8">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-semibold mb-6 text-center">Credit Score</h2>
            
            <div className="text-center mb-8">
              <div className={`inline-block px-8 py-6 rounded-lg text-white ${getScoreColor(scoreData?.score || userData.credit_score)}`}>
                <div className="text-5xl font-bold mb-2">
                  {scoreData?.score || userData.credit_score}
                </div>
                <div className="text-xl">
                  {getScoreLabel(scoreData?.score || userData.credit_score)}
                </div>
              </div>
            </div>

            {/* Score Breakdown */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-4">Score Range</h3>
              <div className="relative">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>300</span>
                  <span>500</span>
                  <span>650</span>
                  <span>750</span>
                  <span>900</span>
                </div>
                <div className="h-4 bg-gradient-to-r from-red-500 via-yellow-500 via-blue-500 to-green-500 rounded-full relative">
                  <div 
                    className="absolute w-4 h-4 bg-white border-2 border-gray-800 rounded-full transform -translate-y-0"
                    style={{ left: `${((scoreData?.score || userData.credit_score) - 300) / 600 * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Explanations */}
            {scoreData?.explanations && (
              <div>
                <h3 className="text-lg font-semibold mb-4">Score Factors</h3>
                <div className="space-y-2">
                  {scoreData.explanations.map((explanation, index) => (
                    <div key={index} className="flex items-start p-3 bg-gray-50 rounded-md">
                      <span className="text-sm">{explanation}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Score Calculator Modal */}
      {showCalculator && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-md w-full max-h-screen overflow-y-auto">
            <h3 className="text-xl font-semibold mb-4">Calculate New Score</h3>
            
            <form onSubmit={handleCalculateNew} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
                <input
                  type="number"
                  value={formData.age}
                  onChange={(e) => setFormData({...formData, age: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  min="18" max="65"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Occupation</label>
                <input
                  type="text"
                  value={formData.occupation}
                  onChange={(e) => setFormData({...formData, occupation: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Income Level</label>
                <select
                  value={formData.income_level}
                  onChange={(e) => setFormData({...formData, income_level: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Income (₹)</label>
                <input
                  type="number"
                  value={formData.monthly_income}
                  onChange={(e) => setFormData({...formData, monthly_income: parseFloat(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Education Level (1-5)</label>
                <input
                  type="number"
                  value={formData.education_level}
                  onChange={(e) => setFormData({...formData, education_level: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  min="1" max="5"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">UPI Transactions/Month</label>
                <input
                  type="number"
                  value={formData.upi_transactions}
                  onChange={(e) => setFormData({...formData, upi_transactions: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>

              <div className="space-y-2">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.rent_paid_on_time}
                    onChange={(e) => setFormData({...formData, rent_paid_on_time: e.target.checked})}
                    className="mr-2"
                  />
                  <label className="text-sm text-gray-700">Rent paid on time</label>
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.utility_bills_paid}
                    onChange={(e) => setFormData({...formData, utility_bills_paid: e.target.checked})}
                    className="mr-2"
                  />
                  <label className="text-sm text-gray-700">Utility bills paid</label>
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.has_savings_account}
                    onChange={(e) => setFormData({...formData, has_savings_account: e.target.checked})}
                    className="mr-2"
                  />
                  <label className="text-sm text-gray-700">Has savings account</label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Employment Duration (months)</label>
                <input
                  type="number"
                  value={formData.employment_months}
                  onChange={(e) => setFormData({...formData, employment_months: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>

              <div className="flex space-x-4 pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-primary-600 text-white py-2 rounded-md hover:bg-primary-700 disabled:opacity-50"
                >
                  {loading ? 'Calculating...' : 'Calculate'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowCalculator(false)}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit User Modal */}
      {editMode && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full max-h-screen overflow-y-auto">
            <h3 className="text-xl font-semibold mb-4">Edit User: {userData?.name}</h3>
            
            <form onSubmit={handleUpdateUser} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
                <input
                  type="number"
                  value={formData.age}
                  onChange={(e) => setFormData({...formData, age: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  min="18" max="65"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Occupation</label>
                <input
                  type="text"
                  value={formData.occupation}
                  onChange={(e) => setFormData({...formData, occupation: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Income Level</label>
                <select
                  value={formData.income_level}
                  onChange={(e) => setFormData({...formData, income_level: e.target.value})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Income (₹)</label>
                <input
                  type="number"
                  value={formData.monthly_income}
                  onChange={(e) => setFormData({...formData, monthly_income: parseFloat(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Education Level (1-5)</label>
                <input
                  type="number"
                  value={formData.education_level}
                  onChange={(e) => setFormData({...formData, education_level: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  min="1" max="5"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">UPI Transactions per month</label>
                <input
                  type="number"
                  value={formData.upi_transactions}
                  onChange={(e) => setFormData({...formData, upi_transactions: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>

              <div className="space-y-2">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.rent_paid_on_time}
                    onChange={(e) => setFormData({...formData, rent_paid_on_time: e.target.checked})}
                    className="mr-2"
                  />
                  <label className="text-sm text-gray-700">Rent paid on time</label>
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.utility_bills_paid}
                    onChange={(e) => setFormData({...formData, utility_bills_paid: e.target.checked})}
                    className="mr-2"
                  />
                  <label className="text-sm text-gray-700">Utility bills paid</label>
                </div>

                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.has_savings_account}
                    onChange={(e) => setFormData({...formData, has_savings_account: e.target.checked})}
                    className="mr-2"
                  />
                  <label className="text-sm text-gray-700">Has savings account</label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Employment Duration (months)</label>
                <input
                  type="number"
                  value={formData.employment_months}
                  onChange={(e) => setFormData({...formData, employment_months: parseInt(e.target.value)})}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                />
              </div>

              <div className="flex space-x-4 pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                  {loading ? 'Updating...' : 'Update User'}
                </button>
                <button
                  type="button"
                  onClick={() => setEditMode(false)}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserDashboard;
