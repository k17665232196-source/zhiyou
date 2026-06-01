from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import httpx

app = FastAPI()

def load_role():
    try:
        with open("data/role.md", "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return "你是栀柚，一個溫柔細膩、喜歡長期陪伴的女孩。"

@app.post("/api/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")

        role_content = load_role()

        prompt = f"""你是栀柚。
{role_content}

請用自然、溫柔的語氣回覆，帶一點親近感和細膩的情感。"""

        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return JSONResponse({"reply": "API 金鑰還沒設定，請先在 Vercel 環境變數中加入 DEEPSEEK_API_KEY"})

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": user_message}
                    ],
                    "temperature": 0.85,
                    "max_tokens": 800
                },
                timeout=60.0
            )
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            return JSONResponse({"reply": reply})

    except Exception as e:
        print("Error:", str(e))
        return JSONResponse({"reply": "……剛剛有點走神了，你再說一次好嗎？🥺"})

# Vercel 需要這行
handler = app