from enum import Enum


class StatusNegociacao(Enum):
    INICIADA = "iniciada"
    APROVADA = "aprovada"
    CANCELADA = "cancelada"
    FINALIZADA = "finalizada"

    def __str__(self):
        return self.value