import pickle
from typing import List, Dict, Optional
from entities.Negociacao import Negociacao
from repository.NegociacaoRepository import NegociacaoRepository


class NegociacaoRepositoryPickle(NegociacaoRepository):
    """Implementação de repositório de negociações usando pickle."""
    
    def __init__(self, arquivo='negociacoes.pkl'):
        self.__arquivo = arquivo
        # {id: Negociacao}
        self.__negociacoes: Dict[int, Negociacao] = self.carregar()
    
    def carregar(self) -> Dict[int, Negociacao]:
        """Carrega negociações do arquivo pickle."""
        try:
            with open(self.__arquivo, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}
    
    def salvar(self) -> None:
        """Salva negociações no arquivo pickle."""
        with open(self.__arquivo, 'wb') as f:
            pickle.dump(self.__negociacoes, f)
    
    def _get_proximo_id(self) -> int:
        """Retorna o próximo ID disponível."""
        if not self.__negociacoes:
            return 1
        return max(self.__negociacoes.keys()) + 1
    
    def adicionar(self, negociacao: Negociacao) -> None:
        """Adiciona uma nova negociação."""
        if negociacao.id == 0:
            negociacao.id = self._get_proximo_id()
        
        if negociacao.id in self.__negociacoes:
            raise ValueError(f"Negociação com ID {negociacao.id} já existe")
        
        self.__negociacoes[negociacao.id] = negociacao
        self.salvar()
    
    def get_por_id(self, negociacao_id: int) -> Optional[Negociacao]:
        """Retorna uma negociação por ID."""
        self.__negociacoes = self.carregar()
        return self.__negociacoes.get(negociacao_id)
    
    def get_por_locatario(self, locatario_email: str) -> List[Negociacao]:
        """Retorna todas as negociações de um locatário."""
        self.__negociacoes = self.carregar()
        email_norm = locatario_email.lower().strip()
        return [n for n in self.__negociacoes.values() if n.locatario_email == email_norm]
    
    def get_por_proprietario(self, proprietario_email: str) -> List[Negociacao]:
        """Retorna todas as negociações de um proprietário."""
        self.__negociacoes = self.carregar()
        email_norm = proprietario_email.lower().strip()
        return [n for n in self.__negociacoes.values() if n.proprietario_email == email_norm]
    
    def get_por_anuncio(self, anuncio_id: int) -> List[Negociacao]:
        """Retorna todas as negociações de um anúncio."""
        self.__negociacoes = self.carregar()
        return [n for n in self.__negociacoes.values() if n.anuncio_id == anuncio_id]
    
    def atualizar(self, negociacao: Negociacao) -> None:
        """Atualiza uma negociação existente."""
        if negociacao.id not in self.__negociacoes:
            raise ValueError(f"Negociação com ID {negociacao.id} não encontrada")
        
        self.__negociacoes[negociacao.id] = negociacao
        self.salvar()
    
    def deletar(self, negociacao_id: int) -> bool:
        """Remove uma negociação."""
        if negociacao_id in self.__negociacoes:
            del self.__negociacoes[negociacao_id]
            self.salvar()
            return True
        return False
    
    def get_all(self) -> List[Negociacao]:
        """Retorna todas as negociações."""
        self.__negociacoes = self.carregar()
        return list(self.__negociacoes.values())