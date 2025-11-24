from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict

@dataclass
class Anuncio:
    id: int
    titulo: str
    cidade: str
    endereco: str
    valor: float
    imagem_url: str
    data_postagem: datetime
    proprietario_email: str  
    imovel : object
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data["data_postagem"] = self.data_postagem.isoformat()
        data["imovel_id"] = self.imovel.id if self.imovel else None
        return data
