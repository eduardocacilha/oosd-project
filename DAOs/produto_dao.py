from DAOs.dao import DAO
from models.produto import Produto


class ProdutoDAO(DAO):

    def __init__(self):
        super().__init__("produtos.pkl")

    def add(self, produto: Produto):
        if (
            produto is not None
            and isinstance(produto, Produto)
            and isinstance(produto.nome, str)
        ):
            super().add(produto.nome, produto)

    def update(self, produto: Produto):
        if (
            produto is not None
            and isinstance(produto, Produto)
            and isinstance(produto.nome, str)
        ):
            super().update(produto.nome, produto)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
