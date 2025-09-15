import unittest
from unittest.mock import MagicMock, patch
from src.domain.venda import Venda
from src.domain.enum.venda_status import VendaStatus
from src.application.usecase.orquestrador_venda_usecase import OrquestradorVendaUseCase

class TestOrquestradorVendaUseCase(unittest.TestCase):

    def setUp(self):
        self.repository = MagicMock()
        self.veiculos_api = MagicMock()
        self.compradores_api = MagicMock()
        self.pagamentos_api = MagicMock()

        self.usecase = OrquestradorVendaUseCase(
            repository=self.repository,
            veiculos_api=self.veiculos_api,
            compradores_api=self.compradores_api,
            pagamentos_api=self.pagamentos_api
        )

    @patch('src.domain.venda.Venda.criar')
    def test_criar_venda_sucesso(self, mock_criar):
        venda_mock = MagicMock()
        venda_mock.id = "v1"
        venda_mock.veiculo_id = "car123"
        venda_mock.comprador_id = "user456"
        mock_criar.return_value = venda_mock

        self.veiculos_api.reservar.return_value = True
        self.compradores_api.verificar.return_value = True
        self.pagamentos_api.gerar_pagamento.return_value = "pg789"
        self.repository.save.return_value = venda_mock

        result = self.usecase.criar_venda("car123", "user456")

        self.assertEqual(result.status, VendaStatus.AGUARDANDO_PAGAMENTO.value)
        self.assertEqual(result.pagamento_id, "pg789")
        self.repository.save.assert_called_once_with(venda_mock)

    @patch('src.domain.venda.Venda.criar')
    def test_criar_venda_veiculo_nao_reservado(self, mock_criar):
        venda_mock = MagicMock()
        venda_mock.id = "v2"
        venda_mock.veiculo_id = "car123"
        mock_criar.return_value = venda_mock

        self.veiculos_api.reservar.return_value = False

        result = self.usecase.criar_venda("car123", "user456")

        self.assertEqual(result.status, VendaStatus.CANCELADO.value)
        self.repository.save.assert_not_called()

    @patch('src.domain.venda.Venda.criar')
    def test_criar_venda_comprador_invalido(self, mock_criar):
        venda_mock = MagicMock()
        venda_mock.id = "v3"
        venda_mock.veiculo_id = "car123"
        venda_mock.comprador_id = "user456"
        mock_criar.return_value = venda_mock

        self.veiculos_api.reservar.return_value = True
        self.compradores_api.verificar.return_value = False

        result = self.usecase.criar_venda("car123", "user456")

        self.assertEqual(result.status, VendaStatus.CANCELADO.value)
        self.veiculos_api.cancelar_reserva.assert_called_once_with("car123")

    @patch('src.domain.venda.Venda.criar')
    def test_criar_venda_pagamento_falhou(self, mock_criar):
        venda_mock = MagicMock()
        venda_mock.id = "v4"
        venda_mock.veiculo_id = "car123"
        venda_mock.comprador_id = "user456"
        mock_criar.return_value = venda_mock

        self.veiculos_api.reservar.return_value = True
        self.compradores_api.verificar.return_value = True
        self.pagamentos_api.gerar_pagamento.return_value = None

        result = self.usecase.criar_venda("car123", "user456")

        self.assertEqual(result.status, VendaStatus.CANCELADO.value)
        self.veiculos_api.cancelar_reserva.assert_called_once_with("car123")

    def test_concluir_venda_sucesso(self):
        venda_mock = MagicMock()
        venda_mock.pagamento_id = "pg123"
        venda_mock.veiculo_id = "car123"
        self.repository.findById.return_value = venda_mock
        self.pagamentos_api.verificar_pagamento.return_value = True
        self.repository.update.return_value = venda_mock

        result = self.usecase.concluir_venda("v1")

        self.assertEqual(result.status, VendaStatus.CONCLUIDO.value)
        self.veiculos_api.baixar.assert_called_once_with("car123")
        self.repository.update.assert_called_once_with(venda_mock)

    def test_concluir_venda_pagamento_nao_confirmado(self):
        venda_mock = MagicMock()
        venda_mock.pagamento_id = "pg123"
        self.repository.findById.return_value = venda_mock
        self.pagamentos_api.verificar_pagamento.return_value = False

        result = self.usecase.concluir_venda("v1")

        self.assertEqual(result, venda_mock)
        self.repository.update.assert_not_called()

    def test_concluir_venda_nao_encontrada(self):
        self.repository.findById.return_value = None

        result = self.usecase.concluir_venda("v1")

        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
