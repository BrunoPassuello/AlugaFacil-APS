from abc import ABC, abstractmethod
from typing import List, Optional
from entities.Visita import Visita


class VisitaRepository(ABC):
    """Interface para repositório de visitas."""
    
    @abstractmethod
    def adicionar(self, visita: Visita) -> None:
        """Adiciona uma nova visita."""
        pass
    
    @abstractmethod
    def get_por_id(self, visita_id: int) -> Optional[Visita]:
        """Retorna uma visita por ID."""
        pass
    
    @abstractmethod
    def get_por_negociacao(self, negociacao_id: int) -> List[Visita]:
        """Retorna todas as visitas de uma negociação."""
        pass
    
    @abstractmethod
    def atualizar(self, visita: Visita) -> None:
        """Atualiza uma visita existente."""
        pass
    
    @abstractmethod
    def deletar(self, visita_id: int) -> bool:
        """Remove uma visita."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Visita]:
        """Retorna todas as visitas."""
        pass