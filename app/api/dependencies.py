
import requests

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.services.supabase_service import verify_supabase_token


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
) -> dict:

    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required.",
        )

    access_token = credentials.credentials

    try:
        user = verify_supabase_token(access_token)

    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Unable to verify authentication with Supabase.",
        )

    if not user or not user.get("id"):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token.",
        )

    user["access_token"] = access_token

    return user
