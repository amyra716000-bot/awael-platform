from app.database.session import SessionLocal
from app.models.stage import Stage
from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.section import Section
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.question_type import QuestionType


def seed():

    db = SessionLocal()

    stage = Stage(name="السادس الاعدادي")
    db.add(stage)
    db.commit()
    db.refresh(stage)

    subject = Subject(
        name="الرياضيات",
        stage_id=stage.id
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)

    chapter = Chapter(
        name="الفصل الاول",
        subject_id=subject.id
    )
    db.add(chapter)
    db.commit()
    db.refresh(chapter)

    section = Section(
        name="اسئلة اختيار",
        type="multiple_choice",
        chapter_id=chapter.id,
        order=1
    )
    db.add(section)
    db.commit()
    db.refresh(section)

    qtype = QuestionType(name="mcq")
    db.add(qtype)
    db.commit()
    db.refresh(qtype)

    questions = [
        ("كم حاصل 2 + 2 ؟", ["3", "4", "5", "6"], 1),
        ("كم حاصل 5 × 3 ؟", ["10", "15", "20", "25"], 1),
        ("كم حاصل 10 ÷ 2 ؟", ["3", "4", "5", "6"], 2),
        ("كم حاصل 7 + 5 ؟", ["10", "11", "12", "13"], 2),
        ("كم حاصل 9 - 3 ؟", ["3", "5", "6", "7"], 2),
    ]

    for text, options, correct in questions:

        question = Question(
            content=text,
            answer=options[correct],
            section_id=section.id,
            type_id=qtype.id
        )

        db.add(question)
        db.commit()
        db.refresh(question)

        for i, opt in enumerate(options):
            option = QuestionOption(
                question_id=question.id,
                text=opt,
                is_correct=(i == correct),
                order=i
            )

            db.add(option)

        db.commit()

    db.close()

    print("TEST DATA INSERTED")


if __name__ == "__main__":
    seed()


