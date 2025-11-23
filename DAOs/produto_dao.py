from DAOs.dao import DAO
from models.produto import Produto


class ProdutoDAO(DAO):

    def __init__(self):
        super().__init__("produtos.pkl")

    def add(self, produto: Produto):
        if (
            produto is not None
            and isinstance(produto, Produto)
            and isinstance(produto.nome, int)
        ):
            super().add(produto.nome, produto)

    def update(self, produto: Produto):
        if (
            produto is not None
            and isinstance(produto, Produto)
            and isinstance(produto.nome, int)
        ):
            super().update(produto.nome, produto)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
