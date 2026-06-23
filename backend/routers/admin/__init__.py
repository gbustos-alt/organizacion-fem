from fastapi import APIRouter
from backend.routers.admin import auth, dashboard, colegios, alumnos, agente

router = APIRouter(prefix="/admin")

# Registrar sub-routers
router.include_router(auth.router)
router.include_router(dashboard.router)
router.include_router(colegios.router)
router.include_router(alumnos.router)
router.include_router(agente.router)
