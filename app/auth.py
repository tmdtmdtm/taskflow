from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate, UserLogin
import bcrypt
import datetime
import jwt

SECRET_KEY = 'your-secret-key'
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@router.post("/register")
def register(user:UserCreate, db: Session = Depends(get_db)):
    #既にメールが登録されていないかチェック
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = bcrypt.hashpw(user.password.encode(),bcrypt.gensalt())
    db_user = User(email = user.email, password_hash = hashed.decode())
    db.add(db_user)
    db.commit()

    return {"message":"User created"}

@router.post("/login")
def login(user:UserLogin,db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400,detail="Invalid credentials")
    
    #パスワード照合
    if not bcrypt.checkpw(user.password.encode(),db_user.password_hash.encode()):
        raise HTTPException(status_code=400,detail="Invalid credentials")

    #JWT発行
    payload ={
        "user_id": db_user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload,SECRET_KEY,algorithm="HS256")

    return {"access_token":token}



           
