# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router
from app.tasks import router as tasks_router

app = FastAPI()

app.add_middleware( CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"], )

app.include_router(auth_router,prefix="/auth")
app.include_router(tasks_router,prefix="/tasks")

@app.get("/")
def read_root():
    return {"message": "TaskFlow API is running"}