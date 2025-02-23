import pytest
from fastapi.testclient import TestClient
import redis
import boto3
from moto import mock_dynamodb
from ..main import app
from ..config import get_settings, Settings
from ..services.auth_service import AuthService

@pytest.fixture
def test_settings():
    return Settings(
        OPENAI_API_KEY="test-key",
        REDIS_HOST="localhost",
        REDIS_PORT=6379,
        DYNAMODB_TABLE="test_chat_history",
        JWT_SECRET_KEY="test-secret",
        API_KEY="test-api-key",
        ENVIRONMENT="test"
    )

@pytest.fixture
def test_client(test_settings):
    with TestClient(app) as client:
        yield client

@pytest.fixture
def auth_headers(test_settings):
    auth_service = AuthService()
    token = auth_service.create_access_token("test-user", "test")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mock_redis():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    yield redis_client
    redis_client.flushdb()

@pytest.fixture
def mock_dynamo():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb')
        
        # Create test table
        table = dynamodb.create_table(
            TableName='test_chat_history',
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'N'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        yield table 