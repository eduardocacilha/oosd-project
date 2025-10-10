class IngressoView:
    
    def tela_opcoes(self):
        print("-------- INGRESSOS ----------")
        print("Escolha a opção:")
        print("1 - Comprar Ingresso")
        print("2 - Listar Meus Ingressos")
        print("3 - Colocar Ingresso à Venda")
        print("4 - Remover Ingresso da Venda")
        print("5 - Comprar Ingresso de Revenda")
        print("6 - Ver Ingressos Disponíveis para Revenda")
        print("0 - Retornar")
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_preco_ingresso(self):
        try:
            preco = float(input("Preço do ingresso (deixe em branco para usar o padrão): "))
            return preco
        except ValueError:
            return None

    def pega_novo_preco_revenda(self):
        preco = float(input("Novo preço para revenda: R$ "))
        return preco

    def mostra_ingresso(self, ingresso):
        print(f"Evento: {ingresso.evento.nome}")
        print(f"Comprador: {ingresso.comprador.nome}")
        print(f"Data da Compra: {ingresso.data_compra}")
        print(f"Preço: R$ {ingresso.preco:.2f}")
        if hasattr(ingresso, 'revendedor') and ingresso.revendedor:
            print(f"Revendedor: {ingresso.revendedor.nome}")
        print("-----------------------------")

    def mostra_ingressos(self, lista_ingressos):
        if len(lista_ingressos) == 0:
            print("Nenhum ingresso encontrado")
        else:
            print("-------- LISTA DE INGRESSOS ----------")
            for i, ingresso in enumerate(lista_ingressos, 1):
                print(f"{i}.")
                self.mostra_ingresso(ingresso)

    def mostra_ingressos_revenda(self, lista_ingressos):
        if len(lista_ingressos) == 0:
            print("Nenhum ingresso disponível para revenda")
        else:
            print("-------- INGRESSOS PARA REVENDA ----------")
            for i, ingresso in enumerate(lista_ingressos, 1):
                print(f"{i}. Evento: {ingresso.evento.nome}")
                print(f"   Revendedor: {ingresso.revendedor.nome}")
                print(f"   Preço: R$ {ingresso.preco:.2f}")
                print("-----------------------------")

    def seleciona_ingresso(self, lista_ingressos):
        if len(lista_ingressos) == 0:
            print("Nenhum ingresso disponível")
            return None
        
        self.mostra_ingressos(lista_ingressos)
        try:
            indice = int(input("Selecione o número do ingresso: ")) - 1
            if 0 <= indice < len(lista_ingressos):
                return lista_ingressos[indice]
            else:
                print("Opção inválida")
                return None
        except ValueError:
            print("Por favor, digite um número válido")
            return None

    def seleciona_ingresso_revenda(self, lista_ingressos):
        if len(lista_ingressos) == 0:
            print("Nenhum ingresso disponível para revenda")
            return None
        
        self.mostra_ingressos_revenda(lista_ingressos)
        try:
            indice = int(input("Selecione o número do ingresso: ")) - 1
            if 0 <= indice < len(lista_ingressos):
                return lista_ingressos[indice]
            else:
                print("Opção inválida")
                return None
        except ValueError:
            print("Por favor, digite um número válido")
            return None

    def mostra_mensagem(self, msg):
        print(msg)