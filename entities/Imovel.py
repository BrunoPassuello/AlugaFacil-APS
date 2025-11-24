from abc import ABC, abstractmethod

class Imovel(ABC):
    def __init__(self, id: int, endereco: str, cidade: str, metragem: float, quartos: int, banheiros: int, possui_garagem: bool, proprietario):
        self._id = id
        self._endereco = endereco
        self._cidade = cidade
        self._metragem = metragem
        self._quartos = quartos
        self._banheiros = banheiros
        self._possui_garagem = possui_garagem
        self._proprietario = proprietario  
        self._anuncio = None

    @property
    def id(self):
        return self._id

    @property
    def endereco(self):
        return self._endereco

    @property
    def cidade(self):
        return self._cidade

    @property
    def metragem(self):
        return self._metragem

    @property
    def quartos(self):
        return self._quartos

    @property
    def banheiros(self):
        return self._banheiros

    @property
    def possui_garagem(self):
        return self._possui_garagem

    @property
    def proprietario(self):
        return self._proprietario

    @proprietario.setter
    def proprietario(self, value):
        self._proprietario = value

    @property
    def anuncio(self):
        return self._anuncio

    @anuncio.setter
    def anuncio(self, value):
        self._anuncio = value

    @abstractmethod
    def tipo_imovel(self):
        pass

    def to_dict(self):
        return {
            "id": self.id,
            "endereco": self.endereco,
            "cidade": self.cidade,
            "metragem": self.metragem,
            "quartos": self.quartos,
            "banheiros": self.banheiros,
            "possui_garagem": self.possui_garagem,
            "proprietario_email": self.proprietario.email if self.proprietario else None,
            "anuncio_id": self.anuncio.id if self.anuncio else None,
            "tipo": self.tipo_imovel()
        }
