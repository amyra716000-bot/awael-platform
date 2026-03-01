# =========================
# SOLVE QUESTION (Progress)
# =========================
@router.post("/solve/{question_id}")
def solve_question(
    question_id: int,
    is_correct: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1️⃣ التأكد من وجود السؤال
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # 2️⃣ جلب تقدم الطالب لهذا السيكشن
    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id,
        StudentProgress.section_id == question.section_id
    ).first()

    # 3️⃣ إذا أول محاولة لهذا السيكشن
    if progress is None:
        progress = StudentProgress(
            user_id=current_user.id,
            section_id=question.section_id,
            correct_answers=1 if is_correct else 0,
            total_attempts=1
        )
        db.add(progress)

    # 4️⃣ إذا موجود مسبقاً نحدث الإحصائيات
    else:
        progress.total_attempts += 1

        if is_correct:
            progress.correct_answers += 1

    # 5️⃣ حفظ التغييرات
    db.commit()

    return {
        "message": "Progress saved successfully",
        "total_attempts": progress.total_attempts,
        "correct_answers": progress.correct_answers
    }
