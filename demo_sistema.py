import sys
import os
from datetime import date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.main_controller import MainController
from models.usuario import Usuario
from models.evento import Evento
from models.camisa import Camisa
from models.copo import Copo

def criar_dados_exemplo():
    
    print("Criando dados de exemplo...")
    
    Usuario._registros.clear()
    Usuario._next_id = 1
    Evento._registros.clear()
    Evento._next_id = 1
    
    usuarios = [
        Usuario("001", "João Silva", "joao@email.com"),
        Usuario("002", "Maria Santos", "maria@email.com"),
        Usuario("003", "Pedro Costa", "pedro@email.com"),
        Usuario("004", "Ana Oliveira", "ana@email.com"),
        Usuario("005", "Carlos Ferreira", "carlos@email.com")
    ]
    
    eventos = [
        Evento("Festa de Formatura UFSC", date(2025, 12, 15), "Centro de Eventos UFSC", 45.0),
        Evento("Show de Rock Nacional", date(2025, 11, 20), "Arena Joinville", 80.0),
        Evento("Festival de Música Eletrônica", date(2025, 10, 25), "Parque da Cidade", 35.0),
        Evento("Baile de Máscaras", date(2025, 12, 31), "Salão Nobre", 60.0),
        Evento("Concert Sinfônico", date(2025, 11, 10), "Teatro Municipal", 25.0)
    ]
    
    return usuarios, eventos

def popular_sistema_com_dados(controller, usuarios, eventos):
    
    controller._MainController__evento_controller._EventoController__eventos = eventos
    
    produto_controller = controller._MainController__produto_controller
    
    produto_controller._ProdutoController__produtos_por_evento["Festa de Formatura UFSC"] = [
        Camisa(1, "Camisa Formatura UFSC", 35.0, 50, "M", "Azul"),
        Camisa(2, "Camisa Formatura UFSC", 35.0, 30, "G", "Azul"),
        Copo(3, "Caneca Formatura", 20.0, 40, 300, "Cerâmica")
    ]
    
    produto_controller._ProdutoController__produtos_por_evento["Show de Rock Nacional"] = [
        Camisa(4, "Camisa Show Rock", 45.0, 80, "M", "Preta"),
        Camisa(5, "Camisa Show Rock", 45.0, 60, "G", "Preta"),
        Copo(6, "Copo Rock'n Roll", 25.0, 100, 500, "Plástico")
    ]
    
    produto_controller._ProdutoController__produtos_por_evento["Festival de Música Eletrônica"] = [
        Camisa(7, "Camisa Festival EDM", 40.0, 70, "M", "Neon"),
        Copo(8, "Copo LED Festival", 30.0, 90, 400, "Plástico")
    ]
    
    try:
        usuarios[0].comprar_ingresso(eventos[0])
        usuarios[1].comprar_ingresso(eventos[1])
        usuarios[2].comprar_ingresso(eventos[0])
        usuarios[0].comprar_ingresso(eventos[2])
        
        eventos[0].adicionar_feedback(usuarios[0], 5, "Evento excelente!")
        eventos[1].adicionar_feedback(usuarios[1], 4, "Show muito bom!")
        eventos[0].adicionar_feedback(usuarios[2], 5, "Perfeito!")
        
    except Exception as e:
        print(f"Erro ao criar compras de exemplo: {e}")
    
    print("✓ Dados de exemplo criados com sucesso!")
    print(f"✓ {len(usuarios)} usuários cadastrados")
    print(f"✓ {len(eventos)} eventos cadastrados")
    print(f"✓ Produtos adicionados aos eventos")
    print(f"✓ Ingressos e avaliações de exemplo criados")

def mostrar_menu_demo():
    
    print("\n" + "="*50)
    print("DEMONSTRAÇÃO DO SISTEMA DE GESTÃO DE FESTAS")
    print("="*50)
    print("1 - Iniciar sistema normalmente")
    print("2 - Mostrar dados de exemplo criados")
    print("3 - Executar teste rápido de relatórios")
    print("0 - Sair")
    print("="*50)

def mostrar_dados_exemplo(controller):
    
    print("\n" + "="*40)
    print("DADOS DE EXEMPLO CRIADOS")
    print("="*40)
    
    print("\nUSUÁRIOS:")
    for usuario in Usuario.get_all():
        print(f"  • {usuario.nome} (Mat: {usuario.matricula}) - {usuario.email}")
    
    print("\nEVENTOS:")
    eventos = controller._MainController__evento_controller._EventoController__eventos
    for evento in eventos:
        print(f"  • {evento.nome}")
        print(f"    Data: {evento.data.strftime('%d/%m/%Y')} | Local: {evento.local}")
        print(f"    Preço: R$ {evento.preco_entrada:.2f}")
        if evento.feedbacks:
            media = sum(f.nota for f in evento.feedbacks) / len(evento.feedbacks)
            print(f"    Avaliação: {media:.1f}/5.0 ({len(evento.feedbacks)} avaliações)")
        print()
    
    print("PRODUTOS POR EVENTO:")
    produto_controller = controller._MainController__produto_controller
    for nome_evento, produtos in produto_controller._ProdutoController__produtos_por_evento.items():
        print(f"  {nome_evento}:")
        for produto in produtos:
            print(f"    • {produto.descricao()} - R$ {produto.preco:.2f} (Estoque: {produto.estoque})")
        print()

def executar_teste_relatorios(controller):
    
    print("\n" + "="*40)
    print("TESTE RÁPIDO DE RELATÓRIOS")
    print("="*40)
    
    relatorio_controller = controller._MainController__relatorio_controller
    
    try:
        print("\n1. Relatório de Eventos por Preço:")
        relatorio_controller.relatorio_eventos_preco()
        
        input("\nPressione Enter para continuar...")
        
        print("\n2. Relatório de Eventos por Avaliação:")
        relatorio_controller.relatorio_eventos_avaliacao()
        
        input("\nPressione Enter para continuar...")
        
        print("\n3. Relatório de Produtos por Preço:")
        relatorio_controller.relatorio_produtos_preco()
        
        print("\n✓ Testes de relatório concluídos!")
        
    except Exception as e:
        print(f"Erro durante teste de relatórios: {e}")

def main():
    
    print("DEMONSTRAÇÃO - SISTEMA DE GESTÃO DE FESTAS")
    print("="*50)
    
    try:
        controller = MainController()
        usuarios, eventos = criar_dados_exemplo()
        popular_sistema_com_dados(controller, usuarios, eventos)
        
        while True:
            mostrar_menu_demo()
            
            try:
                opcao = int(input("\nEscolha uma opção: "))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue
            
            if opcao == 1:
                print("\nIniciando o sistema...")
                controller.iniciar()
                break
                
            elif opcao == 2:
                mostrar_dados_exemplo(controller)
                input("\nPressione Enter para continuar...")
                
            elif opcao == 3:
                executar_teste_relatorios(controller)
                input("\nPressione Enter para continuar...")
                
            elif opcao == 0:
                print("Saindo da demonstração...")
                break
                
            else:
                print("Opção inválida!")
    
    except KeyboardInterrupt:
        print("\n\nDemonstração interrompida pelo usuário.")
    except Exception as e:
        print(f"\nErro durante a demonstração: {str(e)}")

if __name__ == "__main__":
    main()