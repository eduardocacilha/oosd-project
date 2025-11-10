from typing import List, Optional
import PySimpleGUI as sg

class IngressoView:
    
    def tela_opcoes_revenda(self) -> int:
        print("\n-------- MENU REVENDA ----------")
        print("1 - Colocar Ingresso à Venda")
        print("2 - Remover Ingresso da Venda")
        print("3 - Comprar Ingresso de Revenda")
        print("4 - Listar Meus Ingressos à Venda")
        print("0 - Retornar")

        while True:
            try:
                opcao = int(input("Escolha a opção: "))
                if 0 <= opcao <= 4:
                    return opcao
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Entrada inválida! Por favor, digite um número.")

    def pega_novo_preco_revenda(self) -> Optional[float]:
        while True:
            try:
                preco_str = input("Digite o novo preço para revenda: R$ ")
                return float(preco_str)
            except ValueError:
                print("Preço inválido. Por favor, digite um número (ex: 50.00).")

    def mostra_ingresso(self, dados_ingresso: dict):
        print(f"Evento: {dados_ingresso['nome_evento']}")
        print(f"Comprador: {dados_ingresso['nome_comprador']}")
        print(f"Data da Compra: {dados_ingresso['data_compra']}")
        print(f"Preço: R$ {dados_ingresso['preco']:.2f}")
        
        if dados_ingresso.get('nome_revendedor'):
            print(f"Status: À venda por {dados_ingresso['nome_revendedor']}")
        else:
            print("Status: Uso pessoal")
        print("-----------------------------")

    def mostra_ingressos(self, lista_dados_ingressos: List[dict]):
        if not lista_dados_ingressos:
            print("\nNenhum ingresso encontrado.")
        else:
            print("\n-------- LISTA DE INGRESSOS ----------")
            for i, dados in enumerate(lista_dados_ingressos, 1):
                print(f"Ingresso #{i}")
                self.mostra_ingresso(dados)

    def mostra_ingressos_revenda(self, lista_dados_ingressos: List[dict]):
        if not lista_dados_ingressos:
            print("\nNenhum ingresso disponível para revenda no momento.")
        else:
            print("\n-------- INGRESSOS DISPONÍVEIS PARA REVENDA ----------")
            for i, dados in enumerate(lista_dados_ingressos, 1):
                print(f"{i}. Evento: {dados['nome_evento']}")
                print(f"   Vendido por: {dados['nome_revendedor']}")
                print(f"   Preço: R$ {dados['preco']:.2f}")
                print("-----------------------------")

    def seleciona_ingresso(self, lista_dados_ingressos: List[dict]) -> Optional[int]:
        print("\n--- Selecione um de seus ingressos ---")
        self.mostra_ingressos(lista_dados_ingressos)
        
        if not lista_dados_ingressos:
            return None
            
        while True:
            try:
                escolha = input("Selecione o número do ingresso (ou 0 para cancelar): ")
                indice = int(escolha) - 1
                
                if indice == -1:
                    return None
                    
                if 0 <= indice < len(lista_dados_ingressos):
                    return indice
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Por favor, digite um número válido.")

    def seleciona_ingresso_revenda(self, lista_dados_ingressos: List[dict]) -> Optional[int]:
        self.mostra_ingressos_revenda(lista_dados_ingressos)
        if not lista_dados_ingressos:
            return None

        while True:
            try:
                escolha = input("Selecione o número do ingresso que deseja comprar (ou 0 para cancelar): ")
                indice = int(escolha) - 1

                if indice == -1:
                    return None
                if 0 <= indice < len(lista_dados_ingressos):
                    return indice
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número válido.")

    def pega_matricula_comprador(self) -> str:
        while True:
            matricula = input("Digite a matricula do comprador: ").strip()
            if matricula and matricula.isdigit():
                return matricula
            print("Matricula deve conter apenas numeros!")

    def pega_metodo_pagamento(self) -> str:
        while True:
            print("\n-------- METODO DE PAGAMENTO ----------")
            print("1 - Dinheiro")
            print("2 - PIX")
            print("3 - Debito")
            print("4 - Credito")
            
            try:
                opcao = int(input("Escolha o metodo: "))
                if opcao == 1:
                    return "Dinheiro"
                elif opcao == 2:
                    return "PIX"
                elif opcao == 3:
                    return "Debito"
                elif opcao == 4:
                    return "Credito"
                else:
                    print("Opcao invalida. Tente novamente.")
            except ValueError:
                print("Entrada invalida. Digite um numero.")

    def confirma_compra_ingresso(self, dados: dict):
        print("\n--- CONFIRMAR COMPRA ---")
        print(f"Evento: {dados['evento']}")
        print(f"Preco: R$ {dados['preco']:.2f}")
        print(f"Metodo de Pagamento: {dados['metodo_pagamento']}")
        
        while True:
            try:
                opcao = input("Confirmar compra? (s/n): ").lower()
                if opcao == 's':
                    return True
                elif opcao == 'n':
                    print("Compra cancelada.")
                    return False
                else:
                    print("Opcao invalida. Digite 's' para Sim ou 'n' para Nao.")
            except ValueError:
                print("Entrada invalida. Digite um numero.")

    def mostra_mensagem(self, msg: str):
        print(f"\n{msg}\n")