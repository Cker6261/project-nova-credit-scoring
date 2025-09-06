import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="gradient-bg">
        <div className="max-w-7xl mx-auto px-4 py-20">
          <div className="text-center text-white">
            <h1 className="text-5xl font-bold mb-6">
              Project Nova
            </h1>
            <h2 className="text-2xl font-light mb-8 opacity-90">
              Equitable Credit Scoring Engine
            </h2>
            <p className="text-xl mb-12 max-w-3xl mx-auto leading-relaxed">
              Revolutionizing credit scoring with alternative data sources for a more 
              inclusive and fair financial system. We consider UPI transactions, utility 
              payments, and employment history beyond traditional credit metrics.
            </p>
            
            <div className="flex justify-center space-x-6">
              <Link
                to="/user"
                className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Check Your Score
              </Link>
              <Link
                to="/bank"
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary-600 transition-colors"
              >
                Bank Portal
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">
              Why Project Nova?
            </h3>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Traditional credit scoring excludes millions. We're changing that with innovative approaches.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 mx-auto mb-4 bg-primary-100 rounded-full flex items-center justify-center">
                <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h4 className="text-xl font-semibold mb-3">Alternative Data</h4>
              <p className="text-gray-600">
                UPI transactions, utility payments, rent history, and digital behavior 
                create a comprehensive financial profile.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 mx-auto mb-4 bg-success text-white rounded-full flex items-center justify-center">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h4 className="text-xl font-semibold mb-3">AI-Powered</h4>
              <p className="text-gray-600">
                Machine learning algorithms analyze patterns to provide fair and 
                accurate credit assessments for everyone.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 mx-auto mb-4 bg-warning text-white rounded-full flex items-center justify-center">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <h4 className="text-xl font-semibold mb-3">Transparent</h4>
              <p className="text-gray-600">
                Clear explanations of score factors help users understand and 
                improve their financial standing.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary-600 mb-2">1.7B</div>
              <div className="text-gray-600">Unbanked Adults Globally</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-success mb-2">85%</div>
              <div className="text-gray-600">Accuracy with Alt Data</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-warning mb-2">50%</div>
              <div className="text-gray-600">More Inclusive</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-danger mb-2">24/7</div>
              <div className="text-gray-600">Real-time Processing</div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 bg-primary-600">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h3 className="text-3xl font-bold text-white mb-6">
            Ready to Experience Fair Credit Scoring?
          </h3>
          <p className="text-xl text-primary-100 mb-8">
            Join thousands who are building their credit score with alternative data.
          </p>
          <Link
            to="/user"
            className="bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors inline-block"
          >
            Get Started Now
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
