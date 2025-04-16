from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from LLMHelper import EmailAnalysisAssistant
import uvicorn

app = FastAPI(title="LLM Analysis Service", description="提供邮件分析服务的API")

# 初始化EmailAnalysisAssistant实例
assistant = EmailAnalysisAssistant()

class EmailInfo(BaseModel):
    emailId: str
    subject: str
    processed: str
    processed_state: str
    error_message: str
    create_ticket: str
    ticket_id: str
    id: int

@app.post("/analyze_email", response_model=List[Dict[str, Any]])
async def analyze_email(email_info: EmailInfo):
    """
    分析失败的邮件并返回分析结果
    """
    try:
        # 将Pydantic模型转换为字典
        email_dict = email_info.dict()
        # 调用LLMHelper的分析方法
        result = assistant.analyze_failed_email(email_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 