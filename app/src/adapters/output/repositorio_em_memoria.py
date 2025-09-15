# app/adapters/output/repositorio_em_memoria.py

class RepositorioVeiculoEmMemoria:
    def __init__(self):
        self.veiculos = {}

    def salvar(self, veiculo):
        self.veiculos[veiculo.id] = veiculo

    def listar_disponiveis(self):
        return [v for v in self.veiculos.values() if not v.vendido]

    def listar_vendidos(self):
        return [v for v in self.veiculos.values() if v.vendido]

    def buscar_por_id(self, veiculo_id):
        return self.veiculos.get(veiculo_id)

    def atualizar(self, veiculo):
        if veiculo.id in self.veiculos:
            self.veiculos[veiculo.id] = veiculo
            return True
        return False

    def marcar_como_vendido(self, veiculo_id):
        veiculo = self.buscar_por_id(veiculo_id)
        if not veiculo:
            raise ValueError("Veículo não encontrado")
        veiculo.vendido = True
        self.atualizar(veiculo)
        return veiculo
