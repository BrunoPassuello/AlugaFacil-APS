from Pessoa import Pessoa
from datetime import datetime

class Proprietario(Pessoa):
    
    def __init__(self, cpf: str, data_nascimento: str, email: str,
                nome: str, senha: str, telefone: str,
                aceita_apenas_tel_verf: bool, anos_mercado: int,
                avaliacao_media: float, horario_atendimento: datetime,
                quantidade_imoveis: int,
                telefone_verificado: bool = False):
        
        super().__init__(cpf, data_nascimento, email, nome, senha, telefone, telefone_verificado)
        
        self.__aceita_apenas_tel_verf = aceita_apenas_tel_verf
        self.__anos_mercado = anos_mercado
        self.__avaliacao_media = avaliacao_media
        self.__horario_atendimento = horario_atendimento
        self.__quantidade_imoveis = quantidade_imoveis
        
        self.__negociacoes = []
        self.__imoveis = []
        self.__anuncios = []

    @property
    def aceita_apenas_tel_verf(self):
        return self.__aceita_apenas_tel_verf
    
    @aceita_apenas_tel_verf.setter
    def aceita_apenas_tel_verf(self, value):
        self.__aceita_apenas_tel_verf = value
    
    @property
    def anos_mercado(self):
        return self.__anos_mercado
    
    @anos_mercado.setter
    def anos_mercado(self, value):
        self.__anos_mercado = value
    
    @property
    def avaliacao_media(self):
        return self.__avaliacao_media
    
    @avaliacao_media.setter
    def avaliacao_media(self, value):
        self.__avaliacao_media = value
    
    @property
    def horario_atendimento(self):
        return self.__horario_atendimento
    
    @horario_atendimento.setter
    def horario_atendimento(self, value):
        self.__horario_atendimento = value
    
    @property
    def quantidade_imoveis(self):
        return self.__quantidade_imoveis
    
    @quantidade_imoveis.setter
    def quantidade_imoveis(self, value):
        self.__quantidade_imoveis = value
    
    @property
    def negociacoes(self):
        return self.__negociacoes
    
    def adicionar_negociacoes(self, negociacao):
        self.__negociacoes.append(negociacao)

    @property
    def imoveis(self):
        return self.__imoveis
    
    def adicionar_imoveis(self, imoveis):
        self.__imoveis.append(imoveis)

    @property
    def anuncios(self):
        return self.__anuncios
    
    def adicionar_anuncios(self, anuncios):
        self.__anuncios.append(anuncios)

    def get_tipo_usuario(self):
        return "proprietario"
