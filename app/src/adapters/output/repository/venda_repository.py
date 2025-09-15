from src.adapters.output.repository.repository_default import RepositoryDefault
from src.domain.venda import Venda

class VendaRepository(RepositoryDefault[Venda, str]):
    def __init__(self) -> None:
        super().__init__(Venda)


    def parseToModel(self, dict):
        return Venda.parseToModel(dict)
