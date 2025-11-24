from enum import Enum


class StatusVisita(Enum):
    AGENDADA = "agendada"
    REALIZADA = "realizada"
    CANCELADA = "cancelada"
    NAO_COMPARECEU = "nao_compareceu"

    def __str__(self):
        return self.value