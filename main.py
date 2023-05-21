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
import openai
import json
from models import User

QQ = []

openai.api_key = "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"

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

CHATGPT_API_URL = "https://api.openai.com/v1/chat/completions"  # ChatGPTAPIのエンドポイントURL
API_KEY = "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"  # OpenAI APIキー

def get_chatgpt(content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "ChatGPTへの指示"},
            {"role": "user", "content": content}
        ]
    )
    return response["choices"][0]["message"]["content"]

@app.get("/")
async def read_root():
    return {"Hello": random.random()}

@app.post("/create_user")
def create_parent_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    # db_user = crud.get_user_by_session(db,session_id=user.session_id,)
    # if db_user:
    #     raise HTTPException(status_code=404, detail="User alreadty registered")
    return crud.create_parent_user(db, user)

@app.post("/create_room")
def create_room(room: schemas.RoomCreate,db: Session = Depends(get_db)):
    db_room = crud.get_room_by_owner_id(db, room.owner_id)
    if db_room:
        raise HTTPException(status_code=404, detail="Room alreadty registered")
    db_room = crud.create_room(db, room)
    return crud.update_user_room_id(db, room.owner_id, db_room.id)

@app.get("/room/{room_id}")
def join_room_1(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_room_id(db, room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="This room is not exist")
    return db_room

@app.post("/room/{room_id}")
def create_child_user(room_id: int, user: schemas.UserCreate,db: Session = Depends(get_db)):
    db_user = crud.get_user_by_session(db, user.session_id,)
    if db_user:
        raise HTTPException(status_code=404, detail="User alreadty registered")
    return crud.create_child_user(db, user, room_id)

@app.get("/waiting/{room_id}")
def read_participants(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_room_id(db, room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="This room is not exist")
    return crud.get_user_by_room_id(db, room_id)

@app.post("/waiting/{room_id}")
def casting_1(room_id: int, db: Session = Depends(get_db)):
    db_theme = crud.get_theme(db, random.randint(1, 3))
    users = crud.get_user_by_room_id(db, room_id)
    users = users[random.randint(0, len(users) - 1)]
    insider = users.id
    theme = db_theme.name
    genre = db_theme.genre
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

@app.post("/position/{room_id}")
def casting_3(room_id: int, db: Session = Depends(get_db)):
    return  crud.update_room_game_status(db, room_id, 2)












@app.post("/questioning/{room_id}")
def create_question(room_id: int, question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_q = crud.get_question_by_room_id_and_question_round_question_num(db, room_id, question.question_round, question.question_num)
    crud.create_question(db, question, room_id, (len(db_q) + 1))
    db_room = crud.get_room_by_room_id(db, room_id)
    participants_num = db_room.participants_num

    if (len(db_q) + 1) == participants_num :

        contents = """
        インサイダーゲームに協力してください
        以下の全ての質問に対して個別に「はい」か「いいえ」か「分からない」のどれかで回答してください
        回答は一般的な常識で行ってください
        「はい」の場合Y,「いいえ」の場合N,「分からない」の場合Kと返してください
        返す際は以下のようなjson形式で返答してください
        {
            "1": "N",
            "2": "K",
            "3": "K"
        }
        Y,N,K以外で回答をすると無実の人間が被害に遭うので余計なことは発言しないでください

        お題:"""

        theme = crud.get_room_by_room_id(db, room_id)
        contents += theme.answer
        contents += """
        
        """

        for i in range(participants_num):
            Q = crud.get_question_by_room_id_and_question_round_question_num_and_number(db, room_id, question.question_round, question.question_num, number=i+1)
            contents += str(Q.number) + ", " + Q.question + "\n        "
        
        reaponse = get_chatgpt(contents)

        dic = json.loads(reaponse)

        global QQ

        db_room = crud.get_room_by_room_id(db, room_id)
        db_room = crud.update_room_questions_num(db, room_id, db_room.questions_num - 1)

        if db_room.questions_num == 0:
            crud.update_room_game_status(db, room_id, 3)

        try:
            for i in range(participants_num):
                QQQ = {"user_id":"", "q":"", "tf":""}
                QQQ["user_id"] = str(crud.get_question_by_room_id_and_question_round_question_num_and_number(db, room_id, question.question_round, question.question_num, number=i+1).user_id)
                QQQ["q"] = str(crud.get_question_by_room_id_and_question_round_question_num_and_number(db, room_id, question.question_round, question.question_num, number=i+1).question)
                QQQ["tf"] = dic[str(i + 1)]
                QQ.append(QQQ)
            return QQ
        except:
            pass

            
        print(contents)
    return crud.get_room_by_room_id(db, room_id)

@app.get("/questioning/{room_id}")
def get_question(room_id: int, round_num: int, questions_num: int, db: Session = Depends(get_db)):
    #return crud.get_room_by_room_id(db, room_id)
    global QQ
    return QQ

@app.post("/answering/{room_id}")
def check_answer(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_room_id(db, room_id)
    #ChatGPTに答えを投げる

    contents = """
    インサイダーゲームのお題はチョコレートでした
    答えとお題が同じか判断してください
    カタカナや英語表記や短縮形なども正解といえます
    「はい」の場合Y,「いいえ」の場合Nで回答してください

    答え:チョコ
    """

    return  crud.update_room_game_status(db, room_id, 4)

@app.get("/answering/{room_id}")
def get_yes_or_no(room_id: int, db: Session = Depends(get_db)):
    pass

@app.post("/register_theme")
def register_theme(theme: schemas.ThemeCreate, db: Session = Depends(get_db)):
    return crud.create_theme(db, theme = theme)
