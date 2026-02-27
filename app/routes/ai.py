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
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="API key not found")

    subscription, plan = check_ai_access(db, current_user)

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  # موديل مجاني ومستقر
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # 🔥 نطبع الرد الكامل حتى نعرف الخطأ الحقيقي
    print("STATUS CODE:", response.status_code)
    print("FULL RESPONSE:", response.text)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    result = response.json()

    if "choices" not in result:
        raise HTTPException(status_code=500, detail=result)

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
