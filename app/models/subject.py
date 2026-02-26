from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    stage_id = Column(Integer, ForeignKey("stages.id"))
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True)

    stage = relationship("Stage", backref="subjects")
    branch = relationship("Branch", backref="subjects")
