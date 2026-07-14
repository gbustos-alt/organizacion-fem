from fastapi import APIRouter
from backend.routers.admin import auth, dashboard, colegios, agente, novedades, materiales, actividades

router = APIRouter(prefix="/admin")

# Registrar sub-routers
router.include_router(auth.router)
router.include_router(dashboard.router)
router.include_router(colegios.router)
router.include_router(novedades.router)
router.include_router(materiales.router)
router.include_router(actividades.router)
router.include_router(agente.router)
