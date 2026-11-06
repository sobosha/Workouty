from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db import get_db_session
from app.models import Users
from app.tokens import decode_access_token


bareer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bareer_scheme), db: Session = Depends(get_db_session)) -> Users:
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid token" , headers={"WWW-Authenticate": "Bearer"})
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    
    return user