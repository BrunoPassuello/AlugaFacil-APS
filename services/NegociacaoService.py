from typing import List, Optional, Tuple
from datetime import date
from entities.Negociacao import Negociacao
from entities.StatusNegociacao import StatusNegociacao
from repository.NegociacaoRepositoryPickle import NegociacaoRepositoryPickle
from repository.CadastroRepositoryPickle import CadastroRepositoryPickle


class NegociacaoService:
    
    def __init__(self, 
                negociacao_repo: Optional[NegociacaoRepositoryPickle] = None,
                cadastro_repo: Optional[CadastroRepositoryPickle] = None):
        self._negociacao_repo = negociacao_repo or NegociacaoRepositoryPickle()
        self._cadastro_repo = cadastro_repo or CadastroRepositoryPickle()
    
    def criar_negociacao(self,
                        locatario_email: str,
                         proprietario_email: str,
                         anuncio_id: int,
                         valor_proposto: float,
                         observacoes: str = "") -> Tuple[bool, Optional[Negociacao], str]:
        """
        Cria uma nova negociação entre locatário e proprietário.
        
        Retorna: (sucesso, negociacao, mensagem)
        """
        try:
            locatario = self._cadastro_repo.get_pessoa_email(locatario_email)
            proprietario = self._cadastro_repo.get_pessoa_email(proprietario_email)
            
            if not locatario or locatario.get_tipo_usuario() != "locatario":
                return False, None, "Locatário não encontrado"
            
            if not proprietario or proprietario.get_tipo_usuario() != "proprietario":
                return False, None, "Proprietário não encontrado"
            
            if valor_proposto <= 0:
                return False, None, "Valor proposto deve ser maior que zero"
            
            negociacao = Negociacao(
                id=0,  
                avaliacao_locatario=0.0,
                avaliacao_proprietario=0.0,
                data_fim=None,
                data_inicio=date.today(),
                observacoes=observacoes,
                status=StatusNegociacao.INICIADA,
                valor_final=0.0,
                valor_proposto=valor_proposto,
                locatario_email=locatario_email.lower().strip(),
                proprietario_email=proprietario_email.lower().strip(),
                anuncio_id=anuncio_id
            )
            
            self._negociacao_repo.adicionar(negociacao)
            
            locatario.adicionar_negociacoes(negociacao.id)
            proprietario.adicionar_negociacoes(negociacao.id)
            self._cadastro_repo.update_cadastro(locatario_email, locatario)
            self._cadastro_repo.update_cadastro(proprietario_email, proprietario)
            
            return True, negociacao, "Negociação criada com sucesso"
        
        except Exception as e:
            return False, None, f"Erro ao criar negociação: {str(e)}"
    
    def aprovar_negociacao(self, negociacao_id: int, valor_final: float) -> Tuple[bool, str]:
        try:
            negociacao = self._negociacao_repo.get_por_id(negociacao_id)
            if not negociacao:
                return False, "Negociação não encontrada"
            
            if valor_final <= 0:
                return False, "Valor final deve ser maior que zero"
            
            negociacao.aprovar()
            negociacao.valor_final = valor_final
            self._negociacao_repo.atualizar(negociacao)
            
            return True, "Negociação aprovada com sucesso"
        
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao aprovar negociação: {str(e)}"
    
    def cancelar_negociacao(self, negociacao_id: int) -> Tuple[bool, str]:
        try:
            negociacao = self._negociacao_repo.get_por_id(negociacao_id)
            if not negociacao:
                return False, "Negociação não encontrada"
            
            negociacao.cancelar()
            self._negociacao_repo.atualizar(negociacao)
            
            return True, "Negociação cancelada com sucesso"
        
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao cancelar negociação: {str(e)}"
    
    def finalizar_negociacao(self, negociacao_id: int) -> Tuple[bool, str]:
        try:
            negociacao = self._negociacao_repo.get_por_id(negociacao_id)
            if not negociacao:
                return False, "Negociação não encontrada"
            
            negociacao.finalizar()
            self._negociacao_repo.atualizar(negociacao)
            
            return True, "Negociação finalizada com sucesso"
        
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao finalizar negociação: {str(e)}"
    
    def avaliar_locatario(self, negociacao_id: int, nota: float) -> Tuple[bool, str]:
        try:
            if nota < 0 or nota > 5:
                return False, "Nota deve estar entre 0 e 5"
            
            negociacao = self._negociacao_repo.get_por_id(negociacao_id)
            if not negociacao:
                return False, "Negociação não encontrada"
            
            negociacao.avaliacao_locatario = nota
            self._negociacao_repo.atualizar(negociacao)
            
            return True, "Avaliação registrada com sucesso"
        
        except Exception as e:
            return False, f"Erro ao avaliar: {str(e)}"
    
    def avaliar_proprietario(self, negociacao_id: int, nota: float) -> Tuple[bool, str]:
        try:
            if nota < 0 or nota > 5:
                return False, "Nota deve estar entre 0 e 5"
            
            negociacao = self._negociacao_repo.get_por_id(negociacao_id)
            if not negociacao:
                return False, "Negociação não encontrada"
            
            negociacao.avaliacao_proprietario = nota
            self._negociacao_repo.atualizar(negociacao)
            
            return True, "Avaliação registrada com sucesso"
        
        except Exception as e:
            return False, f"Erro ao avaliar: {str(e)}"
    
    def listar_por_locatario(self, locatario_email: str) -> List[Negociacao]:
        return self._negociacao_repo.get_por_locatario(locatario_email)
    
    def listar_por_proprietario(self, proprietario_email: str) -> List[Negociacao]:
        return self._negociacao_repo.get_por_proprietario(proprietario_email)
    
    def listar_por_anuncio(self, anuncio_id: int) -> List[Negociacao]:
        return self._negociacao_repo.get_por_anuncio(anuncio_id)
    
    def get_por_id(self, negociacao_id: int) -> Optional[Negociacao]:
        return self._negociacao_repo.get_por_id(negociacao_id)
    
    def listar_todas(self) -> List[Negociacao]:
        return self._negociacao_repo.get_all()