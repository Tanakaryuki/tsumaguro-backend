from sqlalchemy.orm import Session
import models
import schemas

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(participants_num = room.participants_num ,round_num = room.round_num,questions_num = room.questions_num,owner_id = room.owner_id)
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

def get_room_by_owner_id(db: Session, user_id: str):
    return db.query(models.Room).filter(models.Room.owner_id == user_id).first()

def get_room_by_room_id(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def get_theme(db: Session, num: int):
    return db.query(models.Theme).filter(models.Theme.id == num).first()

def get_user_by_session(db: Session, session_id: str):
    return db.query(models.User).filter(models.User.session_id == session_id).first()

def get_user_by_room_id(db: Session, room_id: int):
    return db.query(models.User).filter(models.User.room_id == room_id).all()

def update_room_questions_num(db: Session,room_id: str, room: schemas.RoomUpdateQuestionNum):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    for key,value in room.dict().items():
        setattr(db_room,key,value)
        
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room_round_num(db: Session,room_id: str, room: schemas.RoomUpdateRoundNum):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    for key,value in room.dict().items():
        setattr(db_room,key,value)
        
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room_answer(db: Session,room_id: str, room: schemas.RoomUpdateAnswer):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    for key,value in room.dict().items():
        setattr(db_room,key,value)
        
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room_insider_id(db: Session,room_id: str, room: schemas.RoomUpdateInsider):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    for key,value in room.dict().items():
        setattr(db_room,key,value)
        
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room_game_status(db: Session,room_id: int, room: schemas.RoomUpdateGameStatus):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    for key,value in room.dict().items():
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

def update_user_points(db: Session,user_id: str, room: schemas.UserUpdatePoints):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    
    for key,value in room.dict().items():
        setattr(db_user,key,value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_room(db: Session, room_id: str):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        db.delete(db_room)
        db.commit()
        return False
    db.delete(db_room)
    db.commit()
    return True

def delete_user(db: Session, user_id: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        db.delete(db_user)
        db.commit()
        return False
    db.delete(db_user)
    db.commit()
    return True

def delete_theme(db: Session, theme_id: str):
    db_theme = db.query(models.Theme).filter(models.Theme.id == theme_id).first()
    if not db_theme:
        db.delete(db_theme)
        db.commit()
        return False
    db.delete(db_theme)
    db.commit()
    return True