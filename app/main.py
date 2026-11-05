from http.client import HTTPException

from fastapi import FastAPI

from app.db import engine

app = FastAPI(title = "Workouty API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    if(not engine.connect()):
        error(503, "Database is not available")
    else:
        return {"status": "ok" , "database": "connected"}

def error(code = 500, message = "Internal Server Error"):
    raise HTTPException(status_code=code, detail=message)