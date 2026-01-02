shiny_jar_suite/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── core/                # Config, database
│   │   └── models/              # SQLAlchemy models
│   ├── requirements.txt
│   └── backend.log
├── frontend/
│   ├── app.py                   # Streamlit main app
│   ├── pages/                   # Multi-page app
│   ├── requirements.txt
│   └── frontend.log
├── docker-compose.yml           # PostgreSQL only
├── backend/scripts/init.sql     # Database schema
├── start_all.sh                 # Master start script
├── stop_all.sh                  # Stop everything
├── db_cli.sh                    # Database access
├── status.sh                    # Check services
├── reset_db.sh                  # Reset database
├── .env                         # Environment variables
├── .gitignore
└── README.md                    # Project documentation