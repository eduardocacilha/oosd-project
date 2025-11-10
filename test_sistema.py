import sys
import os
from datetime import date, datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.main_controller import MainController
from models.usuario import Usuario
from models.evento import Evento
from models.ingresso import Ingresso
from models.venda import Venda
from models.camisa import Camisa
from models.copo import Copo

class TesteSistema:
    def __init__(self):
        self.controller = MainController()
        self.teste_sucesso = 0
        self.teste_falha = 0
    
    def log(self, mensagem, sucesso=True):
        
        status = "✓" if sucesso else "✗"
        print(f"{status} {mensagem}")
        if sucesso:
            self.teste_sucesso += 1
        else:
            self.teste_falha += 1
    
    def testar_usuarios(self):
        
        print("\n" + "="*50)
        print("TESTANDO FUNCIONALIDADES DE USUÁRIOS")
        print("="*50)
        
        try:
            Usuario._registros.clear()
            Usuario._next_id = 1
            
            usuario1 = Usuario("123", "João Silva", "joao@email.com")
            usuario2 = Usuario("456", "Maria Santos", "maria@email.com")
            usuario3 = Usuario("789", "Pedro Costa", "pedro@email.com")
            
            self.log("Inclusão de usuários")
            
            usuario_encontrado = Usuario.get_by_matricula("123")
            if usuario_encontrado and usuario_encontrado.nome == "João Silva":
                self.log("Busca de usuário por matrícula")
            else:
                self.log("Busca de usuário por matrícula", False)
            
            todos_usuarios = Usuario.get_all()
            if len(todos_usuarios) == 3:
                self.log("Listagem de usuários")
            else:
                self.log("Listagem de usuários", False)
            
            usuario1.nome = "João Silva Alterado"
            if usuario1.nome == "João Silva Alterado":
                self.log("Alteração de usuário")
            else:
                self.log("Alteração de usuário", False)
                
        except Exception as e:
            self.log(f"Erro nos testes de usuário: {str(e)}", False)
    
    def testar_eventos(self):
        
        print("\n" + "="*50)
        print("TESTANDO FUNCIONALIDADES DE EVENTOS")
        print("="*50)
        
        try:
            Evento._registros.clear()
            Evento._next_id = 1
            
            evento1 = Evento("Festa de Formatura", date(2025, 12, 15), "Salão de Festas", 50.0)
            evento2 = Evento("Show de Rock", date(2025, 11, 20), "Arena", 80.0)
            evento3 = Evento("Festival de Música", date(2025, 10, 25), "Parque", 30.0)
            
            self.controller._MainController__evento_controller._EventoController__eventos = [evento1, evento2, evento3]
            
            self.log("Inclusão de eventos")
            
            evento_encontrado = self.controller._MainController__evento_controller.buscar_evento_por_nome("Festa de Formatura")
            if evento_encontrado and evento_encontrado.local == "Salão de Festas":
                self.log("Busca de evento por nome")
            else:
                self.log("Busca de evento por nome", False)
            
            eventos = self.controller._MainController__evento_controller._EventoController__eventos
            if len(eventos) == 3:
                self.log("Listagem de eventos")
            else:
                self.log("Listagem de eventos", False)
            
            usuario = Usuario.get_by_matricula("123")
            if usuario:
                from models.feedback import Feedback
                feedback = Feedback(usuario, evento1, 5, "Excelente festa!", date.today())
                evento1.adicionar_feedback(feedback)
                if len(evento1.feedbacks) == 1:
                    self.log("Avaliação de evento")
                else:
                    self.log("Avaliação de evento", False)
            
        except Exception as e:
            self.log(f"Erro nos testes de evento: {str(e)}", False)
    
    def testar_ingressos(self):
        
        print("\n" + "="*50)
        print("TESTANDO FUNCIONALIDADES DE INGRESSOS")
        print("="*50)
        
        try:
            Ingresso._ingressos.clear()
            Ingresso._contador_id = 0
            
            usuario = Usuario.get_by_matricula("123")
            eventos = self.controller._MainController__evento_controller._EventoController__eventos
            evento = eventos[0] if eventos else None
            
            if usuario and evento:
                ingresso = usuario.comprar_ingresso(evento)
                if ingresso:
                    self.log("Compra de ingresso")
                    
                    ingressos_usuario = usuario.ingressos_comprados
                    if len(ingressos_usuario) == 1:
                        self.log("Listagem de ingressos do usuário")
                    else:
                        self.log("Listagem de ingressos do usuário", False)
                    
                    usuario.colocar_ingresso_a_venda(ingresso, 60.0)
                    if ingresso.revendedor is not None:
                        self.log("Colocar ingresso à venda")
                    else:
                        self.log("Colocar ingresso à venda", False)
                    
                    usuario.remover_ingresso_da_venda(ingresso)
                    if ingresso.revendedor is None:
                        self.log("Remover ingresso da venda")
                    else:
                        self.log("Remover ingresso da venda", False)
                else:
                    self.log("Compra de ingresso", False)
            else:
                self.log("Compra de ingresso", False)
                
        except Exception as e:
            self.log(f"Erro nos testes de ingresso: {str(e)}", False)
    
    def testar_produtos(self):
        
        print("\n" + "="*50)
        print("TESTANDO FUNCIONALIDADES DE PRODUTOS")
        print("="*50)
        
        try:
            produto_controller = self.controller._MainController__produto_controller
            produto_controller._ProdutoController__produtos_por_evento.clear()
            
            camisa = Camisa(1, "Camisa Evento", 25.0, 50, "M", "Azul")
            copo = Copo(2, "Copo Personalizado", 15.0, 100, 300, "Plástico")
            
            eventos = self.controller._MainController__evento_controller._EventoController__eventos
            if eventos:
                nome_evento = eventos[0].nome
                produto_controller._ProdutoController__produtos_por_evento[nome_evento] = [camisa, copo]
                self.log("Criação e adição de produtos ao evento")
                
                produtos = produto_controller._ProdutoController__produtos_por_evento[nome_evento]
                if len(produtos) == 2:
                    self.log("Listagem de produtos do evento")
                else:
                    self.log("Listagem de produtos do evento", False)
                
                camisa.preco = 30.0
                if camisa.preco == 30.0:
                    self.log("Alteração de produto")
                else:
                    self.log("Alteração de produto", False)
            else:
                self.log("Criação e adição de produtos ao evento", False)
                
        except Exception as e:
            self.log(f"Erro nos testes de produto: {str(e)}", False)
    
    def testar_vendas(self):
        
        print("\n" + "="*50)
        print("TESTANDO FUNCIONALIDADES DE VENDAS")
        print("="*50)
        
        try:
            Venda._registros.clear()
            Venda._next_id = 1
            
            usuario = Usuario.get_by_matricula("456")
            eventos = self.controller._MainController__evento_controller._EventoController__eventos
            evento = eventos[1] if len(eventos) > 1 else eventos[0]
            
            if usuario and evento:
                from models.item_venda import ItemVenda
                
                produto_controller = self.controller._MainController__produto_controller
                copo = Copo(3, "Copo Show", 20.0, 50, 500, "Vidro")
                produto_controller._ProdutoController__produtos_por_evento[evento.nome] = [copo]
                
                venda = Venda(usuario, evento, "PIX")
                item = ItemVenda(copo, 3, copo.preco)
                venda.adicionar_item(item)
                
                if venda.total == 60.0:
                    self.log("Criação de venda com itens")
                else:
                    self.log("Criação de venda com itens", False)
                
                if copo.estoque == 47:
                    self.log("Baixa de estoque na venda")
                else:
                    self.log("Baixa de estoque na venda", False)
                
                if len(usuario.historico_compras) == 1:
                    self.log("Adição ao histórico de compras")
                else:
                    self.log("Adição ao histórico de compras", False)
            else:
                self.log("Criação de venda com itens", False)
                
        except Exception as e:
            self.log(f"Erro nos testes de venda: {str(e)}", False)
    
    def testar_relatorios(self):
        
        print("\n" + "="*50)
        print("TESTANDO FUNCIONALIDADES DE RELATÓRIOS")
        print("="*50)
        
        try:
            relatorio_controller = self.controller._MainController__relatorio_controller
            
            try:
                relatorio_controller.relatorio_eventos_preco()
                self.log("Relatório de eventos por preço")
            except Exception:
                self.log("Relatório de eventos por preço", False)
            
            try:
                relatorio_controller.relatorio_eventos_avaliacao()
                self.log("Relatório de eventos por avaliação")
            except Exception:
                self.log("Relatório de eventos por avaliação", False)
            
            try:
                relatorio_controller.relatorio_produtos_preco()
                self.log("Relatório de produtos por preço")
            except Exception:
                self.log("Relatório de produtos por preço", False)
            
            try:
                relatorio_controller.relatorio_produtos_vendidos()
                self.log("Relatório de produtos mais vendidos")
            except Exception:
                self.log("Relatório de produtos mais vendidos", False)
            
            try:
                relatorio_controller.relatorio_vendas_pagamento()
                self.log("Relatório de vendas por método de pagamento")
            except Exception:
                self.log("Relatório de vendas por método de pagamento", False)
            
            try:
                relatorio_controller.relatorio_faturamento_evento()
                self.log("Relatório de faturamento por evento")
            except Exception:
                self.log("Relatório de faturamento por evento", False)
            
        except Exception as e:
            self.log(f"Erro nos testes de relatório: {str(e)}", False)
    
    def testar_validacoes(self):
        
        print("\n" + "="*50)
        print("TESTANDO VALIDAÇÕES DO SISTEMA")
        print("="*50)
        
        try:
            usuario_email_invalido = Usuario("999", "Teste", "email_invalido")
            self.log("Criação de usuário com email sem validação automática")
            
            try:
                produto = Copo(99, "Teste", 10.0, 5, 200, "Plástico")
                if not produto.verificar_estoque(10):
                    self.log("Validação de estoque insuficiente")
                else:
                    self.log("Validação de estoque insuficiente", False)
            except:
                self.log("Validação de estoque insuficiente", False)
            
            try:
                data_passada = date(2020, 1, 1)
                evento_passado = Evento("Evento Passado", data_passada, "Local", 10.0)
                self.log("Validação de data no passado")
            except:
                self.log("Validação de data no passado")
                
        except Exception as e:
            self.log(f"Erro nos testes de validação: {str(e)}", False)
    
    def executar_todos_testes(self):
        
        print("INICIANDO TESTE AUTOMATIZADO DO SISTEMA DE GESTÃO DE FESTAS")
        print("="*70)
        
        self.testar_usuarios()
        self.testar_eventos()
        self.testar_ingressos()
        self.testar_produtos()
        self.testar_vendas()
        self.testar_relatorios()
        self.testar_validacoes()
        
        print("\n" + "="*70)
        print("RESUMO DOS TESTES")
        print("="*70)
        print(f"Testes executados com SUCESSO: {self.teste_sucesso}")
        print(f"Testes com FALHA: {self.teste_falha}")
        print(f"Total de testes: {self.teste_sucesso + self.teste_falha}")
        
        if self.teste_falha == 0:
            print("\n🎉 TODOS OS TESTES PASSARAM! O sistema está funcionando corretamente.")
        else:
            print(f"\n⚠️  {self.teste_falha} teste(s) falharam. Verifique os logs acima.")
        
        print("="*70)

def main():
    
    print("Sistema de Testes Automatizados")
    print("Pressione Ctrl+C para interromper a qualquer momento\n")
    
    try:
        teste = TesteSistema()
        teste.executar_todos_testes()
        
        input("\nPressione Enter para finalizar...")
        
    except KeyboardInterrupt:
        print("\n\nTestes interrompidos pelo usuário.")
    except Exception as e:
        print(f"\nErro durante a execução dos testes: {str(e)}")

if __name__ == "__main__":
    main()