from abc import ABC, abstractmethod
from typing import List, Optional
from entities.Negociacao import Negociacao


class NegociacaoRepository(ABC):
    """Interface para repositório de negociações."""
    
    @abstractmethod
    def adicionar(self, negociacao: Negociacao) -> None:
        """Adiciona uma nova negociação."""
        pass
    
    @abstractmethod
    def get_por_id(self, negociacao_id: int) -> Optional[Negociacao]:
        """Retorna uma negociação por ID."""
        pass
    
    @abstractmethod
    def get_por_locatario(self, locatario_email: str) -> List[Negociacao]:
        """Retorna todas as negociações de um locatário."""
        pass
    
    @abstractmethod
    def get_por_proprietario(self, proprietario_email: str) -> List[Negociacao]:
        """Retorna todas as negociações de um proprietário."""
        pass
    
    @abstractmethod
    def get_por_anuncio(self, anuncio_id: int) -> List[Negociacao]:
        """Retorna todas as negociações de um anúncio."""
        pass
    
    @abstractmethod
    def atualizar(self, negociacao: Negociacao) -> None:
        """Atualiza uma negociação existente."""
        pass
    
    @abstractmethod
    def deletar(self, negociacao_id: int) -> bool:
        """Remove uma negociação."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Negociacao]:
        """Retorna todas as negociações."""
        pass