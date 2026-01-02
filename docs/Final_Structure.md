shiny_jar_suite/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── database.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── expenses.py
│   │   │       └── customers.py
│   │   └── crud/
│   │       └── __init__.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── app.py
│   ├── pages/
│   │   ├── dashboard.py
│   │   ├── expenses.py
│   │   └── customers.py
│   └── requirements.txt
├── docker-compose.yml    # ONLY for database
├── .env
├── start.sh              # Master start script
└── README.md