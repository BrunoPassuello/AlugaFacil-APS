import pickle
import os
from typing import List, Optional
from entities.Anuncio import Anuncio

class AnuncioRepositoryPickle:
    
    def __init__(self, arquivo: str = "data/anuncios.pkl"):
        self._arquivo = arquivo
        self._anuncios: List[Anuncio] = []
        self._proximo_id = 1
        self._carregar()
    
    def _carregar(self):
        if os.path.exists(self._arquivo):
            try:
                with open(self._arquivo, 'rb') as f:
                    data = pickle.load(f)
                    self._anuncios = data.get('anuncios', [])
                    self._proximo_id = data.get('proximo_id', 1)
            except Exception as e:
                print(f"Erro ao carregar anúncios: {e}")
                self._anuncios = []
                self._proximo_id = 1
    
    def _salvar(self):
        os.makedirs(os.path.dirname(self._arquivo), exist_ok=True)
        try:
            with open(self._arquivo, 'wb') as f:
                pickle.dump({
                    'anuncios': self._anuncios,
                    'proximo_id': self._proximo_id
                }, f)
        except Exception as e:
            print(f"Erro ao salvar anúncios: {e}")
    
    def adicionar(self, anuncio: Anuncio) -> Anuncio:
        self._anuncios.append(anuncio)
        self._salvar()
        return anuncio
    
    def listar_todos(self) -> List[Anuncio]:
        return list(self._anuncios)
    
    def listar_por_proprietario(self, email_proprietario: str) -> List[Anuncio]:
        return [a for a in self._anuncios if a.proprietario_email == email_proprietario]
    
    def get_por_id(self, anuncio_id: int) -> Optional[Anuncio]:
        return next((a for a in self._anuncios if a.id == anuncio_id), None)
    
    def gerar_proximo_id(self) -> int:
        id_atual = self._proximo_id
        self._proximo_id += 1
        self._salvar()
        return id_atual
    
    def atualizar(self, anuncio: Anuncio) -> bool:
        for i, item in enumerate(self._anuncios):
            if item.id == anuncio.id:
                self._anuncios[i] = anuncio
                self._salvar()
                return True
        return False
    
    def remover(self, anuncio_id: int) -> bool:
        inicial = len(self._anuncios)
        self._anuncios = [a for a in self._anuncios if a.id != anuncio_id]
        if len(self._anuncios) < inicial:
            self._salvar()
            return True
        return False
