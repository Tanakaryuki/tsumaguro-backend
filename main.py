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
from models import User

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
def create_parent_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    # db_user = crud.get_user_by_session(db,session_id=user.session_id,)
    # if db_user:
    #     raise HTTPException(status_code=404, detail="User alreadty registered")
    return crud.create_parent_user(db=db,user=user)

@app.post("/create_room")
def create_room(room: schemas.RoomCreate,db: Session = Depends(get_db)):
    db_room = crud.get_room_by_owner_id(db,user_id=room.owner_id)
    if db_room:
        raise HTTPException(status_code=404, detail="Room alreadty registered")
    db_room = crud.create_room(db=db,room=room)
    return crud.update_user_room_id(db, user_id = room.owner_id, room_id = db_room.id)

@app.get("/room/{room_id}")
def join_room_1(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_room_id(db, room_id=room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="This room is not exist")
    return db_room

@app.post("/room/{room_id}")
def create_child_user(room_id: int, user: schemas.UserCreate,db: Session = Depends(get_db)):
    db_user = crud.get_user_by_session(db, session_id=user.session_id,)
    if db_user:
        raise HTTPException(status_code=404, detail="User alreadty registered")
    return crud.create_child_user(db=db,user=user, room_id = room_id)

@app.get("/waiting/{room_id}")
def read_participants(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_room_id(db, room_id=room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="This room is not exist")
    return crud.get_user_by_room_id(db, room_id = room_id)

@app.post("/waiting/{room_id}")
def casting_1(room_id: int, db: Session = Depends(get_db)):
    theme = crud.get_theme(db, random.randint(1, 10))
    users = crud.get_user_by_room_id(db, room_id)
    users = users[random.randint(0, len(users) - 1)]
    insider = users.id
    theme = theme.name
    genre = theme.genre
    room = crud.get_room_by_room_id(db, room_id)
    room = room.remaining_questions_num
    db_room = crud.update_room_answer(db, room_id, theme)
    db_room = crud.update_room_genre(db, room_id, genre)
    db_room = crud.update_room_insider_id(db, room_id, insider)
    crud.update_room_questions_num(db, room_id, room)
    return  crud.update_room_game_status(db, room_id, 1)

@app.get("/position/{room_id}")
def casting_2(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_room_id(db, room_id)
    return db_room

@app.post("/questioning/{room_id}")
def create_question(room_id: int, question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    crud.create_question(db = db, question=question, room_id = room_id)
    db_q = crud.get_room_by_room_id_and_question_num(db, room_id, question.question_num)
    db_q = len(db_q)
    participant_num = crud.get_room_by_room_id(db, room_id)
    participant_num = participant_num.participants_num

    if db_q == participant_num :

        #ChatGPTへ質問

        db_room = crud.get_room_by_room_id(db, room_id)
        db_room = db_room.questions_num
        db_room = crud.update_room_questions_num(db, room_id, db_room - 1)

        #if db_room.question == 0:
            
    
    return crud.get_room_by_room_id(db, room_id)

@app.get("/questioning/{room_id}")
def get_question(room_id: int, round_num: int, questions_num: int, db: Session = Depends(get_db)):
    return crud.get_room_by_room_id(db, room_id)

@app.post("/register_theme")
def register_theme(theme: schemas.ThemeCreate, db: Session = Depends(get_db)):
    return crud.create_theme(db, theme = theme)
