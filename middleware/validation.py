from fastapi import Request
from typing import Callable, Awaitable
from ..exceptions import ChatbotException
import json

class RequestValidationMiddleware:
    async def __call__(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[str]]
    ):
        try:
            # Validate content type for POST requests
            if request.method == "POST":
                content_type = request.headers.get("content-type", "")
                if not content_type.startswith("application/json"):
                    raise ChatbotException(
                        status_code=415,
                        detail="Content type must be application/json",
                        error_code="INVALID_CONTENT_TYPE"
                    )

            # Validate request body size
            if request.headers.get("content-length"):
                content_length = int(request.headers.get("content-length", 0))
                if content_length > 1024 * 1024:  # 1MB limit
                    raise ChatbotException(
                        status_code=413,
                        detail="Request body too large",
                        error_code="REQUEST_TOO_LARGE"
                    )

            response = await call_next(request)
            return response

        except json.JSONDecodeError:
            raise ChatbotException(
                status_code=400,
                detail="Invalid JSON format",
                error_code="INVALID_JSON"
            )
        except Exception as e:
            if isinstance(e, ChatbotException):
                raise e
            raise ChatbotException(
                status_code=500,
                detail="Internal server error",
                error_code="INTERNAL_ERROR"
            ) 