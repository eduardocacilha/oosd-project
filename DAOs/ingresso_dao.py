from DAOs.dao import DAO
from models.ingresso import Ingresso


class IngressoDAO(DAO):
    def __init__(self):
        super().__init__("ingressos.pkl")

    def add(self, ingresso: Ingresso):
        if (
            ingresso
            and isinstance(ingresso, Ingresso)
            and isinstance(ingresso.id_ingresso, int)
        ):
            super().add(ingresso.id_ingresso, ingresso)

    def update(self, ingresso: Ingresso):
        if (
            ingresso
            and isinstance(ingresso, Ingresso)
            and isinstance(ingresso.id_ingresso, int)
        ):
            super().update(ingresso.id_ingresso, ingresso)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
