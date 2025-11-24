from abc import ABC, abstractmethod
from typing import List, Optional
from entities.Negociacao import Negociacao


class NegociacaoRepository(ABC):
    
    @abstractmethod
    def adicionar(self, negociacao: Negociacao) -> None:
        pass
    
    @abstractmethod
    def get_por_id(self, negociacao_id: int) -> Optional[Negociacao]:
        pass
    
    @abstractmethod
    def get_por_locatario(self, locatario_email: str) -> List[Negociacao]:
        pass
    
    @abstractmethod
    def get_por_proprietario(self, proprietario_email: str) -> List[Negociacao]:
        pass
    
    @abstractmethod
    def get_por_anuncio(self, anuncio_id: int) -> List[Negociacao]:
        pass
    
    @abstractmethod
    def atualizar(self, negociacao: Negociacao) -> None:
        pass
    
    @abstractmethod
    def deletar(self, negociacao_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Negociacao]:
        pass