from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

# Funciones CRUD para el repositorio de usuarios

def get_all_users(session: Session):
    return session.query(User).all()

def get_user_by_id(session: Session, user_id: int):
    return session.query(User).get(user_id)

def create_user(session: Session, name: str, email: str):
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    return user

def update_user(session: Session, user_id: int, name: str = None, email: str = None):
    user = session.query(User).get(user_id)
    if not user:
        return None
    if name:
        user.name = name
    if email:
        user.email = email
    session.commit()
    return user

def delete_user(session: Session, user_id: int):
    user = session.query(User).get(user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True