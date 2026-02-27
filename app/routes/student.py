from fastapi import Query


@router.get("/questions/{section_id}")
def get_questions(
    section_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    is_ministry: bool | None = None,
    is_important: bool | None = None,
    ministry_year: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # فحص الاشتراك (حماية المحتوى)
    subscription, plan = check_ai_access(db, current_user)

    query = db.query(Question).filter(Question.section_id == section_id)

    # فلترة اختيارية
    if is_ministry is not None:
        query = query.filter(Question.is_ministry == is_ministry)

    if is_important is not None:
        query = query.filter(Question.is_important == is_important)

    if ministry_year is not None:
        query = query.filter(Question.ministry_year == ministry_year)

    total = query.count()

    questions = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": questions
    }
