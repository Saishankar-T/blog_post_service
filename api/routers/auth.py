from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.lib.jwt_handler import create_access_token
from api.models.user import User
from api.lib.database import get_db
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid password")
        # If user exists and password is correct, return a new token 
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    
    # Creates new user if username doesn't exist in database
    new_user = User(username=username, hashed_password=get_password_hash(password))
    db.add(new_user)
    db.commit()
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
