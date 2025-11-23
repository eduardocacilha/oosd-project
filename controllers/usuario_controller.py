from views.usuario_view import UsuarioView
from models.usuario import Usuario
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException
from typing import Optional, List, TYPE_CHECKING
from DAOs.usuario_dao import UsuarioDAO

if TYPE_CHECKING:
    from controllers.evento_controller import EventoController


class UsuarioController:

    def __init__(self, usuario_view: UsuarioView):
        self.__view = usuario_view
        from typing import Optional as _Optional

        self.__evento_controller: _Optional["EventoController"] = None
        self.__usuario_dao = UsuarioDAO()

    def set_evento_controller(self, evento_controller):
        self.__evento_controller = evento_controller

    def rodar_menu_usuario(self):
        while True:
            opcao = self.__view.criar_janela_menu_usuario()
            if opcao == "0":
                break
            elif opcao == "1":
                self.incluir_usuario()
            elif opcao == "2":
                self.listar_usuarios()
            elif opcao == "3":
                self.alterar_usuario()
            elif opcao == "4":
                self.excluir_usuario()
            elif opcao == "5":
                self.ver_historico_compras()
            elif opcao == "6":
                self.listar_ingressos_usuario()
            elif opcao == "7":
                self.avaliar_evento()

    def incluir_usuario(self):
        try:
            dados_usuario = self.__view.pega_dados_usuario(pedindo_matricula=True)
            if not dados_usuario:
                return
            if self.__usuario_dao.get(dados_usuario["matricula"]):
                raise RegraDeNegocioException("Matrícula já cadastrada!")
            usuario = Usuario(
                dados_usuario["matricula"],
                dados_usuario["nome"],
                dados_usuario["email"],
            )
            self.__usuario_dao.add(usuario)
            self.__view.mostrar_popup("Sucesso", "Usuário incluído com sucesso!")
        except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro ao incluir usuário: {e}")

    def alterar_usuario(self):
        try:
            matricula = self.__view.pega_matricula_usuario()
            if not matricula:
                return
            usuario = self.__usuario_dao.get(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")
            novos = self.__view.pega_dados_usuario(pedindo_matricula=False)
            if not novos:
                return
            usuario.nome = novos["nome"]
            usuario.email = novos["email"]
            self.__usuario_dao.update(usuario)
            self.__view.mostrar_popup("Sucesso", "Usuário alterado com sucesso!")
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro ao alterar usuário: {e}")

    def listar_usuarios(self):
        usuarios = list(self.__usuario_dao.get_all())
        if not usuarios:
            self.__view.mostrar_popup("Info", "Nenhum usuário cadastrado.")
            return
        dados = [
            {"matricula": u.matricula, "nome": u.nome, "email": u.email}
            for u in usuarios
        ]
        self.__view.mostra_usuarios(dados)

    def excluir_usuario(self):
        try:
            matricula = self.__view.pega_matricula_usuario()
            if not matricula:
                return
            usuario = self.__usuario_dao.get(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")
            if getattr(usuario, "ingressos_comprados", []):
                raise RegraDeNegocioException("Usuário possui ingressos.")
            self.__usuario_dao.remove(matricula)
            self.__view.mostrar_popup("Sucesso", "Usuário excluído.")
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro ao excluir usuário: {e}")

    def ver_historico_compras(self):
        matricula = self.__view.pega_matricula_usuario()
        if not matricula:
            return
        usuario = self.__usuario_dao.get(matricula)
        if not usuario:
            self.__view.mostrar_popup("Erro", "Usuário não encontrado.")
            return
        historico = getattr(usuario, "historico_compras", [])
        if not historico:
            self.__view.mostrar_popup("Info", "Nenhuma compra realizada.")
            return
        dados = []
        for h in historico:
            if isinstance(h, dict):
                dados.append(
                    {
                        "tipo": h.get("tipo", "Dado"),
                        "descricao": f"Ingresso revendido - Preço R$ {h.get('preco', 0):.2f}",
                        "valor": h.get("preco", 0.0),
                        "data": str(getattr(h.get("ingresso"), "data_compra", "N/A")),
                        "metodo": getattr(h.get("ingresso"), "metodo_pagamento", "N/A"),
                    }
                )
            else:
                dados.append(
                    {
                        "tipo": getattr(h, "__class__", type("X", (), {})).__name__,
                        "descricao": str(h),
                        "valor": getattr(h, "preco", getattr(h, "total", 0.0)),
                        "data": str(
                            getattr(h, "data_compra", getattr(h, "data_hora", "N/A"))
                        ),
                        "metodo": getattr(h, "metodo_pagamento", "N/A"),
                    }
                )
        self.__view.mostra_historico_compras(dados)

    def listar_ingressos_usuario(self):
        matricula = self.__view.pega_matricula_usuario()
        if not matricula:
            return
        usuario = self.__usuario_dao.get(matricula)
        if not usuario:
            self.__view.mostrar_popup("Erro", "Usuário não encontrado.")
            return
        ingressos = list(getattr(usuario, "ingressos_comprados", []))
        if not ingressos:
            try:
                from DAOs.ingresso_dao import IngressoDAO

                ingresso_dao = IngressoDAO()
                for ing in ingresso_dao.get_all():
                    if getattr(ing, "comprador", None) == usuario:
                        ingressos.append(ing)
                if not ingressos:
                    self.__view.mostrar_popup("Info", "Nenhum ingresso cadastrado.")
                    return
            except Exception as e:
                self.__view.mostrar_popup("Erro", f"Falha ao recuperar ingressos: {e}")
                return
        dados = []
        for ing in ingressos:
            ev = getattr(ing, "evento", None)
            dados.append(
                {
                    "evento_nome": getattr(ev, "nome", "N/A"),
                    "evento_data": getattr(ev, "data", "N/A"),
                    "evento_local": getattr(ev, "local", "N/A"),
                    "preco": getattr(ing, "preco", 0.0),
                    "data_compra": str(getattr(ing, "data_compra", "N/A")),
                }
            )
        self.__view.mostra_ingressos_usuario(dados)

    def avaliar_evento(self):
        if not self.__evento_controller:
            self.__view.mostrar_popup("Erro", "Controlador de eventos indisponível.")
            return
        usuarios = list(self.__usuario_dao.get_all())
        if not usuarios:
            self.__view.mostrar_popup("Aviso", "Sem usuários cadastrados.")
            return
        if not self.__evento_controller.get_eventos_lista():
            self.__view.mostrar_popup("Aviso", "Sem eventos cadastrados.")
            return
        matricula = self.__view.pega_matricula_usuario()
        if not matricula:
            return
        usuario = self.__usuario_dao.get(matricula)
        if not usuario:
            self.__view.mostrar_popup("Erro", "Usuário não encontrado.")
            return
        evento = self.__evento_controller.selecionar_evento_gui()
        if not evento:
            return
        dados = self.__view.pega_dados_avaliacao()
        if not dados:
            return
        from models.feedback import Feedback
        from datetime import date as _date

        try:
            feedback = Feedback(
                usuario=usuario,
                evento=evento,
                nota=dados["nota"],
                comentario=dados["comentario"],
                data=_date.today(),
            )
            evento.adicionar_feedback(feedback)
            from DAOs.feedback_dao import FeedbackDAO

            FeedbackDAO().add(feedback)
            if hasattr(self.__evento_controller, "persistir_evento"):
                self.__evento_controller.persistir_evento(evento)
            self.__view.mostrar_popup("Sucesso", "Feedback registrado.")
        except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Falha ao registrar feedback: {e}")

    def buscar_usuario_por_matricula(self, matricula: str) -> Optional[Usuario]:
        if not matricula:
            return None
        return self.__usuario_dao.get(matricula)

    def pega_matricula_usuario_gui(self) -> Optional[str]:
        return self.__view.pega_matricula_usuario()

    def listar_usuarios_objetos(self) -> List[Usuario]:
        return list(self.__usuario_dao.get_all())

    def criar_usuario_teste(self, dados: dict) -> Usuario:
        if self.__usuario_dao.get(dados["matricula"]):
            raise RegraDeNegocioException("Matrícula já cadastrada!")
        usuario = Usuario(dados["matricula"], dados["nome"], dados["email"])
        self.__usuario_dao.add(usuario)
        return usuario

    def get_usuario_por_matricula(self, matricula: str) -> Optional[Usuario]:
        return self.__usuario_dao.get(matricula)

    def validar_usuario_existe(self, matricula: str) -> bool:
        return self.__usuario_dao.get(matricula) is not None

    def obter_todos_usuarios(self) -> List[Usuario]:
        return list(self.__usuario_dao.get_all())

    def selecionar_usuario_gui(self) -> Optional[Usuario]:
        matricula = self.__view.pega_matricula_usuario()
        if not matricula:
            return None
        usuario = self.__usuario_dao.get(matricula)
        if not usuario:
            self.__view.mostrar_popup("Erro", "Usuário não encontrado.")
            return None
        return usuario

    def obter_dados_para_relatorio(self) -> List[dict]:
        usuarios = list(self.__usuario_dao.get_all())
        dados = []
        for u in usuarios:
            total_ingressos = len(getattr(u, "ingressos_comprados", []))
            total_gasto = 0
            for ing in getattr(u, "ingressos_comprados", []):
                total_gasto += getattr(ing, "preco", 0)
            dados.append(
                {
                    "nome": u.nome,
                    "matricula": u.matricula,
                    "email": u.email,
                    "total_ingressos": total_ingressos,
                    "total_gasto": total_gasto,
                    "produtos_comprados": 0,
                }
            )
        return dados

    def pega_matricula_usuario(self) -> Optional[str]:
        return self.__view.pega_matricula_usuario()

    def selecionar_usuario_para_revenda(self) -> Optional[Usuario]:
        matricula = self.pega_matricula_usuario_gui()
        if not matricula:
            return None
        usuario = self.__usuario_dao.get(matricula)
        if not usuario:
            self.__view.mostrar_popup("Erro", "Usuário não encontrado.")
            return None
        return usuario

    def obter_ingressos_usuario_para_revenda(self, matricula: str) -> List[dict]:
        usuario = self.__usuario_dao.get(matricula)
        if not usuario:
            return []
        dados = []
        for ingresso in getattr(usuario, "ingressos_comprados", []):
            if not getattr(ingresso, "em_revenda", False):
                ev = getattr(ingresso, "evento", None)
                dados.append(
                    {
                        "nome_evento": getattr(ev, "nome", "N/A"),
                        "preco": getattr(ingresso, "preco", 0.0),
                        "data_compra": str(getattr(ingresso, "data_compra", "N/A")),
                        "ingresso_obj": ingresso,
                    }
                )
        return dados

    def mostrar_popup(self, titulo: str, mensagem: str):
        self.__view.mostrar_popup(titulo, mensagem)

    def recarregar_usuarios(self):
        try:
            from DAOs.usuario_dao import UsuarioDAO

            self.__usuario_dao = UsuarioDAO()
        except Exception as e:
            self.__view.mostrar_popup("Aviso", f"Falha ao recarregar usuários: {e}")
