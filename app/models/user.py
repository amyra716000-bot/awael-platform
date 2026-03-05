from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    xp_points = Column(Integer, default=0)
    level = Column(Integer, default=1)

    stage_id = Column(Integer, ForeignKey("stages.id"))

    stage = relationship("Stage")
    
    subscriptions = relationship("Subscription", back_populates="user")
