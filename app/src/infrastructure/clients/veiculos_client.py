import requests
from src.domain.constants import *

class VeiculosClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def reservar(self, veiculo_id):
        try:
            resp = requests.patch(
                url=f"{self.base_url}/{veiculo_id}/reservar",
                timeout=TIMEOUT_API
            )
            print(resp)
            return resp.status_code == 204
        except Exception as e:
            print(f"[CLIENT VEICULOS] Erro ao reservar veículo {veiculo_id}: {e}")
            return False

    def cancelar_reserva(self, veiculo_id):
        if not veiculo_id or veiculo_id == "False":
            print("[CLIENT VEICULOS] ID inválido para cancelar reserva:", veiculo_id)
            return False
        try:
            resp = requests.patch(
                url=f"{self.base_url}/{veiculo_id}/cancelar/reserva",
                timeout=TIMEOUT_API
            )
            return resp.status_code == 204
        except Exception as e:
            print(f"[CLIENT VEICULOS] Erro ao desreservar veículo {veiculo_id}: {e}")
            return False

    def baixar(self, veiculo_id):
        try:
            resp = requests.patch(
                url=f"{self.base_url}/{veiculo_id}/vendido",
                timeout=TIMEOUT_API
            )
            return resp.status_code == 204
        except Exception as e:
            print(f"[CLIENT VEICULOS] Erro ao baixar veículo {veiculo_id}: {e}")
            return False

