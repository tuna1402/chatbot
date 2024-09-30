from fastapi import FastAPI, BackgroundTasks
import httpx
from pydantic import BaseModel, ValidationError
from typing import Dict, Literal, List

app = FastAPI()

class User(BaseModel):
    id: str

class UserRequest(BaseModel):
    user: User
    utterance: str
    callbackUrl: str
    lang: Literal["ko"]  
    timezone: Literal["Asia/Seoul"]

class SkillRequest(BaseModel):
    bot: Dict[str, str]
    userRequest: UserRequest

@app.get("/")
def main_post():
    return "for checking the connection"

@app.post("/user_requests")
async def skill_server(skills: SkillRequest, background_tasks: BackgroundTasks):
    
    print(skills)

    callback_answer = {
        "version" : "2.0",
        "useCallback" : True,
        "data": {
            "text" : "생각하고 있는 중이에요😘 \n15초 정도 소요될 거 같아요 기다려 주실래요?!"
        }
    }

    try:
        utterance = skills.userRequest.utterance
        callback_url = skills.userRequest.callbackUrl
        # 비동기 작업으로 GPT 응답 받는 작업을 백그라운드로 실행
        background_tasks.add_task(fetch_gpt_response, utterance, callback_url)
        
    except ValidationError as e:
        return {"error": str(e)}
    
    # 바로 callback_answer를 응답으로 반환
    return callback_answer

async def fetch_gpt_response(utterance: str, callback_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8001/gpt_responses", json={"utterance": utterance}, timeout=60.0)
        
        if response.status_code == 200:
            gpt_answer = response.json()            
            await client.post(callback_url, json={"gpt_response": gpt_answer})
        
        else:
            await client.post(callback_url, json={"error": "에러가 발생했습니다."})