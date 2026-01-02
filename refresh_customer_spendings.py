from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

app = FastAPI()

# Replace with your actual database credentials
DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)

@app.post("/refresh-spending")
def refresh_spending():
    try:
        with engine.connect() as connection:
            # Executes the reusable SQL function created earlier
            connection.execute(text("SELECT refresh_customer_spending();"))
            connection.commit()
        return {"status": "success", "message": "Customer spending refreshed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))