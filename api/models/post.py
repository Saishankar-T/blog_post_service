from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.lib.database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(String(500))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")
