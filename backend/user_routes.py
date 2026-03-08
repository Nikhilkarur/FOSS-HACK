from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import Optional

import models
from database import get_db

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    dietary_preference: Optional[str] = None

class UserPreferencesUpdate(BaseModel):
    dietary_preference: str

class UserResponse(BaseModel):
    id: int
    username: str
    dietary_preference: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = models.User(
        username=user.username,
        dietary_preference=user.dietary_preference
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/users/{user_id}/preferences", response_model=UserResponse)
def update_user_preferences(user_id: int, prefs: UserPreferencesUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.dietary_preference = prefs.dietary_preference
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
