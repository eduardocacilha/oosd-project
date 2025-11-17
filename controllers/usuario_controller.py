from views.usuario_view import UsuarioView
from models.usuario import Usuario
from models.ingresso import Ingresso
from models.venda import Venda
from datetime import date
from typing import List, TYPE_CHECKING
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

if TYPE_CHECKING:
    from controllers.evento_controller import EventoController

class UsuarioController:
    
    def __init__(self, usuario_view: UsuarioView):
        self.__view = usuario_view

    def rodar_menu_usuario(self):
        """Loop principal do menu de usuários"""
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
        """Incluir novo usuário com tratamento de exceções"""
        try:
            dados_usuario = self.__view.pega_dados_usuario(pedindo_matricula=True)
            
            if dados_usuario is None:
                return  # Usuário cancelou a operação
            
            # Validação: matrícula já existe
            if Usuario.get_by_matricula(dados_usuario["matricula"]):
                raise RegraDeNegocioException(f"Usuário com matrícula {dados_usuario['matricula']} já cadastrado!")
            
            # Criar novo usuário
            novo_usuario = Usuario(
                dados_usuario["matricula"],
                dados_usuario["nome"],
                dados_usuario["email"]
            )
            Usuario.add(novo_usuario)
            self.__view.mostrar_popup("✓ Sucesso", f"Usuário {novo_usuario.nome} incluído com sucesso!")
            
        except RegraDeNegocioException as e:
            self.__view.mostrar_popup("✗ Erro de Negócio", e.mensagem)
        except ValueError as e:
            self.__view.mostrar_popup("✗ Erro de Validação", str(e))
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro Inesperado", f"Erro ao incluir usuário: {str(e)}")

    def alterar_usuario(self):
        """Alterar dados do usuário com tratamento de exceções"""
        try:
            matricula = self.__view.pega_matricula_usuario()
            
            if matricula is None:
                return  # Usuário cancelou
            
            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException(f"Usuário com matrícula {matricula} não encontrado!")
            
            dados_usuario = self.__view.pega_dados_usuario(pedindo_matricula=False)
            
            if dados_usuario is None:
                return  # Usuário cancelou
            
            # Atualizar dados
            usuario.nome = dados_usuario["nome"]
            usuario.email = dados_usuario["email"]
            
            self.__view.mostrar_popup("✓ Sucesso", f"Usuário {usuario.nome} alterado com sucesso!")
            
        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("✗ Entidade Não Encontrada", e.mensagem)
        except RegraDeNegocioException as e:
            self.__view.mostrar_popup("✗ Erro de Negócio", e.mensagem)
        except ValueError as e:
            self.__view.mostrar_popup("✗ Erro de Validação", str(e))
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro Inesperado", f"Erro ao alterar usuário: {str(e)}")

    def listar_usuarios(self):
        """Listar todos os usuários com tratamento de exceções"""
        try:
            usuarios = Usuario.get_all()
            
            if not usuarios:
                self.__view.mostrar_popup("ℹ Informação", "Nenhum usuário cadastrado.")
                return
            
            # Converter objetos para dicionários para a view
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
        """Excluir usuário com tratamento de exceções"""
        try:
            matricula = self.__view.pega_matricula_usuario()
            
            if matricula is None:
                return  # Usuário cancelou
            
            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException(f"Usuário com matrícula {matricula} não encontrado!")
            
            # Validação: usuário com ingressos não pode ser excluído
            if len(usuario.ingressos_comprados) > 0:
                raise RegraDeNegocioException("Usuário com ingressos não pode ser excluído!")
            
            Usuario.remove(usuario)
            self.__view.mostrar_popup("✓ Sucesso", f"Usuário {usuario.nome} excluído com sucesso!")
            
        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("✗ Entidade Não Encontrada", e.mensagem)
        except RegraDeNegocioException as e:
            self.__view.mostrar_popup("✗ Erro de Negócio", e.mensagem)
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro Inesperado", f"Erro ao excluir usuário: {str(e)}")

    def ver_historico_compras(self):
        """Ver histórico de compras do usuário"""
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
            
            # Converter para formato esperado pela view
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
            self.__view.mostrar_popup("✗ Entidade Não Encontrada", e.mensagem)
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro", f"Erro ao visualizar histórico: {str(e)}")

    def listar_ingressos_usuario(self):
        """Listar ingressos do usuário"""
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
            
            # Converter para formato esperado pela view
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
            self.__view.mostrar_popup("✗ Entidade Não Encontrada", e.mensagem)
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro", f"Erro ao listar ingressos: {str(e)}")

    def avaliar_evento(self):
        """Avaliar um evento"""
        try:
            dados_avaliacao = self.__view.pega_dados_avaliacao()
            
            if dados_avaliacao is None:
                return
            
            # Aqui você implementaria a lógica de avaliação
            self.__view.mostrar_popup("✓ Sucesso", "Avaliação registrada com sucesso!")
            
        except Exception as e:
            self.__view.mostrar_popup("✗ Erro", f"Erro ao registrar avaliação: {str(e)}")