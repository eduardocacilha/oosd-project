class UsuarioView:
    
    def tela_opcoes(self):
        print("-------- USUÁRIOS ----------")
        print("Escolha a opção:")
        print("1 - Incluir Usuário")
        print("2 - Alterar Usuário")
        print("3 - Listar Usuários")
        print("4 - Excluir Usuário")
        print("5 - Comprar Ingresso")
        print("6 - Ver Histórico de Compras")
        print("7 - Avaliar Evento")
        print("8 - Gerenciar Revenda de Ingressos")
        print("0 - Retornar")
        opcao = int(input("Escolha a opção: "))
        return opcao

    def tela_opcoes_revenda(self):
        print("-------- REVENDA DE INGRESSOS ----------")
        print("Escolha a opção:")
        print("1 - Colocar Ingresso à Venda")
        print("2 - Remover Ingresso da Venda")
        print("3 - Comprar Ingresso de Revenda")
        print("4 - Listar Meus Ingressos à Venda")
        print("0 - Retornar")
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_usuario(self):
        print("-------- DADOS USUÁRIO ----------")
        matricula = input("Matrícula: ")
        nome = input("Nome: ")
        email = input("Email: ")
        return {"matricula": matricula, "nome": nome, "email": email}

    def pega_matricula_usuario(self):
        matricula = input("Matrícula do usuário: ")
        return matricula

    def pega_dados_avaliacao(self):
        print("-------- AVALIAR EVENTO ----------")
        nota = int(input("Nota (1-5): "))
        comentario = input("Comentário: ")
        return {"nota": nota, "comentario": comentario}

    def pega_preco_revenda(self):
        preco = float(input("Novo preço para revenda: R$ "))
        return preco

    def mostra_usuario(self, dados_usuario):
        print("MATRÍCULA: ", dados_usuario["matricula"])
        print("NOME: ", dados_usuario["nome"])
        print("EMAIL: ", dados_usuario["email"])
        print()

    def mostra_usuarios(self, lista_usuarios):
        if len(lista_usuarios) == 0:
            print("Nenhum usuário cadastrado")
        else:
            for usuario in lista_usuarios:
                self.mostra_usuario({
                    "matricula": usuario.matricula,
                    "nome": usuario.nome,
                    "email": usuario.email
                })

    def mostra_historico_compras(self, historico):
        if len(historico) == 0:
            print("Nenhuma compra realizada")
        else:
            print("-------- HISTÓRICO DE COMPRAS ----------")
            for i, venda in enumerate(historico, 1):
                print(f"{i}. Venda ID: {venda.id_venda}")
                print(f"   Método: {venda.metodo_pagamento}")
                print(f"   Data: {venda.data_hora}")
                print()

    def mostra_ingressos(self, ingressos):
        if len(ingressos) == 0:
            print("Nenhum ingresso encontrado")
        else:
            print("-------- INGRESSOS ----------")
            for i, ingresso in enumerate(ingressos, 1):
                print(f"{i}. Evento: {ingresso.evento.nome}")
                print(f"   Preço: R$ {ingresso.preco:.2f}")
                print(f"   Data Compra: {ingresso.data_compra}")
                if hasattr(ingresso, 'revendedor') and ingresso.revendedor:
                    print(f"   Status: À venda por {ingresso.revendedor.nome}")
                print()

    def mostra_ingressos_a_venda(self, ingressos_a_venda):
        if len(ingressos_a_venda) == 0:
            print("Nenhum ingresso à venda")
        else:
            print("-------- INGRESSOS À VENDA ----------")
            for i, ingresso in enumerate(ingressos_a_venda, 1):
                print(f"{i}. Evento: {ingresso.evento.nome}")
                print(f"   Preço: R$ {ingresso.preco:.2f}")
                print()

    def seleciona_usuario(self, lista_usuarios):
        if len(lista_usuarios) == 0:
            print("Nenhum usuário cadastrado")
            return None
        
        self.mostra_usuarios(lista_usuarios)
        matricula = input("Digite a matrícula do usuário desejado: ")
        
        for usuario in lista_usuarios:
            if usuario.matricula == matricula:
                return usuario
        #VIEWW NAO RECEBE OBJETO DA ENTIDADE APENAS ALTERAR.
        print("Usuário não encontrado")
        return None

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

    def mostra_mensagem(self, msg):
        print(msg)
    
    def exibir_usuario(self, usuario):
        # Exibe informações de um usuário
        print(f"Usuário: {usuario.nome} - Matrícula: {usuario.matricula} - Email: {usuario.email}")