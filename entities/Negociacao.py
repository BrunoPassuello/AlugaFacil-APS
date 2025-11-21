from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from entities.StatusNegociacao import StatusNegociacao


@dataclass
class Negociacao:
    """Entidade de domínio que representa uma negociação entre locatário e proprietário."""
    id: int
    avaliacao_locatario: float
    avaliacao_proprietario: float
    data_fim: Optional[date]
    data_inicio: date
    observacoes: str
    status: StatusNegociacao
    valor_final: float
    valor_proposto: float
    
    # Relacionamentos bidirecionais (armazena referências aos IDs)
    locatario_email: str  # Email do locatário (chave do repositório)
    proprietario_email: str  # Email do proprietário
    anuncio_id: int  # ID do anúncio relacionado
    
    def __post_init__(self):
        """Validações após inicialização."""
        if isinstance(self.status, str):
            self.status = StatusNegociacao(self.status)
        
        if self.valor_proposto < 0 or self.valor_final < 0:
            raise ValueError("Valores não podem ser negativos")
        
        if self.avaliacao_locatario < 0 or self.avaliacao_locatario > 5:
            raise ValueError("Avaliação do locatário deve estar entre 0 e 5")
        
        if self.avaliacao_proprietario < 0 or self.avaliacao_proprietario > 5:
            raise ValueError("Avaliação do proprietário deve estar entre 0 e 5")
    
    def to_dict(self):
        """Converte a instância em um dicionário serializável."""
        return {
            "id": self.id,
            "avaliacao_locatario": self.avaliacao_locatario,
            "avaliacao_proprietario": self.avaliacao_proprietario,
            "data_fim": self.data_fim.isoformat() if self.data_fim else None,
            "data_inicio": self.data_inicio.isoformat(),
            "observacoes": self.observacoes,
            "status": self.status.value,
            "valor_final": self.valor_final,
            "valor_proposto": self.valor_proposto,
            "locatario_email": self.locatario_email,
            "proprietario_email": self.proprietario_email,
            "anuncio_id": self.anuncio_id
        }
    
    def aprovar(self):
        """Aprova a negociação."""
        if self.status != StatusNegociacao.INICIADA:
            raise ValueError("Apenas negociações iniciadas podem ser aprovadas")
        self.status = StatusNegociacao.APROVADA
    
    def cancelar(self):
        """Cancela a negociação."""
        if self.status == StatusNegociacao.FINALIZADA:
            raise ValueError("Negociações finalizadas não podem ser canceladas")
        self.status = StatusNegociacao.CANCELADA
    
    def finalizar(self):
        """Finaliza a negociação."""
        if self.status != StatusNegociacao.APROVADA:
            raise ValueError("Apenas negociações aprovadas podem ser finalizadas")
        self.status = StatusNegociacao.FINALIZADA
        if not self.data_fim:
            self.data_fim = date.today()