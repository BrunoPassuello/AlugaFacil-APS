from enum import Enum


class StatusVisita(Enum):
    """Enum que representa os possíveis status de uma visita."""
    AGENDADA = "agendada"
    REALIZADA = "realizada"
    CANCELADA = "cancelada"
    NAO_COMPARECEU = "nao_compareceu"

    def __str__(self):
        return self.value