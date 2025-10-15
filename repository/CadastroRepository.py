import pickle
from abc import abstractmethod
from typing import Dict
from entities.Pessoa import Pessoa

class CadastroRepository:
    
    @abstractmethod
    def adicionar_cadastro(self, pessoa: Pessoa):
        raise NotImplementedError
    
    @abstractmethod
    def get_pessoa_email(self, email: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    def update_cadastro(self, email: str, pessoa: Pessoa):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, email: str):
        raise NotImplementedError
    