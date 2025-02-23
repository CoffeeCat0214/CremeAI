from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from ..config import get_settings

settings = get_settings()

class AuthService:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.security = HTTPBearer()

    def create_access_token(self, user_id: str, platform: str) -> str:
        payload = {
            'user_id': user_id,
            'platform': platform,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    async def verify_token(self, credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> Dict:
        try:
            token = credentials.credentials
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            if payload['exp'] < datetime.utcnow().timestamp():
                raise HTTPException(status_code=401, detail='Token has expired')
                
            return payload
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e)) 