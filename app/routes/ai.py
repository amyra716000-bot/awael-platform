import os
import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_user
from app.core.subscription_checker import check_ai_access

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/ask")
def ask_ai(
    question: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="OpenRouter API key not found")

    # فحص الاشتراك
    subscription, plan = check_ai_access(db, current_user)

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://awael-platform-production-6101.up.railway.app",
        "X-Title": "Awael Platform"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    result = response.json()

    try:
        ai_answer = result["choices"][0]["message"]["content"]
    except:
        raise HTTPException(status_code=500, detail="Invalid AI response")

    # زيادة العداد
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
