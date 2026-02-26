from sqlalchemy import Column, Integer, String
from app.database.session import Base


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    branch = Column(String, nullable=True)  # علمي او ادبي
