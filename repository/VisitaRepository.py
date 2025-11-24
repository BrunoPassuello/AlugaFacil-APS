from abc import ABC, abstractmethod
from typing import List, Optional
from entities.Visita import Visita


class VisitaRepository(ABC):
    
    @abstractmethod
    def adicionar(self, visita: Visita) -> None:
        pass
    
    @abstractmethod
    def get_por_id(self, visita_id: int) -> Optional[Visita]:
        pass
    
    @abstractmethod
    def get_por_negociacao(self, negociacao_id: int) -> List[Visita]:
        pass
    
    @abstractmethod
    def atualizar(self, visita: Visita) -> None:
        pass
    
    @abstractmethod
    def deletar(self, visita_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Visita]:
        pass