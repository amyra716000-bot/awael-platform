import os
import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import get_current_user
from app.core.subscription_checker import check_ai_access

router = APIRouter(prefix="/ai", tags=["AI"])

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@router.post("/ask")
def ask_ai(
    question: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="API key not found")

    subscription, plan = check_ai_access(db, current_user)

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://01.up.railway.app",
        "X-Title": "Awael Platform",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    ai_answer = response.json()["choices"][0]["message"]["content"]

    if subscription:
        subscription.ai_used_today += 1
        remaining = plan.daily_ai_limit - subscription.ai_used_today
    else:
        current_user.free_ai_used += 1
        remaining = 5 - current_user.free_ai_used

    db.commit()

    return {
        "question": question,
        "answer": ai_answer,
        "remaining_today": remaining
    }
