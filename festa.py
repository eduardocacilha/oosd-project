try:
    from .evento import Evento
    from .venda import Venda
    from .item_venda import ItemVenda
except ImportError:
    from evento import Evento  # type: ignore
    from venda import Venda  # type: ignore
    from item_venda import ItemVenda  # type: ignore
from typing import List
from datetime import datetime


class Festa(Evento):
    def __init__(self, nome: str, data: str, local: str, preco_entrada: float):
        super().__init__(nome=nome, data=data, local=local)
        self.__preco_entrada = preco_entrada
        self.__vendas_realizadas: List = []

    def registrar_venda(self, venda: Venda):
        """Registra uma venda de produtos na festa"""
        self.__vendas_realizadas.append(venda)

    def realizar_venda(self, usuario, itens_por_produto: dict):
        """Cria uma venda com os itens fornecidos e registra na festa.
        
        Args:
            usuario: Usuario que está fazendo a compra
            itens_por_produto: dict[Produto, int] - mapeamento produto->quantidade
        
        Returns:
            Venda: A venda criada
        """
        venda = Venda(
            id_venda=len(self.__vendas_realizadas) + 1, 
            metodo_pagamento="cartao", 
            data_hora=datetime.now()
        )
        
        for produto, quantidade in itens_por_produto.items():
            venda.adicionar_item(produto, int(quantidade))
        
        # Registra a venda na festa
        self.registrar_venda(venda)
        
        # Adiciona ao histórico do usuário
        if hasattr(usuario, 'adicionar_compra'):
            usuario.adicionar_compra(venda)
        
        return venda

    def listar_vendas(self):
        """Lista todas as vendas realizadas na festa"""
        return list(self.__vendas_realizadas)

    def obter_vendas_por_produto(self, produto):
        """Retorna todas as vendas que incluem um produto específico"""
        vendas_produto = []
        for venda in self.__vendas_realizadas:
            for item in venda.itens:
                if item.produto == produto:
                    vendas_produto.append((venda, item.quantidade))
                    break
        return vendas_produto

    @property
    def vendas_realizadas(self):
        return self.__vendas_realizadas
    
    @property
    def preco_entrada(self):
        return self.__preco_entrada

    @preco_entrada.setter
    def preco_entrada(self, valor):
        self.__preco_entrada = float(valor)

    def get_faturamento_total(self):
        """Calcula o faturamento total da festa (ingressos + vendas de produtos)"""
        receita_ingressos = self.obter_receita_ingressos()
        receita_vendas = sum(v.valor_total for v in self.__vendas_realizadas)
        return round(receita_ingressos + receita_vendas, 2)
