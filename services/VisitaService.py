from typing import List, Optional, Tuple
from datetime import date, time
from entities.Visita import Visita
from entities.StatusVisita import StatusVisita
from repository.VisitaRepositoryPickle import VisitaRepositoryPickle
from repository.NegociacaoRepositoryPickle import NegociacaoRepositoryPickle


class VisitaService:
    """Serviço responsável pela lógica de negócio de visitas."""
    
    def __init__(self, 
                visita_repo: Optional[VisitaRepositoryPickle] = None,
                negociacao_repo: Optional[NegociacaoRepositoryPickle] = None):
        self._visita_repo = visita_repo or VisitaRepositoryPickle()
        self._negociacao_repo = negociacao_repo or NegociacaoRepositoryPickle()
    
    def agendar_visita(self,
                    negociacao_id: int,
                    data_agendada: date,
                    hora_agendada: time,
                    observacoes: str = "") -> Tuple[bool, Optional[Visita], str]:
        """
        Agenda uma nova visita para uma negociação.
        Retorna: (sucesso, visita, mensagem)
        """
        try:
            # Valida se a negociação existe
            negociacao = self._negociacao_repo.get_por_id(negociacao_id)
            if not negociacao:
                return False, None, "Negociação não encontrada"
            
            # Valida se a data é futura
            from datetime import datetime
            data_hora_agendada = datetime.combine(data_agendada, hora_agendada)
            if data_hora_agendada < datetime.now():
                return False, None, "Data e hora devem ser futuras"
            
            # Cria a visita
            visita = Visita(
                id=0,  # Será atribuído pelo repositório
                data_agendada=data_agendada,
                hora_agendada=hora_agendada,
                observacoes=observacoes,
                status=StatusVisita.AGENDADA,
                negociacao_id=negociacao_id
            )
            
            self._visita_repo.adicionar(visita)
            
            return True, visita, "Visita agendada com sucesso"
        
        except Exception as e:
            return False, None, f"Erro ao agendar visita: {str(e)}"
    
    def realizar_visita(self, visita_id: int) -> Tuple[bool, str]:
        """Marca uma visita como realizada."""
        try:
            visita = self._visita_repo.get_por_id(visita_id)
            if not visita:
                return False, "Visita não encontrada"
            
            visita.realizar()
            self._visita_repo.atualizar(visita)
            
            return True, "Visita marcada como realizada"
        
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao realizar visita: {str(e)}"
    
    def cancelar_visita(self, visita_id: int) -> Tuple[bool, str]:
        """Cancela uma visita."""
        try:
            visita = self._visita_repo.get_por_id(visita_id)
            if not visita:
                return False, "Visita não encontrada"
            
            visita.cancelar()
            self._visita_repo.atualizar(visita)
            
            return True, "Visita cancelada com sucesso"
        
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao cancelar visita: {str(e)}"
    
    def registrar_nao_comparecimento(self, visita_id: int) -> Tuple[bool, str]:
        """Registra que o locatário não compareceu à visita."""
        try:
            visita = self._visita_repo.get_por_id(visita_id)
            if not visita:
                return False, "Visita não encontrada"
            
            visita.registrar_nao_comparecimento()
            self._visita_repo.atualizar(visita)
            
            return True, "Não comparecimento registrado"
        
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao registrar não comparecimento: {str(e)}"
    
    def reagendar_visita(self,
                         visita_id: int,
                         nova_data: date,
                         nova_hora: time) -> Tuple[bool, str]:
        """Reagenda uma visita para nova data e hora."""
        try:
            visita = self._visita_repo.get_por_id(visita_id)
            if not visita:
                return False, "Visita não encontrada"
            
            # Valida se a nova data é futura
            from datetime import datetime
            data_hora_agendada = datetime.combine(nova_data, nova_hora)
            if data_hora_agendada < datetime.now():
                return False, "Nova data e hora devem ser futuras"
            
            visita.reagendar(nova_data, nova_hora)
            self._visita_repo.atualizar(visita)
            
            return True, "Visita reagendada com sucesso"
        
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao reagendar visita: {str(e)}"
    
    def atualizar_observacoes(self, visita_id: int, observacoes: str) -> Tuple[bool, str]:
        """Atualiza as observações de uma visita."""
        try:
            visita = self._visita_repo.get_por_id(visita_id)
            if not visita:
                return False, "Visita não encontrada"
            
            visita.observacoes = observacoes
            self._visita_repo.atualizar(visita)
            
            return True, "Observações atualizadas com sucesso"
        
        except Exception as e:
            return False, f"Erro ao atualizar observações: {str(e)}"
    
    def listar_por_negociacao(self, negociacao_id: int) -> List[Visita]:
        """Lista todas as visitas de uma negociação."""
        return self._visita_repo.get_por_negociacao(negociacao_id)
    
    def get_por_id(self, visita_id: int) -> Optional[Visita]:
        """Retorna uma visita por ID."""
        return self._visita_repo.get_por_id(visita_id)
    
    def listar_todas(self) -> List[Visita]:
        """Lista todas as visitas."""
        return self._visita_repo.get_all()