from dataclasses import dataclass
from datetime import date, time, datetime
from entities.StatusVisita import StatusVisita


@dataclass
class Visita:
    id: int
    data_agendada: date
    hora_agendada: time
    observacoes: str
    status: StatusVisita
    
    negociacao_id: int
    
    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = StatusVisita(self.status)
    
    def to_dict(self):
        return {
            "id": self.id,
            "data_agendada": self.data_agendada.isoformat(),
            "hora_agendada": self.hora_agendada.isoformat(),
            "observacoes": self.observacoes,
            "status": self.status.value,
            "negociacao_id": self.negociacao_id
        }
    
    def realizar(self):
        if self.status != StatusVisita.AGENDADA:
            raise ValueError("Apenas visitas agendadas podem ser realizadas")
        self.status = StatusVisita.REALIZADA
    
    def cancelar(self):
        if self.status in [StatusVisita.REALIZADA, StatusVisita.NAO_COMPARECEU]:
            raise ValueError("Visitas realizadas ou com não comparecimento não podem ser canceladas")
        self.status = StatusVisita.CANCELADA
    
    def registrar_nao_comparecimento(self):
        if self.status != StatusVisita.AGENDADA:
            raise ValueError("Apenas visitas agendadas podem ter não comparecimento registrado")
        self.status = StatusVisita.NAO_COMPARECEU
    
    def reagendar(self, nova_data: date, nova_hora: time):
        if self.status == StatusVisita.REALIZADA:
            raise ValueError("Visitas realizadas não podem ser reagendadas")
        self.data_agendada = nova_data
        self.hora_agendada = nova_hora
        self.status = StatusVisita.AGENDADA