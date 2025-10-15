import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .CadastroRepository import CadastroRepository
from typing import Dict
from entities.Pessoa import Pessoa
import pickle

class CadastroRepositoryPickle(CadastroRepository):
    def __init__(self, arquivo = 'pessoas.pkl'):
        self.__arquivo = arquivo
        #{email : Pessoa}
        self.__pessoas: Dict[str, Pessoa] = self.carregar()

    def carregar(self) -> Dict[str, Pessoa]:
        try:
            with open(self.__arquivo, 'rb') as f: ##rb: read binary
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def salvar(self) -> None:
        with open(self.__arquivo, 'wb') as f: #write binary
            pickle.dump(self.__pessoas, f)

    def adicionar_cadastro(self, usuario):
        email = usuario.email.lower().strip()
        if email in self.__pessoas:
            raise ValueError(f"Pessoa com email "+ {email} +" já existe")
        self.__pessoas[email] = usuario
        self.salvar()
        
    def get_pessoa_email(self, email: str):
        self.carregar()
        return self.__pessoas.get(email.lower().strip())
    
    def get_all(self):
        self.__pessoas = self.carregar()  # Garante dados atualizados
        return self.__pessoas.copy()