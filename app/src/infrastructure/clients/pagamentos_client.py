import requests

class PagamentosClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def gerar_pagamento(self, venda_id, veiculo_id, comprador_id):
        try:
            resp = requests.post(
                url=f"{self.base_url}",
                json={
                    "venda_id": venda_id,
                    "comprador_id": comprador_id,
                    "veiculo_id": veiculo_id
                }
            )
            if resp.status_code == 201:
                return resp.json()["_id"]
        except Exception as e:
            print("Erro ao gerar código de pagamento: {}".format(e))
        return None

    def verificar_pagamento(self, pagamento_id):
        try:
            resp = requests.get(
                url=f"{self.base_url}/{pagamento_id}"
            )
            print(resp.json())
            if resp.status_code == 200:
                return resp.json()["status"] == "PAGO"
        except Exception as e:
            print("Erro ao verificar pagamento:", e)
        return False
