from dataclasses import dataclass, field
from src.domain.enum.venda_status import VendaStatus
import uuid

@dataclass
class Venda:
    _id: str
    veiculo_id: str
    comprador_id: str
    pagamento_id: str = field(init=True, default=None)
    status: VendaStatus = field(init=True, default=VendaStatus.RESERVADO.value)

    @property
    def id(self):
        return self._id

    @staticmethod
    def criar(veiculo_id, comprador_id):
        return Venda(
            _id=str(uuid.uuid4()),
            veiculo_id=veiculo_id,
            comprador_id=comprador_id
        )

    @classmethod
    def parseToModel(cls, dataDict):
        return cls(**dataDict)
