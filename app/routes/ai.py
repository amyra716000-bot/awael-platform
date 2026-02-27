from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import get_current_user
from app.core.subscription_checker import check_ai_access
from app.models.user import User
import requests
import os

router = APIRouter(prefix="/ai", tags=["AI"])

FREE_LIMIT = 5
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


@router.post("/ask")
def ask_ai(
    question: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    subscription, plan = check_ai_access(db, current_user)

    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "user", "content": question}
                ]
            }
        )

        data = response.json()

        if "choices" not in data:
            raise HTTPException(status_code=500, detail=str(data))

        ai_answer = data["choices"][0]["message"]["content"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # تحديث العداد
    if subscription:
        subscription.ai_used_today += 1
        remaining = plan.daily_ai_limit - subscription.ai_used_today
    else:
        current_user.free_ai_used += 1
        remaining = FREE_LIMIT - current_user.free_ai_used

    db.commit()

    return {
        "question": question,
        "answer": ai_answer,
        "remaining_today": remaining
    }
