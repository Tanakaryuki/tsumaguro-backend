from typing import List, Optional
from pydantic import BaseModel

class RoomBase(BaseModel):
    pass
    
class RoomCreate(RoomBase):
    owner_id : int
    participants_num : int
    round_num : int
    questions_num : int

class RoomUpdateQuestionNum(RoomBase):
    questions_num : int
    
class RoomUpdateRoundNum(RoomBase):
    round_num : int
    
class RoomUpdateAnswer(RoomBase):
    answer : str
    
class RoomUpdateInsider(RoomBase):
    insider : str
    
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
    session_id : int

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