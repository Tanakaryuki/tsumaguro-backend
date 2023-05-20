from typing import List
from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
#from databases import Database
from fastapi.middleware.cors import CORSMiddleware
import crud
import models
import schemas
from database import SessionLocal, engine
import random

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
#database = Database('sqlite:///tasks.db')

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": random.random()}

@app.post("/create_user")
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    db_user = crud.get_user_by_session(db,session_id=user.session_id,)
    if db_user:
        raise HTTPException(status_code=404, detail="User alreadty registered")
    return crud.create_user(db=db,user=user)

@app.post("/create_room")
def create_room(room: schemas.RoomCreate,db: Session = Depends(get_db)):
    db_room = crud.get_room(db,user_id=room.owner_id)
    if db_room:
        raise HTTPException(status_code=404, detail="Room alreadty registered")
    return crud.create_room(db=db,room=room)