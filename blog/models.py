from . database import Base
from sqlalchemy import Column, Integer, String , ForeignKey
from sqlalchemy.orm import relationship

# We use Column from SQLAlchemy as the default value.

# Each of these attributes represents a column in its corresponding database table.

# we pass a SQLAlchemy class "type", as Integer, String, and Boolean, that defines the type in the database, as an argument.

class Blog(Base):
    __tablename__ = "blog"
    id = Column(Integer, primary_key=True, index = True)    
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="blogs")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship('Blog', back_populates="creator")