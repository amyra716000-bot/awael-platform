import os
import json
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
        raise HTTPException(status_code=500, detail="API key not found")

    subscription, plan = check_ai_access(db, current_user)

    url = "https://openrouter.ai/api/v1/chat/completions"

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    headers = {}
    headers["Authorization"] = "Bearer " + api_key
    headers["Content-Type"] = "application/json"

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
        timeout=30
    )

    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    result = response.json()

    ai_answer = result["choices"][0]["message"]["content"]

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
