# app/application/orquestrador_venda.py

from src.domain.venda import Venda
from src.domain.enum.venda_status import VendaStatus
from src.adapters.output.repository.repository import Repository
from src.infrastructure.clients.veiculos_client import VeiculosClient
from src.infrastructure.clients.compradores_client import CompradoresClient
from src.infrastructure.clients.pagamentos_client import PagamentosClient
from src.util.logger_custom import Logger

class OrquestradorVendaUseCase:
    def __init__(
        self,
        repository: Repository,
        veiculos_api: VeiculosClient,
        compradores_api: CompradoresClient,
        pagamentos_api: PagamentosClient
    ):
        self._repository = repository
        self._veiculos_api = veiculos_api
        self._compradores_api = compradores_api
        self._pagamentos_api = pagamentos_api

    def criar_venda(self, veiculo_id, comprador_id) -> Venda:
        Logger.info(Logger.getClassMethodCurrent(), f"Iniciando a venda do veiculo id: {veiculo_id}")
        venda = Venda.criar(veiculo_id, comprador_id)
        Logger.info(Logger.getClassMethodCurrent(), f"Criado com sucesso a venda id: {venda.id}")

        Logger.info(Logger.getClassMethodCurrent(), f"Reservando veiculo({venda.veiculo_id}) referente a venda id: {venda.id}")
        if not self._veiculos_api.reservar(veiculo_id):
            venda.status = VendaStatus.CANCELADO.value
            return venda

        Logger.info(Logger.getClassMethodCurrent(), f"Validando comprador id: {venda.comprador_id}")
        if not self._compradores_api.verificar(comprador_id):
            return self._cancelar_venda(venda)

        pagamento_id = self._pagamentos_api.gerar_pagamento(venda.id, veiculo_id, comprador_id)
        if not pagamento_id:
            return self._cancelar_venda(venda)
        
        venda.status = VendaStatus.AGUARDANDO_PAGAMENTO.value
        venda.pagamento_id = pagamento_id
        return self._repository.save(venda)

    def buscar_id(self, venda_id: str) -> Venda:
        venda : Venda = self._repository.findById(venda_id)
        return venda

    def concluir_venda(self, venda_id) -> Venda:
        venda = self.buscar_id(venda_id=venda_id)
        if not venda:
            return None

        if not self._pagamentos_api.verificar_pagamento(venda.pagamento_id):
            return venda

        self._veiculos_api.baixar(venda.veiculo_id)
        venda.status = VendaStatus.CONCLUIDO.value
        return self._repository.update(venda)
    
    def _cancelar_venda(self, venda: Venda) -> Venda:
        Logger.info(Logger.getClassMethodCurrent(), f"Cancelando a venda id: {venda.id}")
        self._veiculos_api.cancelar_reserva(venda.veiculo_id)
        venda.status = VendaStatus.CANCELADO.value
        return venda

