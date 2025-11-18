from views.usuario_view import UsuarioView
from models.usuario import Usuario
from models.ingresso import Ingresso
from models.venda import Venda
from datetime import date
from typing import List, TYPE_CHECKING, Optional
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

if TYPE_CHECKING:
    from controllers.evento_controller import EventoController

class UsuarioController:

    def __init__(self, usuario_view: UsuarioView):
        self.__view = usuario_view

    def rodar_menu_usuario(self):
        while True:
            opcao = self.__view.criar_janela_menu_usuario()

            if opcao == '0':
                break
            elif opcao == '1':
                self.incluir_usuario()
            elif opcao == '2':
                self.listar_usuarios()
            elif opcao == '3':
                self.alterar_usuario()
            elif opcao == '4':
                self.excluir_usuario()
            elif opcao == '5':
                self.ver_historico_compras()
            elif opcao == '6':
                self.listar_ingressos_usuario()
            elif opcao == '7':
                self.avaliar_evento()

    def incluir_usuario(self):
        try:
            dados_usuario = self.__view.pega_dados_usuario(pedindo_matricula=True)

            if dados_usuario is None:
                return

            if Usuario.get_by_matricula(dados_usuario["matricula"]):
                raise RegraDeNegocioException(f"Usuário com matrícula {dados_usuario['matricula']} já cadastrado!")

            novo_usuario = Usuario(
                dados_usuario["matricula"],
                dados_usuario["nome"],
                dados_usuario["email"]
            )
            Usuario.add(novo_usuario)
            self.__view.mostrar_popup("✓ Sucesso", f"Usuário {novo_usuario.nome} incluído com sucesso!")

        except RegraDeNegocioException as e:
            self.__view.mostrar_popup("✗ Erro de Negócio", str(e))
        except ValueError as e:
            self.__view.mostrar_popup("✗ Erro de Validação", str(e))
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro Inesperado", f"Erro ao incluir usuário: {str(e)}")

    def alterar_usuario(self):
        try:
            matricula = self.__view.pega_matricula_usuario()

            if matricula is None:
                return

            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException(f"Usuário com matrícula {matricula} não encontrado!")

            dados_usuario = self.__view.pega_dados_usuario(pedindo_matricula=False)

            if dados_usuario is None:
                return

            usuario.nome = dados_usuario["nome"]
            usuario.email = dados_usuario["email"]

            self.__view.mostrar_popup("✓ Sucesso", f"Usuário {usuario.nome} alterado com sucesso!")

        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("✗ Entidade Não Encontrada", str(e))
        except RegraDeNegocioException as e:
            self.__view.mostrar_popup("✗ Erro de Negócio", str(e))
        except ValueError as e:
            self.__view.mostrar_popup("✗ Erro de Validação", str(e))
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro Inesperado", f"Erro ao alterar usuário: {str(e)}")

    def listar_usuarios(self):
        try:
            usuarios = Usuario.get_all()

            if not usuarios:
                self.__view.mostrar_popup("ℹ Informação", "Nenhum usuário cadastrado.")
                return

            dados_usuarios = []
            for usuario in usuarios:
                dados_usuarios.append({
                    "matricula": usuario.matricula,
                    "nome": usuario.nome,
                    "email": usuario.email
                })

            self.__view.mostra_usuarios(dados_usuarios)

        except Exception as e:
            self.__view.mostrar_popup("✗ Erro", f"Erro ao listar usuários: {str(e)}")

    def excluir_usuario(self):
        try:
            matricula = self.__view.pega_matricula_usuario()

            if matricula is None:
                return

            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException(f"Usuário com matrícula {matricula} não encontrado!")

            if len(usuario.ingressos_comprados) > 0:
                raise RegraDeNegocioException("Usuário com ingressos não pode ser excluído!")

            Usuario.remove(usuario)
            self.__view.mostrar_popup("✓ Sucesso", f"Usuário {usuario.nome} excluído com sucesso!")

        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("✗ Entidade Não Encontrada", str(e))
        except RegraDeNegocioException as e:
            self.__view.mostrar_popup("✗ Erro de Negócio", str(e))
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro Inesperado", f"Erro ao excluir usuário: {str(e)}")

    def ver_historico_compras(self):
        try:
            matricula = self.__view.pega_matricula_usuario()

            if matricula is None:
                return

            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException(f"Usuário com matrícula {matricula} não encontrado!")

            historico = usuario.historico_compras

            if not historico:
                self.__view.mostrar_popup("ℹ Informação", "Nenhuma compra realizada.")
                return

            dados_historico = []
            for i, venda in enumerate(historico, 1):
                dados_historico.append({
                    "tipo": "Ingresso",
                    "descricao": str(venda),
                    "valor": getattr(venda, 'preco', 0.0),
                    "data": str(getattr(venda, 'data_compra', 'N/A')),
                    "metodo": getattr(venda, 'metodo_pagamento', 'Não informado')
                })

            self.__view.mostra_historico_compras(dados_historico)

        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("✗ Entidade Não Encontrada", str(e))
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro", f"Erro ao visualizar histórico: {str(e)}")

    def listar_ingressos_usuario(self):
        try:
            matricula = self.__view.pega_matricula_usuario()

            if matricula is None:
                return

            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException(f"Usuário com matrícula {matricula} não encontrado!")

            ingressos = usuario.ingressos_comprados

            if not ingressos:
                self.__view.mostrar_popup("ℹ Informação", "Nenhum ingresso cadastrado.")
                return

            dados_ingressos = []
            for ingresso in ingressos:
                evento = getattr(ingresso, 'evento', None)
                evento_nome = getattr(evento, 'nome', 'Desconhecido') if evento else 'Desconhecido'
                evento_data = getattr(evento, 'data', 'N/A') if evento else 'N/A'
                evento_local = getattr(evento, 'local', 'N/A') if evento else 'N/A'

                dados_ingressos.append({
                    "evento_nome": evento_nome,
                    "evento_data": evento_data,
                    "evento_local": evento_local,
                    "preco": getattr(ingresso, 'preco', 0.0),
                    "data_compra": str(getattr(ingresso, 'data_compra', 'N/A'))
                })

            self.__view.mostra_ingressos_usuario(dados_ingressos)

        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("✗ Entidade Não Encontrada", str(e))
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro", f"Erro ao listar ingressos: {str(e)}")

    def avaliar_evento(self):
        try:
            dados_avaliacao = self.__view.pega_dados_avaliacao()

            if dados_avaliacao is None:
                return

            self.__view.mostrar_popup("✓ Sucesso", "Avaliação registrada com sucesso!")

        except Exception as e:
            self.__view.mostrar_popup("✗ Erro", f"Erro ao registrar avaliação: {str(e)}")

    # Métodos auxiliares necessários para outros controladores
    def buscar_usuario_por_matricula(self, matricula: str) -> Optional[Usuario]:
        """Busca usuário por matrícula - usado por outros controladores"""
        try:
            if not matricula:
                return None
            return Usuario.get_by_matricula(matricula)
        except Exception as e:
            print(f"Erro na busca por matrícula: {e}")
            return None

    def pega_matricula_usuario_gui(self) -> Optional[str]:
        """Coleta matrícula do usuário via interface GUI - usado pelo IngressoController"""
        try:
            return self.__view.pega_matricula_usuario()
        except Exception as e:
            print(f"Erro ao coletar matrícula via GUI: {e}")
            return None

    def listar_usuarios_objetos(self) -> List[Usuario]:
        """Retorna lista de objetos Usuario - usado para relatórios"""
        try:
            return Usuario.get_all()
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []

    def criar_usuario_teste(self, dados: dict) -> Usuario:
        """Método para criar usuários em testes"""
        try:
            if Usuario.get_by_matricula(dados['matricula']):
                raise RegraDeNegocioException("Matrícula já cadastrada!")
            
            usuario = Usuario(dados['matricula'], dados['nome'], dados['email'])
            Usuario.add(usuario)
            return usuario
            
        except Exception as e:
            raise RegraDeNegocioException(f"Erro ao criar usuário teste: {e}")

    def get_usuario_por_matricula(self, matricula: str) -> Optional[Usuario]:
        """Alias para buscar_usuario_por_matricula para compatibilidade"""
        return self.buscar_usuario_por_matricula(matricula)

    def validar_usuario_existe(self, matricula: str) -> bool:
        """Valida se um usuário existe"""
        try:
            usuario = Usuario.get_by_matricula(matricula)
            return usuario is not None
        except Exception:
            return False

    def obter_todos_usuarios(self) -> List[Usuario]:
        """Obtém todos os usuários - alias para listar_usuarios_objetos"""
        return self.listar_usuarios_objetos()

    def selecionar_usuario_gui(self) -> Optional[Usuario]:
        """Permite selecionar um usuário via GUI"""
        try:
            usuarios = Usuario.get_all()
            if not usuarios:
                self.__view.mostrar_popup("ℹ Informação", "Nenhum usuário cadastrado.")
                return None

            dados_usuarios = []
            for usuario in usuarios:
                dados_usuarios.append({
                    "matricula": usuario.matricula,
                    "nome": usuario.nome,
                    "email": usuario.email
                })

            matricula = self.__view.seleciona_usuario_lista(dados_usuarios)
            if matricula:
                return Usuario.get_by_matricula(matricula)
            return None

        except Exception as e:
            self.__view.mostrar_popup("✗ Erro", f"Erro ao selecionar usuário: {e}")
            return None

    def obter_dados_para_relatorio(self) -> List[dict]:
        """Obtém dados dos usuários formatados para relatórios"""
        try:
            usuarios = Usuario.get_all()
            dados_relatorio = []
            
            for usuario in usuarios:
                try:
                    total_ingressos = len(usuario.ingressos_comprados)
                    total_gasto = sum(ing.preco for ing in usuario.ingressos_comprados 
                                    if hasattr(ing, 'preco'))
                    
                    dados_relatorio.append({
                        'nome': usuario.nome,
                        'matricula': usuario.matricula,
                        'email': usuario.email,
                        'total_ingressos': total_ingressos,
                        'total_gasto': total_gasto,
                        'produtos_comprados': 0  # Para implementação futura
                    })
                except Exception as e:
                    print(f"Erro ao processar dados do usuário {usuario.nome}: {e}")
                    continue
            
            return dados_relatorio
            
        except Exception as e:
            print(f"Erro ao obter dados para relatório: {e}")
            return []

    def pega_matricula_usuario(self) -> Optional[str]:
        """Método direto para pegar matrícula - wrapper para a view"""
        try:
            return self.__view.pega_matricula_usuario()
        except Exception as e:
            print(f"Erro ao pegar matrícula do usuário: {e}")
            return None

    def selecionar_usuario_para_revenda(self) -> Optional[Usuario]:
        """Seleciona usuário específico para operações de revenda"""
        try:
            matricula = self.pega_matricula_usuario_gui()
            if not matricula:
                return None
            
            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                self.__view.mostrar_popup("✗ Erro", f"Usuário com matrícula {matricula} não encontrado!")
                return None
                
            return usuario
            
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro", f"Erro ao selecionar usuário: {e}")
            return None

    def obter_ingressos_usuario_para_revenda(self, matricula: str) -> List[dict]:
        """Obtém ingressos de um usuário formatados para revenda"""
        try:
            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                return []
            
            dados_ingressos = []
            for ingresso in usuario.ingressos_comprados:
                # Só incluir ingressos que não estão à venda
                if not hasattr(ingresso, 'em_revenda') or not ingresso.em_revenda:
                    evento = getattr(ingresso, 'evento', None)
                    evento_nome = getattr(evento, 'nome', 'Desconhecido') if evento else 'Desconhecido'
                    
                    dados_ingressos.append({
                        'nome_evento': evento_nome,
                        'preco': getattr(ingresso, 'preco', 0.0),
                        'data_compra': str(getattr(ingresso, 'data_compra', 'N/A')),
                        'ingresso_obj': ingresso  # Referência para uso posterior
                    })
            
            return dados_ingressos
            
        except Exception as e:
            print(f"Erro ao obter ingressos para revenda: {e}")
            return []

    def mostrar_popup(self, titulo: str, mensagem: str):
        """Wrapper para mostrar popup via view"""
        try:
            self.__view.mostrar_popup(titulo, mensagem)
        except Exception as e:
            print(f"Erro ao mostrar popup: {e}")
            print(f"Título: {titulo}, Mensagem: {mensagem}")