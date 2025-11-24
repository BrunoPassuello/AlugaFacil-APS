from entities.Imovel import Imovel

class Apartamento(Imovel):
    def __init__(self, id, endereco, cidade, metragem, quartos, banheiros, possui_garagem, proprietario, andar: int, possui_varanda: bool):
        super().__init__(id, endereco, cidade, metragem, quartos, banheiros, possui_garagem, proprietario)
        self._andar = andar
        self._possui_varanda = possui_varanda

    def tipo_imovel(self):
        return "apartamento"

    @property
    def andar(self):
        return self._andar

    @property
    def possui_varanda(self):
        return self._possui_varanda

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "andar": self.andar,
            "possui_varanda": self.possui_varanda
        })
        return data
