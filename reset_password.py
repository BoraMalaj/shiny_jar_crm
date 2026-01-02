# reset_passwords.py
import bcrypt
from sqlalchemy import create_engine, text

# Database connection
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/shinyjar_db"
engine = create_engine(DATABASE_URL)

# Hash for "admin123"
hashed_password = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode('utf-8')

# Update all users
with engine.connect() as conn:
    users = ['bora_malaj', 'gerta_tirana', 'arsjana_shehaj', 'admin']
    
    for username in users:
        conn.execute(
            text("UPDATE users SET hashed_password = :hash WHERE username = :username"),
            {"hash": hashed_password, "username": username}
        )
    
    conn.commit()

print(f"✅ Updated passwords for all users to 'admin123'")
print(f"Hash used: {hashed_password}")