import pytest
from ..services.task_service import process_long_conversation
from ..services.webhook_service import WebhookService, WebhookConfig

@pytest.mark.celery
def test_process_long_conversation():
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    
    result = process_long_conversation.delay(history)
    assert result.get(timeout=5) is not None

@pytest.mark.asyncio
async def test_webhook_notification(mocker):
    webhook_service = WebhookService()
    
    # Register test webhook
    webhook = WebhookConfig(
        url="http://test.com/webhook",
        events=["chat.response"],
        secret="test-secret"
    )
    webhook_service.register_webhook(webhook)
    
    # Mock notification
    mock_notify = mocker.patch('services.task_service.send_webhook_notification.delay')
    
    await webhook_service.notify_event(
        "chat.response",
        {"test": "data"}
    )
    
    mock_notify.assert_called_once() 