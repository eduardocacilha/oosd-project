class EventoView:
    
    def tela_opcoes(self):
        print("-------- EVENTOS ----------")
        print("Escolha a opção:")
        print("1 - Incluir Evento")
        print("2 - Alterar Evento")
        print("3 - Listar Eventos")
        print("4 - Excluir Evento")
        print("5 - Ver Detalhes do Evento")
        print("6 - Ver Feedbacks do Evento")
        print("0 - Retornar")
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_evento(self):
        print("-------- DADOS EVENTO ----------")
        nome = input("Nome do evento: ")
        data = input("Data do evento (DD/MM/AAAA): ")
        local = input("Local: ")
        preco_entrada = float(input("Preço da entrada: R$ "))
        return {
            "nome": nome,
            "data": data,
            "local": local,
            "preco_entrada": preco_entrada
        }

    def pega_nome_evento(self):
        nome = input("Nome do evento: ")
        return nome

    def mostra_evento(self, evento):
        print(f"Nome: {evento.nome}")
        print(f"Data: {evento.data}")
        print(f"Local: {evento.local}")
        print(f"Preço: R$ {evento.preco_entrada:.2f}")
        print("-----------------------------")

    def mostra_eventos(self, lista_eventos):
        if len(lista_eventos) == 0:
            print("Nenhum evento cadastrado")
        else:
            print("-------- LISTA DE EVENTOS ----------")
            for i, evento in enumerate(lista_eventos, 1):
                print(f"{i}.")
                self.mostra_evento(evento)

    def mostra_detalhes_evento(self, evento):
        print("-------- DETALHES DO EVENTO ----------")
        self.mostra_evento(evento)
        
        if hasattr(evento, 'feedbacks') and len(evento.feedbacks) > 0:
            nota_media = sum([fb.nota for fb in evento.feedbacks]) / len(evento.feedbacks)
            print(f"Avaliação Média: {nota_media:.1f}/5.0 ({len(evento.feedbacks)} avaliações)")

    def mostra_feedbacks(self, lista_feedbacks):
        if len(lista_feedbacks) == 0:
            print("Nenhum feedback encontrado para este evento")
        else:
            print("-------- FEEDBACKS DO EVENTO ----------")
            for i, feedback in enumerate(lista_feedbacks, 1):
                print(f"{i}. Usuário: {feedback.usuario.nome}")
                print(f"   Nota: {feedback.nota}/5")
                print(f"   Comentário: {feedback.comentario}")
                print(f"   Data: {feedback.data}")
                print("-----------------------------")

    def seleciona_evento(self, lista_eventos):
        if len(lista_eventos) == 0:
            print("Nenhum evento cadastrado")
            return None
        
        self.mostra_eventos(lista_eventos)
        nome = input("Digite o nome do evento desejado: ")
        
        for evento in lista_eventos:
            if evento.nome.lower() == nome.lower():
                return evento
        
        print("Evento não encontrado")
        return None

    def seleciona_evento_por_numero(self, lista_eventos):
        if len(lista_eventos) == 0:
            print("Nenhum evento cadastrado")
            return None
        
        self.mostra_eventos(lista_eventos)
        try:
            indice = int(input("Selecione o número do evento: ")) - 1
            if 0 <= indice < len(lista_eventos):
                return lista_eventos[indice]
            else:
                print("Opção inválida")
                return None
        except ValueError:
            print("Por favor, digite um número válido")
            return None

    def exibir_evento(self, evento):
        print(f"Evento: {evento.nome} - Data: {evento.data} - Local: {evento.local} - Preço: {evento.preco}")

    def mostra_mensagem(self, msg):
        print(msg)