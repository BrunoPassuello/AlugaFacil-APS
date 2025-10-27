from typing import List, Dict, Optional

from repository.CadastroRepositoryPickle import CadastroRepositoryPickle
from entities.Anuncio import Anuncio
from entities.Locatario import Locatario


class FavoritoService:
    """Servico responsável por adicionar, listar e remover favoritos utilizando o repositorio Pickle."""

    def __init__(self, repo: Optional[CadastroRepositoryPickle] = None):
        self._repo = repo or CadastroRepositoryPickle()

    # ------------- METODOS PRIVADOS -------------

    def _get_locatario(self, email: str) -> Locatario:
        pessoa = self._repo.get_pessoa_email(email)
        if pessoa is None or pessoa.get_tipo_usuario() != "locatario":
            raise ValueError("Usuário não encontrado ou não é locatário")
        return pessoa  # type: ignore

    def _persist(self, email: str, locatario: Locatario):
        self._repo.update_cadastro(email, locatario)

    # ------------- API PUBLICA -------------

    def listar(self, email: str) -> List[Dict]:
        loc = self._get_locatario(email)
        return loc.get_favoritos()

    def adicionar(self, email: str, anuncio: Anuncio, anotacao: str = "") -> bool:
        loc = self._get_locatario(email)
        adicionado = loc.add_favorito(anuncio, anotacao)
        if adicionado:
            self._persist(email, loc)
        return adicionado

    def atualizar_anotacao(self, email: str, anuncio_id: int, nova_anotacao: str) -> bool:
        loc = self._get_locatario(email)
        ok = loc.update_anotacao(anuncio_id, nova_anotacao)
        if ok:
            self._persist(email, loc)
        return ok

    def remover(self, email: str, anuncio_id: int) -> bool:
        loc = self._get_locatario(email)
        ok = loc.remove_favorito(anuncio_id)
        if ok:
            self._persist(email, loc)
        return ok
