from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import time

from services.chat_service import ChatService
from services.memory_service import MemoryService
from services.personality_service import PersonalityService
from services.monitoring_service import MonitoringService
from middleware.rate_limiter import RateLimiter
from middleware.validation import RequestValidationMiddleware
from exceptions import ChatbotException, AIServiceError, InvalidCredentials
from services.auth_service import AuthService
from services.webhook_service import WebhookService, WebhookConfig

load_dotenv()

app = FastAPI(title="Crème Brûlée Chatbot API")

# Initialize services
auth_service = AuthService()
monitoring_service = MonitoringService()
rate_limiter = RateLimiter()

# Initialize webhook service
webhook_service = WebhookService()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware
app.middleware("http")(RequestValidationMiddleware())

@app.middleware("http")
async def add_monitoring(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    await monitoring_service.log_api_metrics(
        endpoint=request.url.path,
        response_time=process_time,
        status_code=response.status_code,
        user_id=request.headers.get("X-User-ID", "anonymous")
    )
    
    return response

@app.exception_handler(ChatbotException)
async def chatbot_exception_handler(request: Request, exc: ChatbotException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.detail,
                "additional_info": exc.additional_info
            }
        }
    )

class ChatMessage(BaseModel):
    message: str
    platform: str

class ChatResponse(BaseModel):
    response: str
    decree: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    message: ChatMessage,
    request: Request,
    auth: dict = Depends(auth_service.verify_token)
):
    await rate_limiter.check_rate_limit(request)
    
    start_time = time.time()
    try:
        chat_service = ChatService()
        response = await chat_service.generate_response(
            user_id=auth['user_id'],
            message=message.message,
            platform=message.platform
        )
        
        process_time = (time.time() - start_time) * 1000
        await monitoring_service.log_chat_metrics(
            user_id=auth['user_id'],
            platform=message.platform,
            response_length=len(response["response"]),
            processing_time=process_time
        )
        
        return ChatResponse(**response)
    except Exception as e:
        raise AIServiceError(str(e))

@app.post("/auth/token")
async def get_token(platform: str, api_key: str):
    if api_key != settings.API_KEY:
        raise InvalidCredentials()
    
    token = auth_service.create_access_token(
        user_id=f"api-user-{platform}",
        platform=platform
    )
    return {"access_token": token, "token_type": "bearer"}

@app.post("/webhooks/register")
async def register_webhook(
    webhook: WebhookConfig,
    auth: dict = Depends(auth_service.verify_token)
):
    """Register a new webhook endpoint"""
    webhook_service.register_webhook(webhook)
    return {"status": "success", "message": "Webhook registered successfully"}

@app.delete("/webhooks/unregister")
async def unregister_webhook(
    url: str,
    auth: dict = Depends(auth_service.verify_token)
):
    """Unregister a webhook endpoint"""
    webhook_service.unregister_webhook(url)
    return {"status": "success", "message": "Webhook unregistered successfully"} 