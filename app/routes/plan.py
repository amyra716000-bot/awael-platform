from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.plan import Plan
from app.schemas.plan import PlanCreate, PlanUpdate, PlanResponse
from app.core.security import get_current_admin

router = APIRouter(prefix="/plans", tags=["Plans"])


# إنشاء خطة (Admin فقط)
@router.post("/", response_model=PlanResponse)
def create_plan(
    plan: PlanCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    new_plan = Plan(**plan.dict())
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan


# عرض جميع الخطط (للجميع)
@router.get("/", response_model=list[PlanResponse])
def get_plans(db: Session = Depends(get_db)):
    return db.query(Plan).all()


# تعديل خطة (Admin فقط)
@router.put("/{plan_id}", response_model=PlanResponse)
def update_plan(
    plan_id: int,
    plan: PlanUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    for key, value in plan.dict(exclude_unset=True).items():
        setattr(db_plan, key, value)

    db.commit()
    db.refresh(db_plan)

    return db_plan


# حذف خطة (Admin فقط)
@router.delete("/{plan_id}")
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    db.delete(db_plan)
    db.commit()

    return {"message": "Plan deleted successfully"}
