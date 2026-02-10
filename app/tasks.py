from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate
import jwt

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401,detail="Invalid token")

@router.get("/")
def list_tasks(token:str,db:Session = Depends(get_db)):
    user_id = get_current_user(token)
    tasks = db.query(Task).filter(Task.owner_id == user_id).all()
    return tasks

@router.post("/")
def create_tasks(task:TaskCreate,token:str,db: Session = Depends(get_db)):
    user_id = get_current_user(token)
    tasks = Task(title = task.title, description = task.description, owner_id = user_id)
    db.add(tasks)
    db.commit()
    return {"message":"Task created"}

@router.post("{task_id}")
def delete_task(task_id:int,token:str,db: Session = Depends(get_db)):
    user_id = get_current_user(token)
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message":"Task deleted"}

    