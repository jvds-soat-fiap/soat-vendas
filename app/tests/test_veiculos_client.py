import unittest
from unittest.mock import patch, MagicMock
from src.domain.constants import TIMEOUT_API
from src.infrastructure.clients.veiculos_client import VeiculosClient

class TestVeiculosClient(unittest.TestCase):
    def setUp(self):
        self.client = VeiculosClient(base_url="http://mock.veiculos.com")

    @patch("requests.patch")
    def test_reservar_sucesso(self, mock_patch):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_patch.return_value = mock_response

        result = self.client.reservar("123")
        self.assertTrue(result)
        mock_patch.assert_called_once_with(
            url="http://mock.veiculos.com/123/reservar",
            timeout=TIMEOUT_API
        )

    @patch("requests.patch")
    def test_reservar_falha(self, mock_patch):
        mock_patch.side_effect = Exception("Erro de conexão")

        result = self.client.reservar("123")
        self.assertFalse(result)

    @patch("requests.patch")
    def test_cancelar_reserva_sucesso(self, mock_patch):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_patch.return_value = mock_response

        result = self.client.cancelar_reserva("456")
        self.assertTrue(result)
        mock_patch.assert_called_once_with(
            url="http://mock.veiculos.com/456/cancelar/reserva",
            timeout=TIMEOUT_API
        )

    def test_cancelar_reserva_id_invalido(self):
        self.assertFalse(self.client.cancelar_reserva(None))
        self.assertFalse(self.client.cancelar_reserva("False"))

    @patch("requests.patch")
    def test_cancelar_reserva_falha(self, mock_patch):
        mock_patch.side_effect = Exception("Erro de conexão")

        result = self.client.cancelar_reserva("456")
        self.assertFalse(result)

    @patch("requests.patch")
    def test_baixar_sucesso(self, mock_patch):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_patch.return_value = mock_response

        result = self.client.baixar("789")
        self.assertTrue(result)
        mock_patch.assert_called_once_with(
            url="http://mock.veiculos.com/789/vendido",
            timeout=TIMEOUT_API
        )

    @patch("requests.patch")
    def test_baixar_falha(self, mock_patch):
        mock_patch.side_effect = Exception("Erro de conexão")

        result = self.client.baixar("789")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
