from sqlalchemy.orm import Session
from app.models.stage import Stage
from app.models.question_type import QuestionType
from app.models.subject import Subject


def seed_data(db: Session):

    # =====================
    # المراحل الدراسية
    # =====================

    if db.query(Stage).count() == 0:

        stages = [
            Stage(name="سادس ابتدائي"),
            Stage(name="ثالث متوسط"),
            Stage(name="سادس اعدادي علمي"),
            Stage(name="سادس اعدادي ادبي")
        ]

        db.add_all(stages)
        db.commit()

    # =====================
    # أنواع الأسئلة
    # =====================

    if db.query(QuestionType).count() == 0:

        types = [
            QuestionType(name="اختيار من متعدد"),
            QuestionType(name="صح وخطأ"),
            QuestionType(name="فراغات"),
            QuestionType(name="مقالي")
        ]

        db.add_all(types)
        db.commit()

    # =====================
    # المواد
    # =====================

    if db.query(Subject).count() == 0:

        subjects = [

            Subject(name="رياضيات", stage_id=1),
            Subject(name="علوم", stage_id=1),
            Subject(name="عربي", stage_id=1),

            Subject(name="رياضيات", stage_id=2),
            Subject(name="فيزياء", stage_id=2),
            Subject(name="كيمياء", stage_id=2),

            Subject(name="رياضيات", stage_id=3),
            Subject(name="فيزياء", stage_id=3),
            Subject(name="كيمياء", stage_id=3),
            Subject(name="احياء", stage_id=3),

            Subject(name="تاريخ", stage_id=4),
            Subject(name="جغرافية", stage_id=4),
            Subject(name="اقتصاد", stage_id=4)

        ]

        db.add_all(subjects)
        db.commit()
