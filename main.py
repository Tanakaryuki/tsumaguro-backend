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
from pydantic import BaseModel


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


class Answer(BaseModel):
    name : str

class Vote(BaseModel):
    pass

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

        for i in range(participants_num):
            QQQ = {"user_name":"", "q":"", "tf":""}
            user_id = str(crud.get_question_by_room_id_and_question_round_question_num_and_number(db, room_id, question.question_round, question.question_num, number=i+1).user_id)
            QQQ["user_name"] = crud.get_user_name_by_user_id(db, user_id)
            QQQ["q"] = str(crud.get_question_by_room_id_and_question_round_question_num_and_number(db, room_id, question.question_round, question.question_num, number=i+1).question)
            QQQ["tf"] = dic[str(i + 1)]
            QQ.append(QQQ)
        return QQ

    return crud.get_room_by_room_id(db, room_id)

@app.get("/questioning/{room_id}")
def get_question(room_id: int, round_num: int, questions_num: int, db: Session = Depends(get_db)):
    #return crud.get_room_by_room_id(db, room_id)
    global QQ
    return QQ

@app.post("/answering/{room_id}")
def check_answer(room_id: int,answer: Answer,db: Session = Depends(get_db)):
    db_room = crud.get_room_by_room_id(db, room_id)
    #ChatGPTに答えを投げる

    contents = """
    インサイダーゲームのお題は""" + db_room.answer + """でした
    プレイヤーの回答とお題が同じか判断してください
    カタカナや英語表記や短縮形なども正解といえます
    「はい」の場合Y,「いいえ」の場合Nで回答してください

    回答：""" + answer.name


    reaponse = get_chatgpt(contents)

    try:
        if reaponse == "Y" or reaponse == "\"Y\"" :
            return  crud.update_room_game_status(db, room_id, 4)
        elif reaponse == "N" or reaponse == "\"N\"" :
            return  crud.update_room_game_status(db, room_id, 6)
        else :
            reaponse = get_chatgpt(contents)
            try:
                if reaponse == "Y" or reaponse == "\"Y\"" :
                    return  crud.update_room_game_status(db, room_id, 4)
                elif reaponse == "N" or reaponse == "\"N\"" :
                    return  crud.update_room_game_status(db, room_id, 6)
                else :
                    return crud.update_room_game_status(db, room_id, 6)
            except:
                pass
    except:
        pass

@app.get("/answering/{room_id}")
def get_yes_or_no(room_id: int, db: Session = Depends(get_db)):
    return crud.get_room_by_room_id(db, room_id)

@app.get("/voting/{room_id}")
def voting(room_id: int, db: Session = Depends(get_db)):
    users = crud.get_user_name_by_room_id(db, room_id)
    player_list = []
    for i in range(len(users)) :
        player_list_dic = {}
        user_name = users[i].user_name
        user_id = users[i].id
        player_list_dic["user_id"] = user_id
        player_list_dic["user_name"] = user_name
        player_list.append(player_list_dic)
    return player_list

@app.post("/voting/{room_id}")
def counting_vote(room_id: int, vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    crud.create_vote(db, vote, room_id)
    db_room = crud.get_room_by_room_id(db, room_id)
    person_num = db_room.participants_num
    votes = crud.get_vote_by_room_id(db, room_id)
    vote_list = []
    if len(votes) == person_num :
        for i in range(person_num) :
            vote_list.append(votes[i].vote_user_id)
        max = vote_list[0]
        max_num = 0
        for i in range(len(vote_list)):
            if max < vote_list[i]:
                max = vote_list[i]
                max_num = i
        next_max = vote_list[(max_num + 1) % len(vote_list)]
        for i in range(len(vote_list)):
            if i !=max_num:
                if next_max < vote_list[i]:
                    next_max = vote_list[i]
                    next_max_num = i
        if vote_list[max_num] == vote_list[next_max_num]:
            print("Lose")
            crud.update_room_questions_num(db,room_id=room_id,questions_num=0)
        else:
            print("もっとも疑われているのは")
            db_room = crud.get_room_by_room_id(db, room_id)
            if db_room.insider_id == vote_list[max_num].id :
                crud.update_room_questions_num(db,room_id=room_id,questions_num=1)
            else:
                crud.update_room_questions_num(db,room_id=room_id,questions_num=2)

        return 0



@app.post("/register_theme")
def register_theme(theme: schemas.ThemeCreate, db: Session = Depends(get_db)):
    return crud.create_theme(db, theme = theme)
