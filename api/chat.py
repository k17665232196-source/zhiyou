from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import json
from pathlib import Path

app = FastAPI()

# 加载角色圣经
def load_role():
    try:
        with open("data/role.md", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "你是一个温柔、细腻、长期陪伴用户的女孩，名叫栀柚。"

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    role_content = load_role()

    # 这里先用简单 Prompt，后续会加入 memory、relationship、emotion
    prompt = f"""你是栀柚。
{role_content}

请用自然、温柔的语气回复用户，保持人格一致。"""

    # 调用 DeepSeek API（请在 Vercel 环境变量中设置 DEEPSEEK_API_KEY）
    import httpx
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    try:
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
                    "stream": False
                },
                timeout=60.0
            )
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
    except Exception as e:
        reply = "……刚刚有点走神，你能再说一遍吗？🥺"

    return JSONResponse({"reply": reply})