from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict


@dataclass
class Anuncio:
    """Entidade de domínio que representa um anúncio de imóvel exibido ao locatário."""
    id: int
    titulo: str
    cidade: str
    endereco: str
    valor: float
    imagem_url: str
    data_postagem: datetime

    def to_dict(self) -> Dict:
        """Converte a instância em um dicionário serializável (útil para JSON/UI)."""
        data = asdict(self)
        # dataclass converte datetime para objeto datetime; transformar em isoformat p/ serialização
        data["data_postagem"] = self.data_postagem.isoformat()
        return data
