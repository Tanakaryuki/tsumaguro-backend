from sqlalchemy.orm import Session
import models
import schemas
from sqlalchemy import and_

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(participants_num = room.participants_num ,round_num = room.round_num,remaining_questions_num = room.remaining_questions_num,owner_id = room.owner_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def create_parent_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(session_id = user.session_id,user_name = user.user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_child_user(db: Session, user: schemas.UserCreate, room_id: int):
    db_user = models.User(session_id = user.session_id,user_name = user.user_name,room_id = room_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_theme(db: Session, theme: schemas.ThemeCreate):
    db_theme = models.Theme(name = theme.name,genre = theme.genre)
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme

def create_question(db: Session, question: schemas.QuestionCreate, room_id: int, number: int):
    db_question = models.Question(number = number, question = question.question, room_id = room_id, user_id = question.user_id, question_round = question.question_round, question_num = question.question_num)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def create_vote(db: Session, vote: schemas.VoteCreate, room_id: int):
    db_vote = models.Vote(room_id = room_id, user_id = vote.user_id)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote

def get_room_by_owner_id(db: Session, user_id: str):
    return db.query(models.Room).filter(models.Room.owner_id == user_id).first()

def get_room_by_room_id(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def get_room_by_room_id_and_question_num(db: Session, room_id: int, question_num: int):
    return db.query(models.Question).filter(and_(models.Question.room_id == room_id , models.Question.question_num == question_num)).all()

def get_question_by_room_id_and_question_round_question_num(db: Session, room_id: int,question_round: int, question_num: int):
    return db.query(models.Question).filter(and_(models.Question.room_id == room_id , models.Question.question_num == question_num)).all()

def get_question_by_room_id_and_question_round_question_num_and_number(db: Session, room_id: int,question_round: int, question_num: int,number: int):
    return db.query(models.Question).filter(and_(models.Question.room_id == room_id , models.Question.question_num == question_num,models.Question.number == number)).first()

def get_theme(db: Session, num: int):
    return db.query(models.Theme).filter(models.Theme.id == num).first()

def get_question(db: Session, room_id: int, question_round: int, question_num: int):
    return db.query(models.Question).filter(and_(models.Question.room_id == room_id , models.Question.question_round == question_round , models.Question.question_num == question_num)).first()

def get_user_by_session(db: Session, session_id: str):
    return db.query(models.User).filter(models.User.session_id == session_id).first()

def get_user_name_by_user_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first().user_name

def get_user_name_by_room_id(db: Session, room_id: int):
    return db.query(models.User).filter(models.User.room_id == room_id).all()

def get_user_by_room_id(db: Session, room_id: int):
    return db.query(models.User).filter(models.User.room_id == room_id).all()

def get_vote_by_room_id(db: Session, room_id: int):
    return db.query(models.Vote).filter(models.Vote.room_id == room_id).all()

def update_room_questions_num(db: Session, room_id: int, questions_num: int):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    key = "questions_num"
    value = questions_num
    setattr(db_room,key,value)
        
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room_round_num(db: Session,room_id: int, room: schemas.RoomUpdateRoundNum):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    for key,value in room.dict().items():
        setattr(db_room,key,value)
        
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room_answer(db: Session, room_id: int, answer: str):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    key = "answer"
    value = answer
    setattr(db_room,key,value)
        
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room_genre(db: Session, room_id: int, genre: str):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    key = "genre"
    value = genre
    setattr(db_room,key,value)
        
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room_insider_id(db: Session, room_id: int, insider_id: int):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    key = "insider_id"
    value = insider_id
    setattr(db_room,key,value)
        
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room_game_status(db: Session,room_id: int, game_status: int):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    key = "game_status"
    value = game_status
    setattr(db_room,key,value)
        
    db.commit()
    db.refresh(db_room)
    return db_room

def update_user_room_id(db: Session,user_id: int, room_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    
    key = "room_id"
    value = room_id
    setattr(db_user,key,value)
        
    db.commit()
    db.refresh(db_user)
    return db_user   

def update_user_points(db: Session,user_id: int, room: schemas.UserUpdatePoints):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    
    for key,value in room.dict().items():
        setattr(db_user,key,value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_room(db: Session, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        db.delete(db_room)
        db.commit()
        return False
    db.delete(db_room)
    db.commit()
    return True

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        db.delete(db_user)
        db.commit()
        return False
    db.delete(db_user)
    db.commit()
    return True

def delete_theme(db: Session, theme_id: int):
    db_theme = db.query(models.Theme).filter(models.Theme.id == theme_id).first()
    if not db_theme:
        db.delete(db_theme)
        db.commit()
        return False
    db.delete(db_theme)
    db.commit()
    return True