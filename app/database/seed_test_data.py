from sqlalchemy.orm import Session
from app.models.stage import Stage
from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.section import Section
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.question_type import QuestionType
from app.models.exam_template import ExamTemplate


def seed_test_data(db: Session):

    # ======================
    # Stage
    # ======================

    stage = Stage(name="سادس اعدادي علمي")
    db.add(stage)
    db.commit()
    db.refresh(stage)

    # ======================
    # Subject
    # ======================

    subject = Subject(
        name="رياضيات",
        stage_id=stage.id
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)

    # ======================
    # Chapter
    # ======================

    chapter = Chapter(
        name="المصفوفات",
        subject_id=subject.id
    )
    db.add(chapter)
    db.commit()
    db.refresh(chapter)

    # ======================
    # Section
    # ======================

    section = Section(
        name="تعريف المصفوفة",
        chapter_id=chapter.id
    )
    db.add(section)
    db.commit()
    db.refresh(section)

    # ======================
    # Question Type
    # ======================

    qtype = QuestionType(name="اختيار من متعدد")
    db.add(qtype)
    db.commit()
    db.refresh(qtype)

    # ======================
    # Question
    # ======================

    question = Question(
        content="ما هو تعريف المصفوفة؟",
        answer="ترتيب منظم للأعداد",
        section_id=section.id,
        type_id=qtype.id,
        is_ministry=False,
        is_important=True
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    # ======================
    # Options
    # ======================

    options = [
        QuestionOption(
            question_id=question.id,
            text="ترتيب منظم للأعداد",
            is_correct=True,
            order=1
        ),
        QuestionOption(
            question_id=question.id,
            text="مجموعة عشوائية",
            is_correct=False,
            order=2
        ),
        QuestionOption(
            question_id=question.id,
            text="عدد صحيح",
            is_correct=False,
            order=3
        ),
        QuestionOption(
            question_id=question.id,
            text="معادلة",
            is_correct=False,
            order=4
        )
    ]

    db.add_all(options)
    db.commit()

    # ======================
    # Exam Template
    # ======================

    exam = ExamTemplate(
        name="اختبار تجريبي",
        type="daily",
        stage_id=stage.id,
        subject_id=subject.id,
        section_id=section.id,
        total_questions=1,
        duration_minutes=5,
        passing_score=50,
        is_active=True,
        attempt_limit=5,
        is_paid=False
    )

    db.add(exam)
    db.commit()
