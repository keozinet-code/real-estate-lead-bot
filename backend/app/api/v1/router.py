from fastapi import APIRouter

from app.api.v1.leads import router as leads_router
from app.core.config import settings

router = APIRouter(prefix=settings.api_v1_prefix)
router.include_router(leads_router)
