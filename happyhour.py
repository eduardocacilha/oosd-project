try:
    from .evento import Evento
    from .venda import Venda
except ImportError:
    from evento import Evento  # type: ignore
    from venda import Venda  # type: ignore


class HappyHour(Evento):
    def __init__(self, nome: str, data, local: str, horario_inicio: str, horario_fim: str, eh_open_bar: bool, entrada_gratuita: bool):
        super().__init__(nome=nome, data=data, local=local)
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim
        self.__eh_open_bar = bool(eh_open_bar)
        self.__entrada_gratuita = bool(entrada_gratuita)
        self.__vendas: list[Venda] = []

    def registrar_venda(self, venda):
        self.__vendas.append(venda)

    def get_faturamento_total(self) -> float:
        total = 0.0
        if not self.__entrada_gratuita:
            total += 0.0 
        total += sum(v.valor_total for v in self.__vendas)
        return round(total, 2)

    @property
    def horario_inicio(self):
        return self.__horario_inicio

    @horario_inicio.setter
    def horario_inicio(self, value):
        self.__horario_inicio = value

    @property
    def horario_fim(self):
        return self.__horario_fim

    @horario_fim.setter
    def horario_fim(self, value):
        self.__horario_fim = value

    @property
    def eh_open_bar(self):
        return self.__eh_open_bar

    @eh_open_bar.setter
    def eh_open_bar(self, value):
        self.__eh_open_bar = bool(value)

    @property
    def entrada_gratuita(self):
        return self.__entrada_gratuita

    @entrada_gratuita.setter
    def entrada_gratuita(self, value):
        self.__entrada_gratuita = bool(value)

    @property
    def vendas(self):
        return self.__vendas