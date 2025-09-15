import requests

class CompradoresClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def verificar(self, comprador_id):
        resp = requests.get(f"{self.base_url}/{comprador_id}")
        return resp.status_code == 200
