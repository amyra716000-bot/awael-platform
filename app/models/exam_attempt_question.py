class ExamAttemptQuestion(Base):
    __tablename__ = "exam_attempt_questions"

    id = Column(Integer, primary_key=True)

    attempt_id = Column(
        Integer,
        ForeignKey("exam_attempts.id")
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id")
    )

    user_answer = Column(String)

    is_correct = Column(Boolean)

    attempt = relationship(
        "ExamAttempt",
        back_populates="questions"
    )

    question = relationship(
        "Question",
        back_populates="exam_attempt_questions"
    )
