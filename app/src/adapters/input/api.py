from fastapi import APIRouter
from src.adapters.input.health_check_router import router as HealthCheck
from src.adapters.input.venda_router import router as VendaRouter

ROUTER_BASE_URL = "/vendas"

api_router = APIRouter()
api_router.include_router(HealthCheck, prefix='{}/health'.format(ROUTER_BASE_URL), tags=["healthCheck"])
api_router.include_router(VendaRouter, prefix='{}'.format(ROUTER_BASE_URL), tags=["vendas"])
