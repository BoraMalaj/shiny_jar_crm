shiny-jar-suite/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app entry
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── expenses.py
│   │   │   │   ├── customers.py
│   │   │   │   └── analytics.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── database.py   # SQLAlchemy models
│   │   ├── schemas/
│   │   │   └── __init__.py   # Pydantic schemas
│   │   ├── crud/
│   │   │   └── __init__.py   # CRUD operations
│   │   ├── core/
│   │   │   ├── config.py     # Configuration
│   │   │   ├── security.py   # Auth utils
│   │   │   └── database.py   # DB connection
│   │   └── dependencies.py
│   ├── alembic/
│   │   └── alembic.ini
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py               # Streamlit main
│   ├── pages/
│   │   ├── 01_Dashboard.py
│   │   ├── 02_Expenses.py
│   │   ├── 03_Customers.py
│   │   └── 04_Analytics.py
│   ├── components/
│   │   ├── sidebar.py
│   │   └── charts.py
│   └── assets/
│       └── shiny_jar_logo.png
├── shared/
│   └── utils/
│       └── helpers.py
├── tests/
├── scripts/
│   ├── setup_db.py
│   └── import_instagram.py
├── .env.example
├── docker-compose.yml
├── README.md
└── requirements.txt