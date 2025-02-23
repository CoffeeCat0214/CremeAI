import openai
from typing import Dict, Optional
import os
from .memory_service import MemoryService
from .personality_service import PersonalityService
from .cache_service import CacheService
from .webhook_service import WebhookService
from .task_service import process_long_conversation
from ..exceptions import AIServiceError

class ChatService:
    def __init__(self):
        self.memory_service = MemoryService()
        self.personality_service = PersonalityService()
        self.cache_service = CacheService()
        self.webhook_service = WebhookService()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    async def generate_response(
        self, 
        user_id: str, 
        message: str, 
        platform: str
    ) -> Dict[str, str]:
        try:
            # Check cache first
            cached_response = await self.cache_service.get_cached_response(
                user_id=user_id,
                message=message,
                platform=platform
            )
            
            if cached_response:
                return cached_response

            # Get conversation history
            history = await self.memory_service.get_chat_history(user_id)
            
            # Process long conversations in background
            if len(history) > 10:
                process_long_conversation.delay(history)

            # Get personality prompt
            system_prompt = self.personality_service.get_base_prompt()
            
            # Construct the messages for GPT
            messages = [
                {"role": "system", "content": system_prompt},
                *history,
                {"role": "user", "content": message}
            ]

            # Generate response
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=messages,
                temperature=0.9,
                max_tokens=150
            )

            # Store the interaction
            await self.memory_service.store_interaction(
                user_id=user_id,
                message=message,
                response=response.choices[0].message.content,
                platform=platform
            )

            result = {
                "response": response.choices[0].message.content,
                "decree": self._extract_decree(response.choices[0].message.content)
            }

            # Cache the response
            await self.cache_service.cache_response(
                user_id=user_id,
                message=message,
                platform=platform,
                response=result
            )

            # Notify webhooks about new interaction
            await self.webhook_service.notify_event(
                "chat.response",
                {
                    "user_id": user_id,
                    "platform": platform,
                    "response": result
                }
            )

            return result
        except Exception as e:
            raise AIServiceError(str(e))

    def _extract_decree(self, response: str) -> Optional[str]:
        # Extract royal decree if present in the response
        if "ROYAL DECREE:" in response:
            return response.split("ROYAL DECREE:")[1].strip()
        return None 