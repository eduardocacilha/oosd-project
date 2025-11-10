import PySimpleGUI as sg

class MainView:
    def __init__(self):
        sg.theme('Reddit')
    
    def janela_principal(self):

        layout = [
            [sg.Text("============================================", font=("Helvetica", 12))],
            [sg.Text("       SISTEMA DE GESTÃO DE FESTAS", font=("Helvetica", 16, "bold"))],
            [sg.Text("============================================", font=("Helvetica", 12))],
            [sg.Text("Escolha a opção:", font=("Helvetica", 10))],

            # Cada botão tem uma 'key' única para o Controller identificar

           [sg.Button('Gerenciar Usuários', key='1', size=(30,1))],
            [sg.Button('Gerenciar Eventos', key='2', size=(30,1))],
            [sg.Button('Gerenciar Ingressos', key='3', size=(30,1))],
            [sg.Button('Gerenciar Produtos', key='4', size=(30,1))],
            [sg.Button('Relatórios', key='5', size=(30,1))],
            [sg.Button('Finalizar Sistema', key='0', size=(30,1), button_color=('white', 'darkred'))]
        ]

        return sg.Window('Sistema de Festas', layout, finalize=True)

    def mostrar_mensagem_encerramento(self):
        sg.Popup('Sistema Encerrado', 'Obrigado por usar nosso sistema!', keep_on_top=True)
    
    # O substituto do seu "mosta_mensagem"
    def mostrar_mensagem(self, titulo, mensagem):
        sg.Popup(titulo, mensagem, keep_on_top=True)