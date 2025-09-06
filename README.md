# Project Nova - Equitable Credit Scoring Engine

**An AI-powered credit scoring system that uses alternative data sources for more inclusive financial assessment.**

## 🌟 Overview

Project Nova revolutionizes credit scoring by incorporating alternative data sources beyond traditional credit history. Our system analyzes UPI transactions, utility payments, employment history, and digital behavior to provide fair credit assessments for individuals who might be underserved by conventional scoring methods.

## 🎯 Key Features

- **Alternative Data Integration**: UPI transactions, utility payments, rent history
- **AI-Powered Scoring**: Machine learning model trained on diverse financial behaviors
- **Transparent Explanations**: Clear breakdown of score factors
- **Real-time Processing**: Instant credit score calculation
- **Dual Dashboards**: Separate interfaces for users and financial institutions
- **Risk Categorization**: Automated risk assessment with detailed insights

## 🏗️ Project Structure

```
project-nova/
├── backend/                 # FastAPI backend service
│   ├── main.py             # Main API application
│   ├── models.py           # ML model implementation
│   ├── database.py         # Database management
│   ├── schema.py           # API schemas
│   ├── train_model.py      # Model training script
│   ├── requirements.txt    # Python dependencies
│   └── nova_credit.db      # SQLite database (generated)
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── pages/          # Main application pages
│   │   ├── components/     # Reusable components
│   │   └── App.js          # Main app component
│   ├── public/
│   └── package.json        # Node.js dependencies
├── data/                   # Data files and datasets
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (for backend)
- Node.js 14+ (for frontend)
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv nova_env
   nova_env\Scripts\activate  # Windows
   # source nova_env/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the ML model:**
   ```bash
   python train_model.py
   ```

5. **Start the backend server:**
   ```bash
   python main.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## 📊 API Endpoints

### Base URL: `http://localhost:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and health check |
| `/calculate_score` | POST | Calculate credit score for user data |
| `/get_users` | GET | Get all users with scores (bank dashboard) |
| `/get_user/{id}` | GET | Get specific user details |
| `/health` | GET | Health check endpoint |

### Sample API Request

```bash
curl -X POST "http://localhost:8000/calculate_score" \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "age": 28,
  "occupation": "Software Engineer",
  "income_level": "high",
  "monthly_income": 75000,
  "education_level": 4,
  "upi_transactions": 45,
  "rent_paid_on_time": true,
  "utility_bills_paid": true,
  "has_savings_account": true,
  "employment_months": 24
}'
```

## 🎮 Demo Credentials

The system comes pre-loaded with 15 test user profiles:

| User ID | Name | Occupation | Risk Level | Score Range |
|---------|------|------------|------------|-------------|
| 1 | Arjun Sharma | Software Engineer | Low Risk | 750+ |
| 2 | Priya Patel | Teacher | Medium Risk | 650-750 |
| 3 | Rahul Kumar | Delivery Partner | High Risk | <550 |
| ... | ... | ... | ... | ... |

## 🧠 ML Model Details

### Features Used

1. **Demographic**: Age, education level, employment duration
2. **Financial**: Monthly income, income level
3. **Digital Behavior**: UPI transactions per month
4. **Payment History**: Rent and utility payment consistency
5. **Banking**: Savings account ownership

### Model Architecture

- **Algorithm**: Random Forest Regressor
- **Training Data**: 1000+ synthetic records
- **Score Range**: 300-900 (following FICO-like scale)
- **Performance**: ~85% accuracy on test data

### Score Interpretation

| Score Range | Category | Description |
|-------------|----------|-------------|
| 750-900 | Excellent | Lowest risk, best rates |
| 650-749 | Good | Low risk, favorable terms |
| 550-649 | Fair | Medium risk, standard terms |
| 300-549 | Poor | High risk, limited options |

## 🖥️ User Interfaces

### Landing Page
- Project overview and value proposition
- Feature highlights
- Call-to-action buttons

### User Dashboard
- Personal credit score display
- Score breakdown and explanations
- Interactive score calculator
- Profile management

### Bank Dashboard
- Customer portfolio overview
- Risk distribution analytics
- Search and filtering capabilities
- Bulk customer assessment

## 🔍 Score Transparency

Project Nova provides clear explanations for every score calculation:

- ✅ **Positive Factors**: High income, good payment history, digital activity
- ⚠️ **Areas for Improvement**: Payment delays, low digital engagement
- 💡 **Recommendations**: Actionable advice to improve scores

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLite**: Lightweight database
- **scikit-learn**: Machine learning library
- **Pandas**: Data manipulation
- **Pydantic**: Data validation

### Frontend
- **React**: JavaScript UI library
- **TailwindCSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client

## 📈 Business Impact

### For Individuals
- Access to credit for underbanked populations
- Clear understanding of credit factors
- Actionable improvement recommendations
- Fair assessment based on actual behavior

### For Financial Institutions
- Reduced default rates through better risk assessment
- Expanded customer base
- Data-driven lending decisions
- Regulatory compliance support

## 🔒 Privacy & Security

- **Data Minimization**: Only necessary data collected
- **Transparent Processing**: Clear explanations provided
- **Secure APIs**: Input validation and error handling
- **Local Processing**: No external data sharing

## 🚀 Future Enhancements

### Phase 2 Features
- Real-time bank account integration
- Mobile app development
- Advanced ML models (gradient boosting, neural networks)
- Social credit factors
- Blockchain verification

### Scaling Considerations
- Microservices architecture
- Cloud deployment (AWS/Azure)
- Real-time streaming data
- Advanced analytics dashboard

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Load Testing
```bash
cd backend
pip install locust
locust -f load_test.py
```

## 📝 Development Guidelines

### Backend Development
1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Include docstrings for modules and functions
4. Write unit tests for new features

### Frontend Development
1. Use functional components with hooks
2. Follow React best practices
3. Implement responsive design
4. Add proper error handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or support:
- Create an issue in the GitHub repository
- Email: support@projectnova.ai
- Documentation: [docs.projectnova.ai](https://docs.projectnova.ai)

## 🙏 Acknowledgments

- Thanks to the open-source community
- Inspired by financial inclusion initiatives
- Built for the global hackathon community

---

**Built with ❤️ for financial inclusion and fair credit scoring**
