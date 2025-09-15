from enum import Enum

class VendaStatus(Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    CANCELADO = "CANCELADO"    
    CONCLUIDO = "CONCLUIDO"
    RESERVADO = "RESERVADO"

    @classmethod
    def valueOfValid(cls, value) -> bool:
        return any(enumType for enumType in cls if enumType.value == str(value).upper() or enumType.name == str(value).upper())

    @classmethod
    def valueOf(cls, value):
        for enumType in cls:
            if (enumType.value == str(value).upper() or enumType.name == str(value).upper()):
                return enumType
        return None
