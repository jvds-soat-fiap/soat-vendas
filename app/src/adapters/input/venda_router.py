from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.application.exception.business_exception import BusinessException
from src.adapters.output.repository.repository import Repository
from src.adapters.output.repository.venda_repository import VendaRepository
from src.infrastructure.clients.veiculos_client import VeiculosClient
from src.infrastructure.clients.compradores_client import CompradoresClient
from src.infrastructure.clients.pagamentos_client import PagamentosClient
from src.application.usecase.orquestrador_venda_usecase import OrquestradorVendaUseCase

API_VEICULOS_BASE_URL="http://soat-veiculos:8000/soat-veiculo/v1/veiculos"
API_COMPRADORES_BASE_URL="http://soat-compradores:8001/soat-veiculo/v1/compradores"
API_PAGAMENTOS_BASE_URL="http://soat-pagamentos:8002/soat-veiculo/v1/pagamentos"


_veiculos_api :VeiculosClient = VeiculosClient(API_VEICULOS_BASE_URL)
_compradores_api: CompradoresClient = CompradoresClient(API_COMPRADORES_BASE_URL)
_pagamentos_api: PagamentosClient = PagamentosClient(API_PAGAMENTOS_BASE_URL)

_repository : Repository = VendaRepository()
_usecase = OrquestradorVendaUseCase(
    repository=_repository,
    veiculos_api=_veiculos_api,
    compradores_api=_compradores_api,
    pagamentos_api=_pagamentos_api
)
router = APIRouter()



class VendaInput(BaseModel):
    veiculo_id: str
    comprador_id: str

@router.post(path="/",status_code=status.HTTP_201_CREATED)
def criar_venda(input: VendaInput):
    venda = _usecase.criar_venda(input.veiculo_id, input.comprador_id)
    return venda

@router.patch(path="/{venda_id}/concluir",status_code=status.HTTP_200_OK)
def concluir_venda(venda_id: str):
    venda = _usecase.concluir_venda(venda_id)
    if not venda:
        raise BusinessException(status_code=404, detail="Nao encontrado a venda id: {}".format(venda_id))
    return venda
