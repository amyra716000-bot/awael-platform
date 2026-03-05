from sqlalchemy import Column, Integer, ForeignKey, Float, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    stage_id = Column(
        Integer,
        ForeignKey("stages.id"),
        nullable=False
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False
    )

    # أعلى درجة حصل عليها الطالب
    highest_score = Column(Float, default=0)

    # متوسط درجات الطالب
    average_score = Column(Float, default=0)

    # عدد الامتحانات
    total_exams = Column(Integer, default=0)

    # مؤشر التنافس
    competitive_score = Column(Float, default=0)

    # =========================
    # العلاقات
    # =========================
    user = relationship("User", back_populates="leaderboards")
    stage = relationship("Stage")
    subject = relationship("Subject")

    # =========================
    # القيود
    # =========================
    __table_args__ = (

        # منع تكرار نفس المستخدم في نفس المادة
        UniqueConstraint(
            "user_id",
            "stage_id",
            "subject_id",
            name="unique_leaderboard_entry"
        ),

        # فهرس لتحسين الترتيب
        Index(
            "idx_leaderboard_competition",
            "stage_id",
            "subject_id",
            "competitive_score"
        ),
    )
