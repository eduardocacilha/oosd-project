from typing import List, Optional
import FreeSimpleGUI as sg

class ProdutoView:
    
    def tela_opcoes(self) -> int:
        print("\n-------- MENU PRODUTOS ----------")
        print("1 - Adicionar Produto a um Evento")
        print("2 - Alterar Produto")
        print("3 - Listar Produtos de um Evento")
        print("4 - Excluir Produto")
        print("5 - Registrar Venda")
        print("6 - Relatório de Vendas")
        print("0 - Retornar ao Menu Principal")
        
        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            return -1

    def escolher_tipo_produto(self) -> int:
        print("\n-------- TIPO DE PRODUTO ----------")
        print("1 - Camisa")
        print("2 - Copo")
        print("0 - Cancelar")
        
        try:
            return int(input("Escolha o tipo: "))
        except ValueError:
            return -1

    def pega_dados_camisa(self) -> dict:
        print("\n-------- DADOS DA CAMISA ----------")
        
        while True:
            nome = input("Nome da camisa: ").strip()
            if nome:
                break
            print("Nome não pode estar vazio!")
        
        while True:
            try:
                preco = float(input("Preço: R$ "))
                if preco > 0:
                    break
                else:
                    print("Preço deve ser maior que zero!")
            except ValueError:
                print("Preço inválido! Digite um número.")
        
        while True:
            try:
                estoque = int(input("Quantidade em estoque: "))
                if estoque >= 0:
                    break
                else:
                    print("Estoque não pode ser negativo!")
            except ValueError:
                print("Quantidade inválida! Digite um número inteiro.")
        
        while True:
            tamanho = input("Tamanho (P/M/G/GG): ").upper().strip()
            if tamanho in ["P", "M", "G", "GG"]:
                break
            print("Tamanho inválido! Use: P, M, G ou GG")
        
        while True:
            cor = input("Cor: ").strip()
            if cor:
                break
            print("Cor não pode estar vazia!")
        
        return {
            "nome": nome,
            "preco": preco,
            "estoque": estoque,
            "tamanho": tamanho,
            "cor": cor
        }

    def pega_dados_copo(self) -> dict:
        print("\n-------- DADOS DO COPO ----------")
        
        while True:
            nome = input("Nome do copo: ").strip()
            if nome:
                break
            print("Nome não pode estar vazio!")
        
        while True:
            try:
                preco = float(input("Preço: R$ "))
                if preco > 0:
                    break
                else:
                    print("Preço deve ser maior que zero!")
            except ValueError:
                print("Preço inválido! Digite um número.")
        
        while True:
            try:
                estoque = int(input("Quantidade em estoque: "))
                if estoque >= 0:
                    break
                else:
                    print("Estoque não pode ser negativo!")
            except ValueError:
                print("Quantidade inválida! Digite um número inteiro.")
        
        while True:
            try:
                capacidade = int(input("Capacidade (ml): "))
                if capacidade > 0:
                    break
                else:
                    print("Capacidade deve ser maior que zero!")
            except ValueError:
                print("Capacidade inválida! Digite um número inteiro.")
        
        while True:
            material = input("Material: ").strip()
            if material:
                break
            print("Material não pode estar vazio!")
        
        return {
            "nome": nome,
            "preco": preco,
            "estoque": estoque,
            "capacidade_ml": capacidade,
            "material": material
        }

    def mostra_produtos(self, lista_produtos: List[dict]):
        if not lista_produtos:
            print("\nNenhum produto cadastrado para este evento.")
            return
        
        print("\n-------- PRODUTOS DO EVENTO ----------")
        for i, produto in enumerate(lista_produtos, 1):
            print(f"{i}. {produto['descricao']} - R$ {produto['preco']:.2f} - Estoque: {produto['estoque']}")

    def seleciona_produto(self, lista_produtos: List[dict]) -> Optional[int]:
        if not lista_produtos:
            print("\nNenhum produto disponível.")
            return None
        
        self.mostra_produtos(lista_produtos)
        print("0 - Cancelar")
        
        try:
            opcao = int(input("Selecione o NÚMERO do produto: "))
            if opcao == 0:
                return None
            if 1 <= opcao <= len(lista_produtos):
                return opcao - 1
            else:
                print("Opção inválida.")
                return None
        except ValueError:
            print("Opção inválida.")
            return None

    def pega_quantidade_venda(self) -> int:
        return int(input("Quantidade: "))

    def pega_metodo_pagamento(self) -> str:
        print("\n-------- MÉTODO DE PAGAMENTO ----------")
        print("1 - Dinheiro")
        print("2 - PIX")
        print("3 - Débito")
        print("4 - Crédito")
        
        try:
            opcao = int(input("Escolha o método: "))
            metodos = {1: "Dinheiro", 2: "PIX", 3: "Débito", 4: "Crédito"}
            return metodos.get(opcao, "Dinheiro")
        except ValueError:
            return "Dinheiro"

    def mostra_venda_realizada(self, dados_venda: dict):
        print(f"\nVENDA REALIZADA COM SUCESSO!")
        print(f"ID da Venda: {dados_venda['id_venda']}")
        print(f"Cliente: {dados_venda['cliente']}")
        print(f"Evento: {dados_venda['evento']}")
        print(f"Total: R$ {dados_venda['total']:.2f}")
        print(f"Método: {dados_venda['metodo']}")

    def mostra_relatorio_vendas(self, lista_vendas: List[dict]):
        if not lista_vendas:
            print("\nNenhuma venda registrada.")
            return
        
        print("\n-------- RELATÓRIO DE VENDAS ----------")
        total_geral = 0
        for venda in lista_vendas:
            print(f"Venda {venda['id_venda']} - {venda['cliente']} - {venda['evento']}")
            print(f"  Data: {venda['data']} - Método: {venda['metodo']} - Total: R$ {venda['total']:.2f}")
            total_geral += venda['total']
        
        print(f"\nTOTAL GERAL: R$ {total_geral:.2f}")

    def mostra_mensagem(self, msg: str):
        print(f"\n{msg}\n")