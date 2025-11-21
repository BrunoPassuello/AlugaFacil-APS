import pickle
from typing import List, Dict, Optional
from entities.Visita import Visita
from repository.VisitaRepository import VisitaRepository


class VisitaRepositoryPickle(VisitaRepository):
    """Implementação de repositório de visitas usando pickle."""
    
    def __init__(self, arquivo='visitas.pkl'):
        self.__arquivo = arquivo
        # {id: Visita}
        self.__visitas: Dict[int, Visita] = self.carregar()
    
    def carregar(self) -> Dict[int, Visita]:
        """Carrega visitas do arquivo pickle."""
        try:
            with open(self.__arquivo, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}
    
    def salvar(self) -> None:
        """Salva visitas no arquivo pickle."""
        with open(self.__arquivo, 'wb') as f:
            pickle.dump(self.__visitas, f)
    
    def _get_proximo_id(self) -> int:
        """Retorna o próximo ID disponível."""
        if not self.__visitas:
            return 1
        return max(self.__visitas.keys()) + 1
    
    def adicionar(self, visita: Visita) -> None:
        """Adiciona uma nova visita."""
        if visita.id == 0:
            visita.id = self._get_proximo_id()
        
        if visita.id in self.__visitas:
            raise ValueError(f"Visita com ID {visita.id} já existe")
        
        self.__visitas[visita.id] = visita
        self.salvar()
    
    def get_por_id(self, visita_id: int) -> Optional[Visita]:
        """Retorna uma visita por ID."""
        self.__visitas = self.carregar()
        return self.__visitas.get(visita_id)
    
    def get_por_negociacao(self, negociacao_id: int) -> List[Visita]:
        """Retorna todas as visitas de uma negociação."""
        self.__visitas = self.carregar()
        return [v for v in self.__visitas.values() if v.negociacao_id == negociacao_id]
    
    def atualizar(self, visita: Visita) -> None:
        """Atualiza uma visita existente."""
        if visita.id not in self.__visitas:
            raise ValueError(f"Visita com ID {visita.id} não encontrada")
        
        self.__visitas[visita.id] = visita
        self.salvar()
    
    def deletar(self, visita_id: int) -> bool:
        """Remove uma visita."""
        if visita_id in self.__visitas:
            del self.__visitas[visita_id]
            self.salvar()
            return True
        return False
    
    def get_all(self) -> List[Visita]:
        """Retorna todas as visitas."""
        self.__visitas = self.carregar()
        return list(self.__visitas.values())