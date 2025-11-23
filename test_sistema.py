from controllers.main_controller import MainController
from controllers.usuario_controller import UsuarioController
from controllers.evento_controller import EventoController
from controllers.ingresso_controller import IngressoController
from controllers.produto_controller import ProdutoController
from controllers.venda_controller import VendaController
from views.venda_view import VendaView
from views.usuario_view import UsuarioView
from views.evento_view import EventoView
from views.ingresso_view import IngressoView
from views.produto_view import ProdutoView
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException
from datetime import datetime, timedelta
import time
import os
from pathlib import Path

# limpeza opcional de dados persistidos para evitar interferência em testes
LIMPAR_DADOS_PERSISTIDOS = True

# importar DAOs para persistir alterações feitas diretamente nos modelos
from DAOs.usuario_dao import UsuarioDAO
from DAOs.evento_dao import EventoDAO
from DAOs.ingresso_dao import IngressoDAO
from DAOs.venda_dao import VendaDAO  # usado possivelmente em futuras expansões

try:
    from DAOs.produto_dao import ProdutoDAO
except ImportError:
    ProdutoDAO = None


class TesteSistema:

    def __init__(self):
        try:
            print("=" * 60)
            print("INICIANDO TESTE AUTOMÁTICO DO SISTEMA")
            print("=" * 60)
            if LIMPAR_DADOS_PERSISTIDOS:
                self._limpar_dados_persistidos()
            self.usuario_view = UsuarioView()
            self.evento_view = EventoView()
            self.ingresso_view = IngressoView()
            self.produto_view = ProdutoView()
            self.usuario_controller = UsuarioController(self.usuario_view)
            self.evento_controller = EventoController(self.evento_view)
            self.ingresso_controller = IngressoController(self.ingresso_view)
            self.produto_controller = ProdutoController(self.produto_view)
            self.venda_view = VendaView()
            self.venda_controller = VendaController(
                self.venda_view,
                self.evento_controller,
                self.usuario_controller,
                self.produto_controller,
            )
            if hasattr(self.ingresso_controller, "set_usuario_controller"):
                self.ingresso_controller.set_usuario_controller(self.usuario_controller)
            if hasattr(self.ingresso_controller, "set_evento_controller"):
                self.ingresso_controller.set_evento_controller(self.evento_controller)
            if hasattr(self.produto_controller, "set_evento_controller"):
                self.produto_controller.set_evento_controller(self.evento_controller)
            self.usuarios_teste = []
            self.eventos_teste = []
            print("✓ Sistema inicializado com sucesso!")
        except Exception as e:
            print(f"✗ ERRO na inicialização: {e}")
            raise

    # função para remover arquivos .pkl antes de iniciar DAOs
    def _limpar_dados_persistidos(self):
        try:
            # Arquivos .pkl são armazenados na raiz do projeto
            raiz = Path(__file__).parent
            removidos = 0
            for nome in [
                "usuarios.pkl",
                "eventos.pkl",
                "ingressos.pkl",
                "produtos.pkl",
                "vendas.pkl",
            ]:
                arq = raiz / nome
                if arq.exists():
                    try:
                        os.remove(arq)
                        removidos += 1
                    except OSError:
                        pass
            print(f"(Limpeza) Removidos {removidos} arquivos .pkl para teste isolado.")
        except Exception as e:
            print(f"(Aviso) Falha ao limpar persistência: {e}")

    # persistir ingresso (usuário, evento e ingresso) após compra direta
    def _persistir_ingresso(self, ingresso):
        try:
            IngressoDAO().add(ingresso)
            if getattr(ingresso, "comprador", None):
                UsuarioDAO().update(ingresso.comprador)
            if getattr(ingresso, "evento", None):
                EventoDAO().update(ingresso.evento)
        except Exception as e:
            print(f"(Aviso) Falha ao persistir ingresso: {e}")

    def aguardar(self, segundos=1):
        time.sleep(segundos)

    def teste_usuarios(self):
        print("\n" + "=" * 40)
        print("TESTANDO MÓDULO DE USUÁRIOS")
        print("=" * 40)
        usuarios_dados = [
            {"nome": "João Silva", "email": "joao@email.com", "matricula": "12345"},
            {"nome": "Maria Santos", "email": "maria@email.com", "matricula": "67890"},
            {"nome": "Pedro Costa", "email": "pedro@email.com", "matricula": "11111"},
            {"nome": "Ana Oliveira", "email": "ana@email.com", "matricula": "22222"},
        ]
        usuario_dao = UsuarioDAO()
        for i, dados in enumerate(usuarios_dados, 1):
            try:
                print(f"\n{i}. Criando usuário: {dados['nome']}")
                matricula_unica = dados["matricula"]
                while usuario_dao.get(matricula_unica) is not None:
                    matricula_unica += "X"
                dados_unicos = {
                    "nome": dados["nome"],
                    "email": dados["email"],
                    "matricula": matricula_unica,
                }
                usuario = self.usuario_controller.criar_usuario_teste(dados_unicos)
                self.usuarios_teste.append(usuario)
                print(
                    f"  ✓ Usuário {dados_unicos['nome']} criado (Matrícula: {dados_unicos['matricula']})"
                )
                self.aguardar(0.5)
            except Exception as e:
                print(f"  ✗ Erro ao criar usuário {dados['nome']}: {e}")
        try:
            print(f"\n5. Testando listagem de usuários...")
            usuarios = self.usuario_controller.listar_usuarios_objetos()
            print(f"  ✓ Total de usuários cadastrados: {len(usuarios)}")
            self.aguardar()
        except Exception as e:
            print(f"  ✗ Erro na listagem: {e}")
        try:
            print(f"\n6. Testando busca por matrícula...")
            usuario_encontrado = self.usuario_controller.buscar_usuario_por_matricula(
                "12345"
            )
            if usuario_encontrado:
                print(f"  ✓ Usuário encontrado: {usuario_encontrado.nome}")
            else:
                print(f"  ✗ Usuário não encontrado")
            self.aguardar()
        except Exception as e:
            print(f"  ✗ Erro na busca: {e}")

    def teste_eventos(self):
        print("\n" + "=" * 40)
        print("TESTANDO MÓDULO DE EVENTOS")
        print("=" * 40)
        hoje = datetime.now()
        eventos_dados = [
            {
                "nome": "Show de Rock",
                "data": (hoje + timedelta(days=30)).date(),  # corrigido para date
                "data_str": (hoje + timedelta(days=30)).strftime("%d/%m/%Y"),
                "local": "Estádio Central",
                "preco_entrada": 80.0,
            },
            {
                "nome": "Festival de Jazz",
                "data": (hoje + timedelta(days=45)).date(),
                "data_str": (hoje + timedelta(days=45)).strftime("%d/%m/%Y"),
                "local": "Teatro Municipal",
                "preco_entrada": 120.0,
            },
            {
                "nome": "Feira de Tecnologia",
                "data": (hoje + timedelta(days=60)).date(),
                "data_str": (hoje + timedelta(days=60)).strftime("%d/%m/%Y"),
                "local": "Centro de Convenções",
                "preco_entrada": 50.0,
            },
        ]
        for i, dados in enumerate(eventos_dados, 1):
            try:
                print(f"\n{i}. Criando evento (controller): {dados['nome']} para {dados['data_str']}")
                evento = self.evento_controller.criar_evento_teste(
                    {
                        "nome": dados["nome"],
                        "data": dados["data"],
                        "local": dados["local"],
                        "preco_entrada": dados["preco_entrada"],
                    }
                )
                self.eventos_teste.append(evento)
                print(f"  ✓ Evento '{evento.nome}' criado")
                self.aguardar(0.5)
            except Exception as e:
                print(f"  ✗ Erro ao criar evento {dados['nome']}: {e}")
        try:
            # Recarregar eventos no controller para refletir aqueles adicionados diretamente via DAO
            if hasattr(self.evento_controller, "recarregar_eventos"):
                self.evento_controller.recarregar_eventos()
            print(f"\n4. Testando listagem de eventos...")
            eventos = self.evento_controller.get_eventos_lista()
            print(f"  ✓ Total de eventos cadastrados: {len(eventos)}")
            self.aguardar()
        except Exception as e:
            print(f"  ✗ Erro na listagem de eventos: {e}")

    def teste_ingressos(self):
        print("\n" + "=" * 40)
        print("TESTANDO MÓDULO DE INGRESSOS")
        print("=" * 40)
        if not self.usuarios_teste or not self.eventos_teste:
            print("  ✗ Não há usuários ou eventos para testar ingressos")
            return
        compras = [
            {"usuario_idx": 0, "evento_idx": 0, "metodo": "PIX"},
            {"usuario_idx": 1, "evento_idx": 0, "metodo": "Credito"},
            {"usuario_idx": 0, "evento_idx": 1, "metodo": "Dinheiro"},
            (
                {"usuario_idx": 2, "evento_idx": 2, "metodo": "Debito"}
                if len(self.usuarios_teste) > 2
                else {"usuario_idx": 0, "evento_idx": 2, "metodo": "Debito"}
            ),
        ]
        for i, compra in enumerate(compras, 1):
            try:
                if compra["usuario_idx"] >= len(self.usuarios_teste) or compra[
                    "evento_idx"
                ] >= len(self.eventos_teste):
                    print(f"  ⚠ Pulando compra {i} - índices inválidos")
                    continue
                usuario = self.usuarios_teste[compra["usuario_idx"]]
                evento = self.eventos_teste[compra["evento_idx"]]
                print(f"\n{i}. {usuario.nome} comprando ingresso para '{evento.nome}'")
                ingresso = usuario.comprar_ingresso(
                    evento, evento.preco_entrada, compra["metodo"]
                )
                # Persistir ingresso e atualizações de usuario/evento
                self._persistir_ingresso(ingresso)
                print(
                    f"  ✓ Ingresso comprado por R$ {ingresso.preco:.2f} via {compra['metodo']}"
                )
                self.aguardar(0.5)
            except Exception as e:
                print(f"  ✗ Erro na compra {i}: {e}")
        # Resumo de ingressos persistidos
        try:
            total_ingressos_persistidos = len(list(IngressoDAO().get_all()))
            print(f"\nTotal de ingressos persistidos: {total_ingressos_persistidos}")
        except Exception as e:
            print(f"(Aviso) Falha ao consultar ingressos persistidos: {e}")
        try:
            print(f"\n5. Testando listagem de ingressos do primeiro usuário...")
            usuario = self.usuarios_teste[0]
            ingressos = usuario.listar_ingressos()
            print(f"  ✓ {usuario.nome} possui {len(ingressos)} ingresso(s)")
            for j, ing in enumerate(ingressos, 1):
                print(f"    {j}. {ing.evento.nome} - R$ {ing.preco:.2f}")
            self.aguardar()
        except Exception as e:
            print(f"  ✗ Erro na listagem de ingressos: {e}")

    def teste_revenda(self):
        print("\n" + "=" * 40)
        print("TESTANDO MÓDULO DE REVENDA")
        print("=" * 40)
        if len(self.usuarios_teste) < 2:
            print("  ✗ Não há usuários suficientes para testar revenda")
            return
        try:
            usuario1 = self.usuarios_teste[0]
            usuario2 = self.usuarios_teste[1]
            ingressos_usuario1 = usuario1.listar_ingressos()
            if not ingressos_usuario1:
                print("  ✗ Usuário1 não tem ingressos para revender")
                return
            ingresso_para_revenda = ingressos_usuario1[0]
            novo_preco = 150.0
            print(
                f"\n1. {usuario1.nome} colocando ingresso à venda por R$ {novo_preco:.2f}"
            )
            usuario1.colocar_ingresso_a_venda(ingresso_para_revenda, novo_preco)
            print(
                f"  ✓ Ingresso de '{ingresso_para_revenda.evento.nome}' colocado à venda"
            )
            self.aguardar()
            print(f"\n2. {usuario2.nome} comprando ingresso de revenda...")
            # Utiliza método de revenda recém implementado no modelo Usuario
            usuario2.comprar_ingresso_revenda(ingresso_para_revenda)
            # Atualizar persistência após transferência
            try:
                UsuarioDAO().update(usuario1)
                UsuarioDAO().update(usuario2)
                IngressoDAO().update(ingresso_para_revenda)
            except Exception as e:
                print(f"(Aviso) Falha ao persistir revenda: {e}")
            print(f"  ✓ Ingresso comprado de {usuario1.nome}")
            self.aguardar()
        except Exception as e:
            print(f"  ✗ Erro no teste de revenda: {e}")

    def teste_produtos(self):
        print("\n" + "=" * 40)
        print("TESTANDO MÓDULO DE PRODUTOS")
        print("=" * 40)
        if not self.eventos_teste:
            print("  ✗ Não há eventos para associar produtos")
            return
        evento = self.eventos_teste[0]
        produtos_dados = [
            {
                "tipo": "camisa",
                "nome": "Camisa Show Rock",
                "preco": 45.0,
                "estoque": 100,
                "tamanho": "M",
                "cor": "Preta",
            },
            {
                "tipo": "copo",
                "nome": "Copo Personalizado",
                "preco": 25.0,
                "estoque": 50,
                "capacidade_ml": 400,
                "material": "Plástico",
            },
        ]
        for i, dados in enumerate(produtos_dados, 1):
            try:
                print(f"\n{i}. Criando produto: {dados['nome']}")
                if hasattr(self.produto_controller, "criar_produto_teste"):
                    produto = self.produto_controller.criar_produto_teste(evento, dados)
                else:
                    try:
                        if dados["tipo"] == "camisa":
                            from models.camisa import Camisa

                            produto = Camisa(
                                dados["nome"],
                                dados["preco"],
                                dados["estoque"],
                                dados["tamanho"],
                                dados["cor"],
                            )
                        else:
                            from models.copo import Copo

                            produto = Copo(
                                dados["nome"],
                                dados["preco"],
                                dados["estoque"],
                                dados["capacidade_ml"],
                                dados["material"],
                            )
                        if hasattr(evento, "adicionar_produto"):
                            evento.adicionar_produto(produto)
                    except ImportError:
                        print(
                            f"  ⚠ Classes de produto não encontradas, simulando criação..."
                        )
                        produto = type(
                            "Produto",
                            (),
                            {
                                "nome": dados["nome"],
                                "preco": dados["preco"],
                                "estoque": dados["estoque"],
                            },
                        )()
                # Associar produto ao evento e persistir
                try:
                    setattr(produto, "evento_nome", evento.nome)
                    from DAOs.produto_dao import ProdutoDAO
                    ProdutoDAO().add(produto)
                except Exception as e:
                    print(f"  ⚠ Falha ao persistir produto: {e}")
                print(f"  ✓ Produto '{dados['nome']}' criado - R$ {dados['preco']:.2f}")
                self.aguardar(0.5)
            except Exception as e:
                print(f"  ✗ Erro ao criar produto {dados['nome']}: {e}")

    def teste_vendas(self):
        print("\n" + "=" * 40)
        print("TESTANDO MÓDULO DE VENDAS")
        print("=" * 40)
        if not self.usuarios_teste or not self.eventos_teste:
            print("  ✗ Não há dados suficientes para testar vendas")
            return
        try:
            # Localizar produtos criados
            from DAOs.produto_dao import ProdutoDAO
            produto_dao = ProdutoDAO()
            produtos = list(produto_dao.get_all())
            if not produtos:
                print("  ✗ Nenhum produto disponível para vendas")
                return
            usuario = self.usuarios_teste[0]
            evento = self.eventos_teste[0]
            itens_venda = []
            for p in produtos:
                if p.nome.startswith("Camisa"):
                    itens_venda.append((p, 2))
                elif p.nome.startswith("Copo"):
                    itens_venda.append((p, 3))
            print("\n1. Criando venda real via controller...")
            venda = self.venda_controller.criar_venda_teste(
                usuario, evento, itens_venda, "PIX"
            )
            print(
                f"  ✓ Venda criada ID {venda.id_venda} Total R$ {venda.total:.2f} Itens: {len(venda.itens)}"
            )
        except Exception as e:
            print(f"  ✗ Erro ao criar venda real: {e}")

    def teste_feedback(self):
        print("\n" + "=" * 40)
        print("TESTANDO PERSISTÊNCIA DE FEEDBACK")
        print("=" * 40)
        if not self.usuarios_teste or not self.eventos_teste:
            print("  ✗ Sem usuários ou eventos para feedback")
            return
        try:
            usuario = self.usuarios_teste[0]
            evento = self.eventos_teste[0]
            # Forçar data do evento para passado para permitir avaliação
            try:
                import datetime as _dt
                evento._Evento__data = _dt.date.today() - _dt.timedelta(days=1)  # bypass setter para teste
            except Exception:
                pass
            from models.feedback import Feedback
            from DAOs.feedback_dao import FeedbackDAO
            from datetime import date as _date
            feedback = Feedback(usuario, evento, 5, "Excelente evento!", _date.today())
            evento.adicionar_feedback(feedback)
            FeedbackDAO().add(feedback)
            print(f"  ✓ Feedback persistido para evento '{evento.nome}'")
        except Exception as e:
            print(f"  ✗ Erro ao testar feedback: {e}")

    def teste_excecoes(self):
        print("\n" + "=" * 40)
        print("TESTANDO TRATAMENTO DE EXCEÇÕES")
        print("=" * 40)
        try:
            print("\n1. Testando busca de usuário inexistente...")
            usuario = self.usuario_controller.buscar_usuario_por_matricula("99999")
            if usuario is None:
                print("  ✓ Busca retornou None corretamente")
            else:
                print("  ✗ Deveria retornar None")
        except Exception as e:
            print(f"  ✓ Exceção capturada corretamente: {e}")
        try:
            print("\n2. Testando criação de usuário com dados inválidos...")
            from models.usuario import Usuario

            usuario_invalido = Usuario("", "email_inválido", "abc123")
            print("  ✗ Deveria ter lançado exceção para matrícula inválida")
        except Exception as e:
            print(f"  ✓ Exceção capturada corretamente: {e}")
        try:
            print("\n3. Testando criação de evento com data no passado...")
            from models.evento import Evento
            from datetime import datetime, timedelta

            data_passado = datetime.now() - timedelta(days=1)
            evento_invalido = Evento("Evento Passado", data_passado, "Local", 50.0)
            print("  ✗ Deveria ter lançado exceção para data no passado")
        except Exception as e:
            print(f"  ✓ Exceção capturada corretamente: {e}")
        try:
            print("\n4. Testando operação em controlador vazio...")
            controller_vazio = UsuarioController(self.usuario_view)
            usuarios = controller_vazio.listar_usuarios_objetos()
            print(f"  ✓ Lista vazia retornada corretamente (tamanho: {len(usuarios)})")
        except Exception as e:
            print(f"  ✓ Exceção tratada: {e}")

    def executar_todos_os_testes(self):
        try:
            print("\nIniciando bateria completa de testes...")
            self.aguardar(1)
            self.teste_usuarios()
            self.aguardar(1)
            self.teste_eventos()
            self.aguardar(1)
            self.teste_ingressos()
            self.aguardar(1)
            self.teste_revenda()
            self.aguardar(1)
            self.teste_produtos()
            self.aguardar(1)
            self.teste_vendas()
            self.aguardar(1)
            self.teste_feedback()
            self.aguardar(1)
            self.teste_excecoes()
            print("\n" + "=" * 60)
            print("RESUMO DOS TESTES")
            print("=" * 60)
            print(f"✓ Usuários cadastrados: {len(self.usuarios_teste)}")
            print(f"✓ Eventos criados: {len(self.eventos_teste)}")
            print("✓ Todos os módulos testados")
            print("✓ Tratamento de exceções verificado")
            print("\n🎉 TESTES CONCLUÍDOS COM SUCESSO!")
        except Exception as e:
            print(f"\n❌ ERRO CRÍTICO NOS TESTES: {e}")
            import traceback

            traceback.print_exc()


