# 💎 Shiny Jar CRM - Jewelry Business Management System

![Shiny Jar CRM](frontend/assets/logo.png)

A complete CRM system built for a jewelry business, featuring inventory management, customer tracking, supplier management, financial analytics and more...

## 🚀 Features

### 📊 **Dashboard**
- Real-time business metrics
- Income/Expense tracking
- Monthly trends visualization
- Top customer insights

### 👥 **Customer Management**
- Complete customer database
- Instagram integration
- Purchase history tracking
- Customer segmentation

### 🏭 **Supplier Management**
- Supplier database
- Order tracking
- Performance analytics
- Contact management

### 📦 **Inventory System**
- Stock level tracking
- Low stock alerts
- Stock movement history
- Inventory valuation
- Supplier linking

### 💰 **Financial Management**
- Income/Expense tracking
- Budget planning & tracking
- Financial reports
- Category-based analytics

### 🔐 **Multi-Role Authentication**
- Admin (Business Owner)
- Customer Portal
- Supplier Portal
- Demo mode for presentations

## 🛠️ Technology Stack

**Backend:**
- FastAPI (Python)
- SQLAlchemy ORM
- JWT Authentication
- PostgreSQL Database

**Frontend:**
- Streamlit (Python)
- Plotly for visualizations
- Dark theme UI
- Responsive design

**Database:**
- PostgreSQL
- Docker containerization
- Complete schema with sample data

**DevOps:**
- Docker & Docker Compose
- Environment variables
- Ready for cloud deployment

## 📦 Installation & Setup

### Option 1: Local Development

```bash
# 1. Clone the repository
git clone https://github.com/BoraMalaj/shiny-jar-crm.git
cd shiny_jar_crm

# 2. Set up environment
cp .env.example .env
# Edit .env with your database credentials

# 3. Start the database
docker-compose up -d

# 4. Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Initialize database
python backend/scripts/setup_dev.py

# 7. Start backend server
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 8. Start frontend (in new terminal)
cd frontend
streamlit run app.py


Access the Application
Frontend: http://localhost:8501

Backend API: http://localhost:8000

API Documentation: http://localhost:8000/docs

Database: PostgreSQL on localhost:5432

🔐 Demo Accounts
Admin Mode:

Username: admin or bora_malaj

Password: admin123

Customer Portal:

Username: arsjana_shehaj

Password: admin123

Supplier Portal:

Username: gerta_tirana

Password: admin123

📊 Database Schema
https://docs/database_schema.png

The database includes tables for:

Users & Authentication

Customers & Suppliers

Transactions (Income/Expense)

Inventory & Stock Movements

Budgets & Categories

Businesses & Settings

🎯 University Project Features
Budget Management System - Track and analyze expenses vs budgets

Analytics Dashboard - Business intelligence and forecasting

Multi-role System - Different interfaces for different users

Professional Reports - Exportable financial reports

Real-time Data - Live updates and notifications

📈 Project Structure
text
shiny_jar_suite/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Configuration & database
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── main.py      # Main application
│   ├── scripts/         # Database scripts
│   └── requirements.txt
├── frontend/            # Streamlit frontend
│   ├── pages/          # Page modules
│   ├── assets/         # Images & logos
│   └── app.py          # Main app
├── docs/               # Documentation
├── docker-compose.yml  # Docker setup
└── README.md           # This file
🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
New York University - Project requirements and guidance

Streamlit - Amazing frontend framework

FastAPI - High-performance backend framework

PostgreSQL - Robust database system

📞 Contact
Bora Malaj - GitHub - bora@shinyjar.com

Project Link: https://github.com/BoraMalaj/shiny-jar-crm