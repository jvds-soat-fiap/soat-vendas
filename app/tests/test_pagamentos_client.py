import unittest
from unittest.mock import patch, MagicMock
from src.infrastructure.clients.pagamentos_client import PagamentosClient

class TestPagamentosClient(unittest.TestCase):
    def setUp(self):
        self.client = PagamentosClient(base_url="http://mock.pagamentos.com")

    @patch("requests.post")
    def test_gerar_pagamento_sucesso(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"_id": "12345"}
        mock_post.return_value = mock_response

        result = self.client.gerar_pagamento("v1", "v2", "c1")
        self.assertEqual(result, "12345")
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_gerar_pagamento_falha_status(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        result = self.client.gerar_pagamento("v1", "v2", "c1")
        self.assertIsNone(result)

    @patch("requests.post")
    def test_gerar_pagamento_excecao(self, mock_post):
        mock_post.side_effect = Exception("Erro de rede")

        result = self.client.gerar_pagamento("v1", "v2", "c1")
        self.assertIsNone(result)

    @patch("requests.get")
    def test_verificar_pagamento_pago(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "PAGO"}
        mock_get.return_value = mock_response

        result = self.client.verificar_pagamento("12345")
        self.assertTrue(result)

    @patch("requests.get")
    def test_verificar_pagamento_nao_pago(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "PENDENTE"}
        mock_get.return_value = mock_response

        result = self.client.verificar_pagamento("12345")
        self.assertFalse(result)

    @patch("requests.get")
    def test_verificar_pagamento_falha_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.client.verificar_pagamento("12345")
        self.assertFalse(result)

    @patch("requests.get")
    def test_verificar_pagamento_excecao(self, mock_get):
        mock_get.side_effect = Exception("Erro de rede")

        result = self.client.verificar_pagamento("12345")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