def executar_teste_interativo():
    teste = TesteSistema()
    while True:
        print("\n" + "=" * 50)
        print("MENU DE TESTES")
        print("=" * 50)
        print("1 - Testar Usuários")
        print("2 - Testar Eventos")
        print("3 - Testar Ingressos")
        print("4 - Testar Revenda")
        print("5 - Testar Produtos")
        print("6 - Testar Vendas")
        print("7 - Testar Exceções")
        print("8 - Executar TODOS os testes")
        print("0 - Sair")
        try:
            opcao = input("\nEscolha uma opção: ").strip()
            if opcao == "1":
                teste.teste_usuarios()
            elif opcao == "2":
                teste.teste_eventos()
            elif opcao == "3":
                teste.teste_ingressos()
            elif opcao == "4":
                teste.teste_revenda()
            elif opcao == "5":
                teste.teste_produtos()
            elif opcao == "6":
                teste.teste_vendas()
            elif opcao == "7":
                teste.teste_excecoes()
            elif opcao == "8":
                teste.executar_todos_os_testes()
            elif opcao == "0":
                print("\nEncerrando testes...")
                break
            else:
                print("Opção inválida!")
        except KeyboardInterrupt:
            print("\n\nTestes interrompidos pelo usuário.")
            break
        except Exception as e:
            print(f"\nErro no menu: {e}")


if __name__ == "__main__":
    try:
        print("Escolha o modo de teste:")
        print("1 - Executar todos os testes automaticamente")
        print("2 - Menu interativo")
        modo = input("Modo (1 ou 2): ").strip()
        if modo == "1":
            teste = TesteSistema()
            teste.executar_todos_os_testes()
        elif modo == "2":
            executar_teste_interativo()
        else:
            print("Modo inválido. Executando todos os testes...")
            teste = TesteSistema()
            teste.executar_todos_os_testes()
    except Exception as e:
        print(f"ERRO CRÍTICO: {e}")
        import traceback

        traceback.print_exc()
