import pickle
from typing import List, Dict, Optional
from entities.Negociacao import Negociacao
from repository.NegociacaoRepository import NegociacaoRepository


class NegociacaoRepositoryPickle(NegociacaoRepository):
    def __init__(self, arquivo='negociacoes.pkl'):
        self.__arquivo = arquivo
        # {id: Negociacao}
        self.__negociacoes: Dict[int, Negociacao] = self.carregar()
    
    def carregar(self) -> Dict[int, Negociacao]:
        try:
            with open(self.__arquivo, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}
    
    def salvar(self) -> None:
        with open(self.__arquivo, 'wb') as f:
            pickle.dump(self.__negociacoes, f)
    
    def _get_proximo_id(self) -> int:
        if not self.__negociacoes:
            return 1
        return max(self.__negociacoes.keys()) + 1
    
    def adicionar(self, negociacao: Negociacao) -> None:
        if negociacao.id == 0:
            negociacao.id = self._get_proximo_id()
        
        if negociacao.id in self.__negociacoes:
            raise ValueError(f"Negociação com ID {negociacao.id} já existe")
        
        self.__negociacoes[negociacao.id] = negociacao
        self.salvar()
    
    def get_por_id(self, negociacao_id: int) -> Optional[Negociacao]:
        self.__negociacoes = self.carregar()
        return self.__negociacoes.get(negociacao_id)
    
    def get_por_locatario(self, locatario_email: str) -> List[Negociacao]:
        self.__negociacoes = self.carregar()
        email_norm = locatario_email.lower().strip()
        return [n for n in self.__negociacoes.values() if n.locatario_email == email_norm]
    
    def get_por_proprietario(self, proprietario_email: str) -> List[Negociacao]:
        self.__negociacoes = self.carregar()
        email_norm = proprietario_email.lower().strip()
        return [n for n in self.__negociacoes.values() if n.proprietario_email == email_norm]
    
    def get_por_anuncio(self, anuncio_id: int) -> List[Negociacao]:
        self.__negociacoes = self.carregar()
        return [n for n in self.__negociacoes.values() if n.anuncio_id == anuncio_id]
    
    def atualizar(self, negociacao: Negociacao) -> None:
        if negociacao.id not in self.__negociacoes:
            raise ValueError(f"Negociação com ID {negociacao.id} não encontrada")
        
        self.__negociacoes[negociacao.id] = negociacao
        self.salvar()
    
    def deletar(self, negociacao_id: int) -> bool:
        if negociacao_id in self.__negociacoes:
            del self.__negociacoes[negociacao_id]
            self.salvar()
            return True
        return False
    
    def get_all(self) -> List[Negociacao]:
        self.__negociacoes = self.carregar()
        return list(self.__negociacoes.values())