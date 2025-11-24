from entities.Imovel import Imovel

class Casa(Imovel):
    def __init__(self, id, endereco, cidade, metragem, quartos, banheiros, possui_garagem, proprietario, area_lazer: bool, numero_pisos: int):
        super().__init__(id, endereco, cidade, metragem, quartos, banheiros, possui_garagem, proprietario)
        self._area_lazer = area_lazer
        self._numero_pisos = numero_pisos

    def tipo_imovel(self):
        return "casa"

    @property
    def area_lazer(self):
        return self._area_lazer

    @property
    def numero_pisos(self):
        return self._numero_pisos

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "area_lazer": self.area_lazer,
            "numero_pisos": self.numero_pisos
        })
        return data
