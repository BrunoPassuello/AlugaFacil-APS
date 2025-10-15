from entities.Pessoa import Pessoa
class Locatario(Pessoa):
    
    def __init__(self, cpf: str, data_nascimento: str, email: str,
                nome: str, senha: str, telefone: str,
                estudante: bool, fumante: bool,
                instituicao_ensino_str: str, observacoes_str: str,
                possui_pet: bool, profissao_str: str,
                tipo_pet_str: str,
                telefone_verificado: bool = False):
        
        super().__init__(cpf, data_nascimento, email, nome, senha, telefone, telefone_verificado)
        
        self.__estudante = estudante
        self.__fumante = fumante
        self.__instituicao_ensino_str = instituicao_ensino_str
        self.__observacoes_str = observacoes_str
        self.__possui_pet = possui_pet
        self.__profissao_str = profissao_str
        self.__tipo_pet_str = tipo_pet_str
        
        self.__negociacoes = []
    
    @property
    def estudante(self):
        return self.__estudante
    
    @estudante.setter
    def estudante(self, value):
        self.__estudante = value
    
    @property
    def fumante(self):
        return self.__fumante
    
    @fumante.setter
    def fumante(self, value):
        self.__fumante = value
    
    @property
    def instituicao_ensino_str(self):
        return self.__instituicao_ensino_str
    
    @instituicao_ensino_str.setter
    def instituicao_ensino_str(self, value):
        self.__instituicao_ensino_str = value
    
    @property
    def observacoes_str(self):
        return self.__observacoes_str
    
    @observacoes_str.setter
    def observacoes_str(self, value):
        self.__observacoes_str = value
    
    @property
    def possui_pet(self):
        return self.__possui_pet
    
    @possui_pet.setter
    def possui_pet(self, value):
        self.__possui_pet = value
    
    @property
    def profissao_str(self):
        return self.__profissao_str
    
    @profissao_str.setter
    def profissao_str(self, value):
        self.__profissao_str = value
    
    @property
    def tipo_pet_str(self):
        return self.__tipo_pet_str
    
    @tipo_pet_str.setter
    def tipo_pet_str(self, value):
        self.__tipo_pet_str = value
    
    @property
    def anuncios_salvos(self):
        return self.__anuncios_salvos
    
    @anuncios_salvos.setter
    def anuncios_salvos(self, value):
        self.__anuncios_salvos = value
    
    @property
    def filtros_personalizados(self):
        return self.__filtros_personalizados
    
    @filtros_personalizados.setter
    def filtros_personalizados(self, value):
        self.__filtros_personalizados = value
    
    @property
    def visitas_agendadas(self):
        return self.__visitas_agendadas
    
    @visitas_agendadas.setter
    def visitas_agendadas(self, value):
        self.__visitas_agendadas = value
    
    @property
    def negociacoes(self):
        return self.__negociacoes
    
    def adicionar_negociacoes(self, negociacao):
        self.__negociacoes.append(negociacao)

    def get_tipo_usuario(self):
        return "locatario"