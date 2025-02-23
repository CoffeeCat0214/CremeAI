from fastapi import HTTPException
from typing import Any, Dict, Optional

class ChatbotException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.additional_info = additional_info or {}

class RateLimitExceeded(ChatbotException):
    def __init__(self, retry_after: int):
        super().__init__(
            status_code=429,
            detail="Rate limit exceeded",
            error_code="RATE_LIMIT_EXCEEDED",
            additional_info={"retry_after": retry_after}
        )

class InvalidCredentials(ChatbotException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid credentials",
            error_code="INVALID_CREDENTIALS"
        )

class AIServiceError(ChatbotException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=503,
            detail=f"AI Service error: {detail}",
            error_code="AI_SERVICE_ERROR"
        ) 