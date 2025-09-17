#Classe que armazena usuarios em memória
from typing import Dict
from Pessoa import Pessoa
class RepositorioUsuarios:
    def __init__(self):
        #{email : Pessoa}
        self.__dicionario_email: Dict[str, Pessoa] = {}

    def adicionar(self, usuario):
        email = usuario.email.lower().strip()
        self.__dicionario_email[email] = usuario

    def obter_por_email(self, email: str):
        return self.__dicionario_email.get(email.lower().strip())