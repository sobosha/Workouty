from http.client import HTTPException

from sqlalchemy import text

from fastapi import FastAPI

from app.db import engine

app = FastAPI(title = "Workouty API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as e:
        raise HTTPException(status_code=503, detail="Database connection failed")
    
    return {"status": "ok", "database": "connected"}

def error(code = 500, message = "Internal Server Error"):
    raise HTTPException(status_code=code, detail=message)