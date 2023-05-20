from typing import List, Optional
from pydantic import BaseModel

class RoomBase(BaseModel):
    pass
    
class RoomCreate(RoomBase):
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
    id : str
    owner_id : str
    answer : str
    insider_id : str
    game_status : int
    
    class Config:
        orm_mode = True
        
class UserBase(BaseModel):
    user_name : str
    
class UserCreate(UserBase):
    pass

class UserUpdatePoints(UserBase):
    points : int

class User(UserBase):
    id : str
    session_id : str
    room_id : str
    points : int
    
    class Config:
        orm_mode = True
    
class ThemeBase(BaseModel):
    name : str
    genre : str
    
class ThemeCreate(ThemeBase):
    pass

class Theme(ThemeBase):
    id : str
    
    class Config:
        orm_mode = True