from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database.session import get_db
from app.models.leaderboard import Leaderboard
from app.core.security import get_current_user

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/top10")
def get_top_10(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    top_users = (
        db.query(Leaderboard)
        .order_by(desc(Leaderboard.total_score))
        .limit(10)
        .all()
    )

    return top_users
