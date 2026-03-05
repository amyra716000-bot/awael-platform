class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    template_id = Column(Integer, ForeignKey("exam_templates.id"))

    score = Column(Integer)

    user = relationship(
        "User",
        back_populates="exam_attempts"
    )

    questions = relationship(
        "ExamAttemptQuestion",
        back_populates="attempt",
        cascade="all, delete"
    )
