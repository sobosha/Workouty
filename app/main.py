from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

from fastapi import FastAPI,HTTPException, Depends

from app.db import engine, get_db_session

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.dependencies import get_current_user
from app.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse, ExerciseResponse
from app.models import Users, Exercises
from app.security import hash_password, verify_email_format, verify_password
from app.seed_exercise import EXERCISES
from app.tokens import create_access_token


app = FastAPI(title = "Workouty API")


def seed_exercise():
    sql_command = insert(Exercises).values(EXERCISES).on_conflict_do_nothing(index_elements=['name'])
    with Session(engine) as session:
        session.execute(sql_command)
        session.commit()

if __name__ == "__main__":
    seed_exercise()

"""-------------get endpoints-------------"""

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

@app.get("/users/me", response_model=UserResponse)
def get_current_user_info(current_user: Users = Depends(get_current_user)) -> UserResponse:
    return current_user


@app.get("/exercises", response_model=list[ExerciseResponse] , dependencies=[Depends(get_current_user)])
def get_exercises(db: Session = Depends(get_db_session)) -> list[ExerciseResponse]:
    exercises = db.query(Exercises).all()
    return exercises

@app.get("/exercises/{id}", response_model=ExerciseResponse , dependencies=[Depends(get_current_user)])
def get_exercise_by_id(id: int, db: Session = Depends(get_db_session)) -> ExerciseResponse:
    exercise = db.get(Exercises, id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


"""-------------post endpoints-------------"""

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
    return user

@app.post("/auth/login" , response_model = TokenResponse)
def login_user(payload: LoginRequest , db: Session = Depends(get_db_session)) -> TokenResponse:
    user = db.query(Users).filter(Users.email == payload.email).first()
    if not verify_email_format(payload.email):
        error(code=422, message="Invalid email format")
    if not user:
        error(code=401, message="Invalid email or password")
    if not verify_password(payload.password, user.password_hash):
        error(code=401, message="Invalid email or password")
    access_token = create_access_token(user.id)
    return TokenResponse(access_token=access_token)

def error(code = 500, message = "Internal Server Error"):
    raise HTTPException(status_code=code, detail=message)


