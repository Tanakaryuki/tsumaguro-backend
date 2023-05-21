from typing import List, Optional
from pydantic import BaseModel

class RoomBase(BaseModel):
    pass
    
class RoomCreate(RoomBase):
    owner_id : int
    participants_num : int
    round_num : int
    remaining_questions_num : int

class RoomUpdateQuestionNum(RoomBase):
    questions_num : int
    
class RoomUpdateRoundNum(RoomBase):
    round_num : int
    
class RoomUpdateAnswer(RoomBase):
    answer : str
    
class RoomUpdateInsider(RoomBase):
    insider : int
    
class RoomUpdateGameStatus(RoomBase):
    game_status : int

class Room(RoomBase):
    id : int
    answer : str
    insider_id : int
    game_status : int
    
    class Config:
        orm_mode = True
        
class UserBase(BaseModel):
    user_name : str
    
class UserCreate(UserBase):
    session_id : str

class UserUpdateRoomId(UserBase):
    room_id : int

class UserUpdatePoints(UserBase):
    points : int

class User(UserBase):
    room_id : int
    id : str
    points : int
    
    class Config:
        orm_mode = True
    
class ThemeBase(BaseModel):
    name : str
    genre : str
    
class ThemeCreate(ThemeBase):
    pass

class Theme(ThemeBase):
    id : int
    
    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    question : str
    room_id : int
    user_id : int
    question_round : int
    question_num : int

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id : int

    class Config:
        orm_mode = True

class VoteBase(BaseModel):
    room_id : int
    user_id : int
    vote_user_id: int

class VoteCreate(VoteBase):
    pass

class Vote(VoteBase):
    id : int

    class Config:
        orm_mode = True
