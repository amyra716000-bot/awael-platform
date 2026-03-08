from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Branch(Base):
    __tablename__ = "branches"

    # =========================
    # Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    stage_id = Column(
        Integer,
        ForeignKey("stages.id"),
        index=True
    )

    # =========================
    # Relationships
    # =========================

    stage = relationship(
        "Stage",
        back_populates="branches"
    )
