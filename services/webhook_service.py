from typing import Dict, Any, List
import json
from pydantic import BaseModel, HttpUrl
from .task_service import send_webhook_notification
from ..config import get_settings

settings = get_settings()

class WebhookConfig(BaseModel):
    url: HttpUrl
    events: List[str]
    secret: str

class WebhookService:
    def __init__(self):
        self.webhooks: Dict[str, WebhookConfig] = {}

    def register_webhook(self, webhook: WebhookConfig):
        """Register a new webhook endpoint"""
        self.webhooks[str(webhook.url)] = webhook

    def unregister_webhook(self, url: str):
        """Unregister a webhook endpoint"""
        if url in self.webhooks:
            del self.webhooks[url]

    async def notify_event(self, event_type: str, event_data: Dict[str, Any]):
        """Notify all registered webhooks about an event"""
        for webhook in self.webhooks.values():
            if event_type in webhook.events:
                # Send notification in background
                send_webhook_notification.delay(
                    str(webhook.url),
                    {
                        "event_type": event_type,
                        "data": event_data,
                        "timestamp": int(time.time())
                    }
                ) 