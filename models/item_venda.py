from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

class ItemVenda:
    def __init__(self, produto, quantidade: int, preco_unitario: float):

        if not produto:
            raise RegraDeNegocioException("Produto não pode ser nulo.")

        if not isinstance(quantidade, int) or quantidade <= 0:
            raise RegraDeNegocioException("Quantidade deve ser um número inteiro positivo.")

        if not isinstance(preco_unitario, (int, float)) or preco_unitario < 0:
            raise RegraDeNegocioException("Preço unitário deve ser um número não negativo.")

        self.__produto = produto
        self.__quantidade = quantidade
        self.__preco_unitario = float(preco_unitario)

    @property
    def produto(self):
        return self.__produto

    @property
    def quantidade(self) -> int:
        return self.__quantidade

    @property
    def preco_unitario(self) -> float:
        return self.__preco_unitario

    @property
    def subtotal(self) -> float:
        return self.__quantidade * self.__preco_unitario

    def __str__(self) -> str:
        return f"{self.__produto.nome} - Qtd: {self.__quantidade} - Preço Unit: R$ {self.__preco_unitario:.2f} - Subtotal: R$ {self.subtotal:.2f}"
