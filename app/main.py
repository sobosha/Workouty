from sqlalchemy import text

from fastapi import FastAPI,HTTPException, Depends

from app.db import engine, get_db_session

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas import RegisterRequest, UserResponse
from app.models import Users
from app.security import hash_password
app = FastAPI(title = "Workouty API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail="Database connection failed")
    
    return {"status": "ok", "database": "connected"}

@app.post("/auth/register" , response_model = UserResponse , status_code = 201)
def register_user(payload: RegisterRequest , db: Session = Depends(get_db_session)) -> UserResponse:
    user = Users(email = payload.email , password_hash = hash_password(payload.password))
    try:
        db.add(user)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        error(code=409, message="Email already registered")
    db.refresh(user)
    return UserResponse(id = user.id , email = user.email , created_at = user.created_at)

def error(code = 500, message = "Internal Server Error"):
    raise HTTPException(status_code=code, detail=message)