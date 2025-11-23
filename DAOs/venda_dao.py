from DAOs.dao import DAO
from models.venda import Venda


class VendaDAO(DAO):
    def __init__(self):
        super().__init__("vendas.pkl")

    def add(self, venda: Venda):
        if venda and isinstance(venda, Venda) and isinstance(venda.id_venda, int):
            super().add(venda.id_venda, venda)

    def update(self, venda: Venda):
        if venda and isinstance(venda, Venda) and isinstance(venda.id_venda, int):
            super().update(venda.id_venda, venda)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
