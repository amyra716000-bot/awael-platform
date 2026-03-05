from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.plan import Plan
from app.models.subscription import Subscription
from app.schemas.plan import PlanCreate, PlanUpdate, PlanResponse
from app.core.security import get_current_admin

router = APIRouter(prefix="/plans", tags=["Plans"])


# =========================
# CREATE PLAN (ADMIN)
# =========================
@router.post("/", response_model=PlanResponse)
def create_plan(
    plan: PlanCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    existing = db.query(Plan).filter(
        Plan.name == plan.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Plan already exists"
        )

    new_plan = Plan(**plan.dict())

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return new_plan


# =========================
# GET ALL PLANS
# =========================
@router.get("/", response_model=list[PlanResponse])
def get_plans(
    db: Session = Depends(get_db)
):

    plans = db.query(Plan).all()

    return plans


# =========================
# UPDATE PLAN (ADMIN)
# =========================
@router.put("/{plan_id}", response_model=PlanResponse)
def update_plan(
    plan_id: int,
    plan: PlanUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    db_plan = db.query(Plan).filter(
        Plan.id == plan_id
    ).first()

    if not db_plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    for key, value in plan.dict(exclude_unset=True).items():
        setattr(db_plan, key, value)

    db.commit()
    db.refresh(db_plan)

    return db_plan


# =========================
# DELETE PLAN (ADMIN)
# =========================
@router.delete("/{plan_id}")
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    db_plan = db.query(Plan).filter(
        Plan.id == plan_id
    ).first()

    if not db_plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    # منع حذف خطة مستخدمة
    used = db.query(Subscription).filter(
        Subscription.plan_id == plan_id
    ).first()

    if used:
        raise HTTPException(
            status_code=400,
            detail="Plan is used by subscriptions"
        )

    db.delete(db_plan)
    db.commit()

    return {
        "message": "Plan deleted successfully"
        }
