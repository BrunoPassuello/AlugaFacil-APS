import pickle
import os
from typing import List, Optional
from entities.Imovel import Imovel

class ImovelRepositoryPickle:
    
    def __init__(self, arquivo: str = "data/imoveis.pkl"):
        self._arquivo = arquivo
        self._imoveis: List[Imovel] = []
        self._proximo_id = 1
        self._carregar()
    
    def _carregar(self):
        if os.path.exists(self._arquivo):
            try:
                with open(self._arquivo, 'rb') as f:
                    data = pickle.load(f)
                    self._imoveis = data.get('imoveis', [])
                    self._proximo_id = data.get('proximo_id', 1)
            except Exception as e:
                print(f"Erro ao carregar imóveis: {e}")
                self._imoveis = []
                self._proximo_id = 1
    
    def _salvar(self):
        os.makedirs(os.path.dirname(self._arquivo), exist_ok=True)
        try:
            with open(self._arquivo, 'wb') as f:
                pickle.dump({
                    'imoveis': self._imoveis,
                    'proximo_id': self._proximo_id
                }, f)
        except Exception as e:
            print(f"Erro ao salvar imóveis: {e}")
    
    def adicionar(self, imovel: Imovel) -> Imovel:
        imovel._id = self._proximo_id
        self._proximo_id += 1
        self._imoveis.append(imovel)
        self._salvar()
        return imovel
    
    def listar_por_proprietario(self, email_proprietario: str) -> List[Imovel]:
        return [i for i in self._imoveis if i.proprietario and i.proprietario.email == email_proprietario]
    
    def get_por_id(self, imovel_id: int) -> Optional[Imovel]:
        return next((i for i in self._imoveis if i.id == imovel_id), None)
    
    def atualizar(self, imovel: Imovel) -> bool:
        for i, item in enumerate(self._imoveis):
            if item.id == imovel.id:
                self._imoveis[i] = imovel
                self._salvar()
                return True
        return False
    
    def remover(self, imovel_id: int) -> bool:
        inicial = len(self._imoveis)
        self._imoveis = [i for i in self._imoveis if i.id != imovel_id]
        if len(self._imoveis) < inicial:
            self._salvar()
            return True
        return False
