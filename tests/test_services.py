import pytest
from ..services.chat_service import ChatService
from ..services.cache_service import CacheService
from ..services.memory_service import MemoryService
from ..exceptions import AIServiceError

@pytest.mark.asyncio
async def test_cache_service(mock_redis):
    cache_service = CacheService()
    test_data = {
        "response": "Hello!",
        "decree": None
    }
    
    await cache_service.cache_response(
        user_id="test-user",
        message="test",
        platform="test",
        response=test_data
    )
    
    cached = await cache_service.get_cached_response(
        user_id="test-user",
        message="test",
        platform="test"
    )
    
    assert cached == test_data

@pytest.mark.asyncio
async def test_memory_service(mock_dynamo):
    memory_service = MemoryService()
    
    await memory_service.store_interaction(
        user_id="test-user",
        message="Hello",
        response="Hi there!",
        platform="test"
    )
    
    history = await memory_service.get_chat_history("test-user")
    assert len(history) > 0
    assert history[0]["content"] == "Hi there!"

@pytest.mark.asyncio
async def test_chat_service_error_handling():
    chat_service = ChatService()
    
    with pytest.raises(AIServiceError):
        await chat_service.generate_response(
            user_id="test-user",
            message="Hello",
            platform="test"
        ) 