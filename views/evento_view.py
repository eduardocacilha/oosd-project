from typing import List, Optional
import PySimpleGUI as sg

class EventoView:
    
    def tela_opcoes(self) -> int:
        print("\n-------- MENU EVENTOS ----------")
        print("1 - Incluir Evento")
        print("2 - Alterar Evento")
        print("3 - Listar Eventos")
        print("4 - Excluir Evento")
        print("5 - Ver Detalhes de um Evento")
        print("6 - Ver Feedbacks de um Evento")
        print("0 - Retornar ao Menu Principal")

        while True:
            try:
                opcao = int(input("Escolha a opção: "))
                if 0 <= opcao <= 6:
                    return opcao
                else:
                    print("Opção inválida! Por favor, escolha um número do menu.")
            except ValueError:
                print("Entrada inválida! Por favor, digite um número.")

    def pega_dados_evento(self) -> dict:
        print("\n-------- DADOS DO EVENTO ----------")
        
        while True:
            nome = input("Nome do evento: ").strip()
            if nome:
                break
            print("Nome do evento não pode estar vazio!")
        
        from datetime import datetime
        while True:
            data_str = input("Data do evento (DD/MM/AAAA): ").strip()
            try:
                data_obj = datetime.strptime(data_str, '%d/%m/%Y')
                if data_obj.date() < datetime.now().date():
                    print("A data do evento não pode ser no passado!")
                    continue
                break
            except ValueError:
                print("ERRO: Formato de data inválido. Use DD/MM/AAAA (ex: 25/12/2024).")
        
        while True:
            local = input("Local: ").strip()
            if local:
                break
            print("Local não pode estar vazio!")
        
        while True:
            try:
                preco_entrada = float(input("Preço da entrada: R$ "))
                if preco_entrada >= 0:
                    break
                else:
                    print("Preço não pode ser negativo!")
            except ValueError:
                print("Preço inválido. Use apenas números (ex: 100.50).")
        
        return {
            "nome": nome,
            "data": data_str,
            "local": local,
            "preco_entrada": preco_entrada
        }

    def mostra_evento(self, dados_evento: dict):
        print(f"Nome: {dados_evento['nome']}")
        print(f"Data: {dados_evento['data']}")
        print(f"Local: {dados_evento['local']}")
        print(f"Preço: R$ {dados_evento['preco_entrada']:.2f}")

    def mostra_eventos(self, lista_dados_eventos: List[dict]):
        if not lista_dados_eventos:
            print("\nNenhum evento cadastrado.")
        else:
            print("\n-------- LISTA DE EVENTOS ----------")
            for i, dados in enumerate(lista_dados_eventos, 1):
                print(f"{i}. {dados['nome']} - {dados['data']} - {dados['local']} - R$ {dados['preco_entrada']:.2f}")
            print("------------------------------------")

    def mostra_detalhes_evento(self, dados_detalhados_evento: dict):
        print("\n-------- DETALHES DO EVENTO ----------")
        self.mostra_evento(dados_detalhados_evento)
        
        if dados_detalhados_evento.get('nota_media') is not None:
            nota = dados_detalhados_evento['nota_media']
            avaliacoes = dados_detalhados_evento['total_avaliacoes']
            print(f"Avaliação Média: {nota:.1f}/5.0 ({avaliacoes} avaliações)")
        else:
            print("Avaliação Média: Ainda não há avaliações para este evento.")
        print("------------------------------------")

    def mostra_feedbacks(self, lista_dados_feedbacks: List[dict]):
        if not lista_dados_feedbacks:
            print("\nNenhum feedback encontrado para este evento.")
        else:
            print("\n-------- FEEDBACKS DO EVENTO ----------")
            for i, dados in enumerate(lista_dados_feedbacks, 1):
                print(f"{i}. Usuário: {dados['nome_usuario']}")
                print(f"   Nota: {dados['nota']}/5")
                print(f"   Comentário: {dados['comentario']}")
                print(f"   Data: {dados['data']}")
                print("-----------------------------")

    def seleciona_evento(self, lista_dados_eventos: List[dict]) -> Optional[int]:
        self.mostra_eventos(lista_dados_eventos)
        if not lista_dados_eventos:
            return None
            
        while True:
            try:
                escolha = input("Selecione o NÚMERO do evento (ou 0 para cancelar): ")
                if not escolha: continue
                
                indice = int(escolha) - 1
                if indice == -1:
                    return None
                    
                if 0 <= indice < len(lista_dados_eventos):
                    return indice
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Por favor, digite um número válido.")

    def mostra_mensagem(self, msg: str):
        print(f"\n{msg}\n")