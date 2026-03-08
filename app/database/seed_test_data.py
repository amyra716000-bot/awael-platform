from app.database.session import SessionLocal

from app.models.stage import Stage
from app.models.branch import Branch
from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.section import Section
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.question_type import QuestionType
from app.models.exam_template import ExamTemplate


def seed():

    db = SessionLocal()

    # =========================
    # Stage
    # =========================
    stage = Stage(name="السادس الاعدادي")
    db.add(stage)
    db.commit()
    db.refresh(stage)

    # =========================
    # Branch
    # =========================
    branch = Branch(
        name="العلمي",
        stage_id=stage.id
    )

    db.add(branch)
    db.commit()

    # =========================
    # Subject
    # =========================
    subject = Subject(
        name="الرياضيات",
        stage_id=stage.id
    )

    db.add(subject)
    db.commit()
    db.refresh(subject)

    # =========================
    # Chapter
    # =========================
    chapter = Chapter(
        name="الفصل الاول",
        subject_id=subject.id
    )

    db.add(chapter)
    db.commit()
    db.refresh(chapter)

    # =========================
    # Section
    # =========================
    section = Section(
        name="اسئلة اختيار",
        type="multiple_choice",
        chapter_id=chapter.id,
        order=1
    )

    db.add(section)
    db.commit()
    db.refresh(section)

    # =========================
    # Question Type
    # =========================
    qtype = QuestionType(name="mcq")

    db.add(qtype)
    db.commit()
    db.refresh(qtype)

    # =========================
    # Questions
    # =========================

    questions_data = [

        ("كم حاصل 2 + 2 ؟", ["3", "4", "5", "6"], 1),
        ("كم حاصل 5 × 3 ؟", ["10", "15", "20", "25"], 1),
        ("كم حاصل 10 ÷ 2 ؟", ["3", "4", "5", "6"], 2),
        ("كم حاصل 7 + 5 ؟", ["10", "11", "12", "13"], 2),
        ("كم حاصل 9 - 3 ؟", ["3", "5", "6", "7"], 2),

    ]

    for text, options, correct in questions_data:

        question = Question(
            content=text,
            answer=options[correct],
            section_id=section.id,
            type_id=qtype.id
        )

        db.add(question)
        db.commit()
        db.refresh(question)

        for i, option in enumerate(options):

            db.add(
                QuestionOption(
                    question_id=question.id,
                    text=option,
                    is_correct=(i == correct),
                    order=i
                )
            )

        db.commit()

    # =========================
    # Exam Template
    # =========================

    exam = ExamTemplate(

        name="اختبار تجريبي",
        type="daily",

        stage_id=stage.id,
        subject_id=subject.id,
        section_id=section.id,

        total_questions=5,
        duration_minutes=5,
        passing_score=50,

        is_active=True,
        attempt_limit=5,
        is_paid=False

    )

    db.add(exam)
    db.commit()

    db.close()

    print("Seed Data Inserted Successfully")


if __name__ == "__main__":
    seed()
