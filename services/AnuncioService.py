from datetime import datetime
from typing import List, Optional, Tuple
from entities.Anuncio import Anuncio
from repository.AnuncioRepositoryPickle import AnuncioRepositoryPickle
from repository.ImovelRepositoryPickle import ImovelRepositoryPickle

class AnuncioService:    
    def __init__(self,
                 anuncio_repo: Optional[AnuncioRepositoryPickle] = None,
                 imovel_repo: Optional[ImovelRepositoryPickle] = None):
        self._anuncio_repo = anuncio_repo or AnuncioRepositoryPickle()
        self._imovel_repo = imovel_repo or ImovelRepositoryPickle()
    
    def criar_anuncio(self,
                     proprietario_email: str,
                     imovel_id: int,
                     titulo: str,
                     valor: float,
                     imagem_url: str = "https://i.ibb.co/9q0N4pG/door-key.jpg") -> Tuple[bool, Optional[Anuncio], str]:
        """
        Cria um novo anúncio para um imóvel.
        Retorna: (sucesso, anuncio, mensagem)
        """
        try:
            imovel = self._imovel_repo.get_por_id(imovel_id)
            if not imovel:
                return False, None, "Imóvel não encontrado"
            
            if imovel.proprietario.email != proprietario_email:
                return False, None, "Você não tem permissão para anunciar este imóvel"
            
            anuncio_id = self._anuncio_repo.gerar_proximo_id()
            anuncio = Anuncio(
                id=anuncio_id,
                titulo=titulo,
                cidade=imovel.cidade,
                endereco=imovel.endereco,
                valor=valor,
                imagem_url=imagem_url,
                data_postagem=datetime.now(),
                proprietario_email=proprietario_email,
                imovel=imovel
            )
            
            anuncio_salvo = self._anuncio_repo.adicionar(anuncio)
            return True, anuncio_salvo, "Anúncio criado com sucesso!"
            
        except Exception as e:
            return False, None, f"Erro ao criar anúncio: {str(e)}"
    
    def listar(self) -> List[Anuncio]:
        return self._anuncio_repo.listar_todos()
    
    def listar_por_proprietario(self, email_proprietario: str) -> List[Anuncio]:
        return self._anuncio_repo.listar_por_proprietario(email_proprietario)
    
    def get_por_id(self, anuncio_id: int) -> Optional[Anuncio]:
        return self._anuncio_repo.get_por_id(anuncio_id)
    
    def remover(self, anuncio_id: int, proprietario_email: str) -> Tuple[bool, str]:
        anuncio = self._anuncio_repo.get_por_id(anuncio_id)
        if not anuncio:
            return False, "Anúncio não encontrado"
        
        if anuncio.proprietario_email != proprietario_email:
            return False, "Você não tem permissão para remover este anúncio"
        
        sucesso = self._anuncio_repo.remover(anuncio_id)
        if sucesso:
            return True, "Anúncio removido com sucesso!"
        return False, "Erro ao remover anúncio"

    def atualizar_anuncio(self,
                        anuncio_id: int,
                        proprietario_email: str,
                        titulo: str,
                        valor: float,
                        imagem_url: str) -> Tuple[bool, str]:
        """
        Atualiza um anúncio existente.
        Retorna: (sucesso, mensagem)
        """
        try:
            anuncio = self._anuncio_repo.get_por_id(anuncio_id)
            if not anuncio:
                return False, "Anúncio não encontrado"
            
            if anuncio.proprietario_email != proprietario_email:
                return False, "Você não tem permissão para editar este anúncio"
            
            from dataclasses import replace
            anuncio_atualizado = replace(
                anuncio,
                titulo=titulo,
                valor=valor,
                imagem_url=imagem_url
            )
            
            sucesso = self._anuncio_repo.atualizar(anuncio_atualizado)
            if sucesso:
                return True, "Anúncio atualizado com sucesso!"
            return False, "Erro ao atualizar anúncio"
            
        except Exception as e:
            return False, f"Erro ao atualizar anúncio: {str(e)}"
