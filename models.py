from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer,primary_key = True,index = True)
    owner_id = Column(Integer,nullable = False)
    participants_num = Column(Integer,nullable = False)
    round_num = Column(Integer,nullable = False)
    questions_num = Column(Integer, default = 0)
    remaining_questions_num = Column(Integer,nullable = False, default = 0)
    answer = Column(String,default = "リンゴ")
    genre = Column(String, default = "くだもの")
    insider_id = Column(Integer,nullable = False,default = "example")
    game_status = Column(Integer,default = 0)
    
    # __table_args__ = (
    #     CheckConstraint('participants_num >= 3',name = 'check_participants_num'),
    #     CheckConstraint('round_num >= 1',name = 'check_round_num'),
    #     CheckConstraint('remaining_questions_num >= 3',name = 'check_remaining_questions_num')
    # )
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key = True,index = True)
    session_id = Column(String)
    user_name = Column(Integer,default = "ユーザ名")
    room_id = Column(Integer,default = 0)
    points = Column(Integer,default = 0)
    
class Theme(Base):
    __tablename__ = "themes"
    
    id = Column(Integer,primary_key = True,index = True)
    name = Column(String)
    genre = Column(String)

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer,primary_key = True)
    question = Column(String)
    room_id = Column(Integer,default = 0)
    user_id = Column(Integer,default = 0)
    question_round = Column(Integer, default = 0)
    question_num = Column(Integer, default = 0)
