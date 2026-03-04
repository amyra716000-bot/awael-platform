from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Text
from sqlalchemy.orm import relationship
from app.database.session import Base


class ExamAttemptQuestion(Base):
    __tablename__ = "exam_attempt_questions"

    id = Column(Integer, primary_key=True, index=True)

    # المحاولة المرتبط بها السؤال
    exam_attempt_id = Column(
        Integer,
        ForeignKey("exam_attempts.id", ondelete="CASCADE"),
        nullable=False
    )

    # نص السؤال
    question_text = Column(Text, nullable=False)

    # نوع السؤال
    question_type = Column(String, nullable=False)

    # الخيارات (في حالة الاختيارات)
    options_json = Column(Text, nullable=True)

    # الجواب الصحيح
    correct_answer = Column(String, nullable=False)

    # درجة السؤال
    question_degree = Column(Integer, default=1)

    # إجابة الطالب
    selected_answer = Column(String, nullable=True)

    # هل الإجابة صحيحة
    is_correct = Column(Boolean, nullable=True)

    # العلاقة مع محاولة الامتحان
    exam_attempt = relationship(
        "ExamAttempt",
        back_populates="questions"
    )
