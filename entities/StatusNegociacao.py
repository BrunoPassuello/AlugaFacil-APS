from enum import Enum


class StatusNegociacao(Enum):
    """Enum que representa os possíveis status de uma negociação."""
    INICIADA = "iniciada"
    APROVADA = "aprovada"
    CANCELADA = "cancelada"
    FINALIZADA = "finalizada"

    def __str__(self):
        return self.value