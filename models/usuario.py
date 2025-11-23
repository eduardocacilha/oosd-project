from __future__ import annotations
from datetime import date
from typing import List, Optional
from .venda import Venda
from .feedback import Feedback
from .evento import Evento
from exceptions.regraDeNegocioException import RegraDeNegocioException


class Usuario:
    _registros: List["Usuario"] = []
    _next_id = 1

    def __init__(self, matricula: str, nome: str, email: str):
        if not matricula.isdigit():
            raise RegraDeNegocioException("Matrícula deve conter apenas números")
        if not nome or len(nome) < 2:
            raise RegraDeNegocioException("Nome deve ter pelo menos 2 caracteres")
        if not email or "@" not in email:
            raise RegraDeNegocioException("Email inválido")
        self.__matricula = matricula
        self.__nome = nome
        self.__email = email
        self.__historico_compras: List[Venda] = []
        self.__ingressos_comprados: List["Ingresso"] = []
        Usuario._registros.append(self)

    @classmethod
    def get_by_matricula(cls, matricula: str) -> Optional["Usuario"]:
        for u in cls._registros:
            if u.matricula == matricula:
                return u
        return None

    @classmethod
    def get_all(cls) -> List["Usuario"]:
        return list(cls._registros)

    @classmethod
    def add(cls, usuario: "Usuario"):
        if usuario not in cls._registros:
            cls._registros.append(usuario)

    @classmethod
    def remove(cls, usuario: "Usuario"):
        if usuario in cls._registros:
            cls._registros.remove(usuario)

    def comprar_ingresso(
        self,
        evento: Evento,
        preco: Optional[float] = None,
        metodo_pagamento: str = "Não informado",
    ) -> "Ingresso":
        try:
            from .ingresso import Ingresso

            if evento is None:
                raise RegraDeNegocioException("Evento não pode ser nulo")
            if preco is None:
                preco = getattr(evento, "preco_entrada", 0.0)
            if preco < 0:
                raise RegraDeNegocioException("Preço do ingresso não pode ser negativo")
            ingresso = Ingresso(evento, self, date.today(), preco, metodo_pagamento)
            self.__ingressos_comprados.append(ingresso)
            if hasattr(evento, "registrar_compra_ingresso"):
                evento.registrar_compra_ingresso(ingresso)
            self.__historico_compras.append(ingresso)
            return ingresso
        except RegraDeNegocioException:
            raise
        except Exception as e:
            raise RegraDeNegocioException(f"Erro ao comprar ingresso: {str(e)}")

    def colocar_ingresso_a_venda(self, ingresso: "Ingresso", novo_preco: float):
        try:
            if ingresso not in self.__ingressos_comprados:
                raise RegraDeNegocioException(
                    "Este ingresso não pertence a este usuário"
                )
            if novo_preco <= 0:
                raise RegraDeNegocioException("Preço deve ser maior que zero")
            ingresso.preco = novo_preco
            ingresso.revendedor = self
        except RegraDeNegocioException:
            raise
        except Exception as e:
            raise RegraDeNegocioException(f"Erro ao colocar ingresso à venda: {str(e)}")

    def remover_ingresso_da_venda(self, ingresso: "Ingresso"):
        try:
            if ingresso.revendedor != self:
                raise RegraDeNegocioException(
                    "Este ingresso não está sendo revendido por você"
                )
            ingresso.revendedor = None
        except RegraDeNegocioException:
            raise
        except Exception as e:
            raise RegraDeNegocioException(
                f"Erro ao remover ingresso da venda: {str(e)}"
            )

    def comprar_ingresso_revenda(self, ingresso: "Ingresso"):
        try:
            from .ingresso import Ingresso  # evitar import circular em topo

            if not isinstance(ingresso, Ingresso):
                raise RegraDeNegocioException("Ingresso inválido para revenda")
            revendedor = ingresso.revendedor
            if revendedor is None:
                raise RegraDeNegocioException("Ingresso não está em revenda")
            if revendedor == self:
                raise RegraDeNegocioException(
                    "Você já é o comprador atual deste ingresso"
                )
            try:
                if ingresso in revendedor.ingressos_comprados:
                    revendedor.ingressos_comprados.remove(ingresso)
                else:
                    priv = getattr(revendedor, "_Usuario__ingressos_comprados", None)
                    if priv is not None and ingresso in priv:
                        priv.remove(ingresso)
            except Exception:
                pass
            ingresso.comprador = self
            ingresso.revendedor = None
            if ingresso not in self.ingressos_comprados:
                try:
                    self.ingressos_comprados.append(ingresso)
                except AttributeError:
                    priv_self = getattr(self, "_Usuario__ingressos_comprados", None)
                    if priv_self is not None and ingresso not in priv_self:
                        priv_self.append(ingresso)
            try:
                self.__historico_compras.append(ingresso)
                rev_hist = getattr(revendedor, "_Usuario__historico_compras", None)
                if rev_hist is not None:
                    rev_hist.append(
                        {
                            "tipo": "REVENDIDO",
                            "preco": ingresso.preco,
                            "ingresso": ingresso,
                        }
                    )
            except Exception:
                pass
        except RegraDeNegocioException:
            raise
        except Exception as e:
            raise RegraDeNegocioException(
                f"Erro ao concluir compra de revenda: {str(e)}"
            )

    def adicionar_venda_historico(self, venda: Venda):
        try:
            if venda is None:
                raise RegraDeNegocioException("Venda não pode ser nula")
            self.__historico_compras.append(venda)
        except RegraDeNegocioException:
            raise
        except Exception as e:
            raise RegraDeNegocioException(
                f"Erro ao adicionar venda ao histórico: {str(e)}"
            )

    def listar_ingressos(self) -> List["Ingresso"]:
        try:
            return list(self.__ingressos_comprados)
        except Exception as e:
            raise RegraDeNegocioException(f"Erro ao listar ingressos: {str(e)}")

    @property
    def matricula(self) -> str:
        return self.__matricula

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, value: str):
        if not value or len(value) < 2:
            raise RegraDeNegocioException("Nome deve ter pelo menos 2 caracteres")
        self.__nome = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        if not value or "@" not in value:
            raise RegraDeNegocioException("Email inválido")
        self.__email = value

    @property
    def historico_compras(self) -> List[Venda]:
        return self.__historico_compras

    @property
    def ingressos_comprados(self) -> List["Ingresso"]:
        return self.__ingressos_comprados
