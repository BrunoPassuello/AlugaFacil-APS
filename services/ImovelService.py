from typing import List, Optional, Tuple
from entities.Casa import Casa
from entities.Apartamento import Apartamento
from entities.Proprietario import Proprietario
from repository.ImovelRepositoryPickle import ImovelRepositoryPickle
from repository.CadastroRepositoryPickle import CadastroRepositoryPickle

class ImovelService:
    
    def __init__(self,
                 imovel_repo: Optional[ImovelRepositoryPickle] = None,
                 cadastro_repo: Optional[CadastroRepositoryPickle] = None):
        self._imovel_repo = imovel_repo or ImovelRepositoryPickle()
        self._cadastro_repo = cadastro_repo or CadastroRepositoryPickle()
    
    def cadastrar_casa(self,
                       proprietario_email: str,
                       endereco: str,
                       cidade: str,
                       metragem: float,
                       quartos: int,
                       banheiros: int,
                       possui_garagem: bool,
                       area_lazer: bool,
                       numero_pisos: int) -> Tuple[bool, Optional[Casa], str]:
        """
        Cadastra uma nova casa.
        Retorna: (sucesso, casa, mensagem)
        """
        try:
            proprietario = self._cadastro_repo.get_pessoa_email(proprietario_email)
            if not proprietario or not isinstance(proprietario, Proprietario):
                return False, None, "Proprietário não encontrado"
            
            casa = Casa(
                id=0,  
                endereco=endereco,
                cidade=cidade,
                metragem=metragem,
                quartos=quartos,
                banheiros=banheiros,
                possui_garagem=possui_garagem,
                proprietario=proprietario,
                area_lazer=area_lazer,
                numero_pisos=numero_pisos
            )
            
            casa_salva = self._imovel_repo.adicionar(casa)
            return True, casa_salva, "Casa cadastrada com sucesso!"
            
        except Exception as e:
            return False, None, f"Erro ao cadastrar casa: {str(e)}"
    
    def cadastrar_apartamento(self,
                            proprietario_email: str,
                            endereco: str,
                            cidade: str,
                            metragem: float,
                            quartos: int,
                            banheiros: int,
                            possui_garagem: bool,
                            andar: int,
                            possui_varanda: bool) -> Tuple[bool, Optional[Apartamento], str]:  # CORRIGIDO: possui_varanda
        """
        Cadastra um novo apartamento.
        Retorna: (sucesso, apartamento, mensagem)
        """
        try:
            proprietario = self._cadastro_repo.get_pessoa_email(proprietario_email)
            if not proprietario or not isinstance(proprietario, Proprietario):
                return False, None, "Proprietário não encontrado"
            
            apartamento = Apartamento(
                id=0,  
                endereco=endereco,
                cidade=cidade,
                metragem=metragem,
                quartos=quartos,
                banheiros=banheiros,
                possui_garagem=possui_garagem,
                proprietario=proprietario,
                andar=andar,
                possui_varanda=possui_varanda  
            )
            
            apto_salvo = self._imovel_repo.adicionar(apartamento)
            return True, apto_salvo, "Apartamento cadastrado com sucesso!"
            
        except Exception as e:
            return False, None, f"Erro ao cadastrar apartamento: {str(e)}"

    
    def listar_por_proprietario(self, email_proprietario: str) -> List:
        return self._imovel_repo.listar_por_proprietario(email_proprietario)
    
    def get_por_id(self, imovel_id: int):
        return self._imovel_repo.get_por_id(imovel_id)
    
    def remover(self, imovel_id: int) -> Tuple[bool, str]:
        sucesso = self._imovel_repo.remover(imovel_id)
        if sucesso:
            return True, "Imóvel removido com sucesso!"
        return False, "Imóvel não encontrado"

    def atualizar_imovel(self,
                        imovel_id: int,
                        proprietario_email: str,
                        endereco: str,
                        cidade: str,
                        metragem: float,
                        quartos: int,
                        banheiros: int,
                        possui_garagem: bool,
                        **kwargs) -> Tuple[bool, str]:
        """
        Atualiza um imóvel existente.
        kwargs pode conter campos específicos (area_lazer, numero_pisos, andar, possui_varanda)
        Retorna: (sucesso, mensagem)
        """
        try:
            imovel = self._imovel_repo.get_por_id(imovel_id)
            if not imovel:
                return False, "Imóvel não encontrado"
            
            if imovel.proprietario.email != proprietario_email:
                return False, "Você não tem permissão para editar este imóvel"
            
            imovel._endereco = endereco
            imovel._cidade = cidade
            imovel._metragem = metragem
            imovel._quartos = quartos
            imovel._banheiros = banheiros
            imovel._possui_garagem = possui_garagem
            
            if imovel.tipo_imovel() == 'casa':
                if 'area_lazer' in kwargs:
                    imovel._area_lazer = kwargs['area_lazer']
                if 'numero_pisos' in kwargs:
                    imovel._numero_pisos = kwargs['numero_pisos']
            elif imovel.tipo_imovel() == 'apartamento':
                if 'andar' in kwargs:
                    imovel._andar = kwargs['andar']
                if 'possui_varanda' in kwargs: 
                    imovel._possui_varanda = kwargs['possui_varanda']
            
            sucesso = self._imovel_repo.atualizar(imovel)
            if sucesso:
                return True, "Imóvel atualizado com sucesso!"
            return False, "Erro ao atualizar imóvel"
            
        except Exception as e:
            return False, f"Erro ao atualizar imóvel: {str(e)}"

