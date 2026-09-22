from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix=settings.api_v1_prefix)
# Register versioned feature routers here.
