from abc import ABC, abstractmethod
from datetime import datetime
import hashlib

class Pessoa(ABC):
    def __init__(self, 
                cpf: str, 
                data_nascimento: datetime, 
                email: str, 
                nome: str, 
                senha: str, 
                telefone: str, 
                telefone_verificado: bool = False):
            self.__cpf = cpf
            self.__data_nascimento = data_nascimento
            self.__email = email
            self.__nome = nome
            self.__senha = self._hash_password(senha)
            self.__telefone = telefone
            self.__telefone_verificado = telefone_verificado
            self.__created_at = datetime.now()
            self.__avaliacao = 0.0

    def _hash_password(self, senha):
            salt = "aluga_facil_melhor_que_olx"
            return hashlib.sha256((senha + salt).encode()).hexdigest()
        
    def verificar_senha(self, senha):
        return self._hash_password(senha) == self.senha

    @property
    def cpf(self):
        return self.__cpf
    
    @cpf.setter
    def cpf(self, value):
        self.__cpf = value
    
    @property
    def data_nascimento(self):
        return self.__data_nascimento
    
    @data_nascimento.setter
    def data_nascimento(self, value):
        self.__data_nascimento = value
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value):
        self.__email = value
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, value):
        self.__nome = value
    
    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, value):
        self.__senha = self._hash_password(value)
    
    @property
    def telefone(self):
        return self.__telefone
    
    @telefone.setter
    def telefone(self, value):
        self.__telefone = value
    
    @property
    def telefone_verificado(self):
        return self.__telefone_verificado
    
    @telefone_verificado.setter
    def telefone_verificado(self, value):
        self.__telefone_verificado = value
    
    @property
    def created_at(self):
        return self.__created_at
    
    @created_at.setter
    def created_at(self, value):
        self.__created_at = value
    
    @property
    def avaliacao(self):
        return self.__avaliacao
    
    @avaliacao.setter
    def avaliacao (self, value):
        self.__avaliacao = value

    @abstractmethod
    def get_tipo_usuario(self):
        pass
    
    def __str__(self):
        return f"{self.nome} ({self.email}) - {self.get_tipo_usuario()}"