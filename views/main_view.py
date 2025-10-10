class MainView:
    
    def tela_opcoes(self):
        print("============================================")
        print("       SISTEMA DE GESTÃO DE FESTAS")
        print("============================================")
        print("Escolha a opção:")
        print("1 - Gerenciar Usuários")
        print("2 - Gerenciar Eventos")
        print("3 - Gerenciar Ingressos")
        print("0 - Finalizar sistema")
        opcao = int(input("Escolha a opção: "))
        return opcao

    def mostra_mensagem(self, msg):
        print(msg)

    def mostra_mensagem_inicial(self):
        print("============================================")
        print("    BEM-VINDO AO SISTEMA DE FESTAS!")
        print("============================================")

    def mostra_mensagem_encerramento(self):
        print("============================================")
        print("         SISTEMA ENCERRADO!")
        print("    Obrigado por usar nosso sistema!")
        print("============================================")
    
    def mostrar(self):
       # Método principal para mostrar o sistema
        self.mostra_mensagem_inicial()
        opcao = self.tela_opcoes()
        return opcao