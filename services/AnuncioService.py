from datetime import datetime
from typing import List, Optional
from entities.Anuncio import Anuncio

class AnuncioService:
    """Serviço que fornece o catálogo de anúncios (mock em memória)."""
    
    def __init__(self):
        self._anuncios = self._carregar_mock()
    
    def _carregar_mock(self) -> List[Anuncio]:
        """Carrega alguns anúncios de teste."""
        return [
            Anuncio(
                id=1,
                titulo="Anúncio 1",
                cidade="Florianópolis - SC",
                endereco="Avenida Mauro Ramos, 1306, Centro",
                valor=800.0,
                imagem_url="https://i.ibb.co/9q0N4pG/door-key.jpg",
                data_postagem=datetime(2025, 9, 17),
                proprietario_email="proprietario1@email.com"
            ),
            Anuncio(
                id=2,
                titulo="Anúncio 2",
                cidade="Florianópolis - SC",
                endereco="Avenida Mauro Ramos, 1306, Centro",
                valor=800.0,
                imagem_url="https://i.ibb.co/9q0N4pG/door-key.jpg",
                data_postagem=datetime(2025, 9, 17),
                proprietario_email="proprietario2@email.com"
            ),
            Anuncio(
                id=3,
                titulo="Anúncio 3",
                cidade="Florianópolis - SC",
                endereco="Avenida Mauro Ramos, 1306, Centro",
                valor=800.0,
                imagem_url="https://i.ibb.co/9q0N4pG/door-key.jpg",
                data_postagem=datetime(2025, 9, 17),
                proprietario_email="proprietario1@email.com"
            ),
        ]
    
    # ------------------ API PÚBLICA ------------------
    
    def listar(self) -> List[Anuncio]:
        return list(self._anuncios)
    
    def get_por_id(self, anuncio_id: int) -> Optional[Anuncio]:
        return next((a for a in self._anuncios if a.id == anuncio_id), None)
