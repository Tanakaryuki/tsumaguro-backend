from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(String,primary_key = True,index = True)
    owner_id = Column(String,ForeignKey("users.id"),nullable = False)
    participants_num = Column(Integer,nullable = False)
    round_num = Column(Integer,nullable = False)
    questions_num = Column(Integer,nullable = False)
    answer = Column(String,default = "リンゴ")
    insider_id = Column(String,ForeignKey("users.id"),nullable = False)
    game_status = Column(Integer,default = 0)
    
    __table_args__ = (
        CheckConstraint('participants_num >= 3',name = 'check_participants_num'),
        CheckConstraint('round_num >= 1',name = 'check_round_num'),
        CheckConstraint('questions_num >= 3',name = 'check_questions_num')
    )
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(String,primary_key = True,index = True)
    session_id = Column(String,nullable = False)
    user_name = Column(String,default = "ユーザ名")
    room_id = Column(String,ForeignKey("rooms.id"),nullable = False)
    points = Column(Integer,default = 0)
    
class Theme(Base):
    __tablename__ = "themes"
    
    id = Column(String,primary_key = True,index = True)
    name = Column(String)
    genre = Column(String)
