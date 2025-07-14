from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from app import config

security = HTTPBasic()

ADMIN_USERNAME = config.api_user
ADMIN_PASSWORD = config.api_pass

class AdminUser:
    def __init__(self, username: str):
        self.username = username

async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> AdminUser:
    is_correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    is_correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return AdminUser(username=credentials.username)
