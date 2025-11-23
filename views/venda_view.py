import FreeSimpleGUI as sg
from typing import List, Dict


class VendaView:
    def __init__(self):
        sg.theme("Reddit")

    def mostrar_popup(self, titulo: str, msg: str):
        sg.Popup(titulo, msg, keep_on_top=True, modal=True)

    def tela_opcoes(self) -> int:
        layout = [
            [
                sg.Text(
                    "\n-------- MENU VENDAS ----------", font=("Helvetica", 14, "bold")
                )
            ],
            [sg.Button("Nova Venda", key=1, size=(30, 1))],
            [sg.Button("Listar Vendas", key=2, size=(30, 1))],
            [sg.Button("Voltar", key=0, size=(30, 1), button_color=("white", "red"))],
        ]
        janela = sg.Window("Menu Vendas", layout, finalize=True, modal=True)
        evento, _ = janela.read()
        janela.close()
        return 0 if evento in (sg.WINDOW_CLOSED, None) else evento

    def escolher_metodo_pagamento(self) -> str | None:
        layout = [
            [sg.Text("Método de Pagamento", font=("Helvetica", 12, "bold"))],
            [
                sg.Combo(
                    ["PIX", "Débito", "Crédito", "Dinheiro"],
                    key="-METODO-",
                    readonly=True,
                )
            ],
            [sg.Button("OK", key="-OK-"), sg.Button("Cancelar", key="-CANCEL-")],
        ]
        janela = sg.Window("Pagamento", layout, modal=True, finalize=True)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WINDOW_CLOSED, "-CANCEL-"):
                janela.close()
                return None
            if evento == "-OK-":
                metodo = valores["-METODO-"]
                if metodo:
                    janela.close()
                    return metodo
                else:
                    self.mostrar_popup("Erro", "Selecione um método.")

    def selecionar_produto_para_venda(self, produtos: List[Dict]) -> int | None:
        headings = ["#", "Descrição", "Preço", "Estoque"]
        dados = [
            [i + 1, p["descricao"], f"R$ {p['preco']:.2f}", p["estoque"]]
            for i, p in enumerate(produtos)
        ]
        layout = [
            [sg.Text("Selecione Produto", font=("Helvetica", 12, "bold"))],
            [
                sg.Table(
                    values=dados,
                    headings=headings,
                    key="-TAB-",
                    enable_events=True,
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    num_rows=min(len(dados), 10),
                )
            ],
            [
                sg.Button("Adicionar", key="-ADD-"),
                sg.Button("Cancelar", key="-CANCEL-"),
            ],
        ]
        janela = sg.Window("Produtos", layout, modal=True, finalize=True)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WINDOW_CLOSED, "-CANCEL-"):
                janela.close()
                return None
            if evento == "-ADD-":
                sel = valores["-TAB-"]
                if not sel:
                    self.mostrar_popup("Aviso", "Selecione uma linha.")
                    continue
                idx = sel[0]
                janela.close()
                return idx

    def pegar_quantidade(self) -> int | None:
        layout = [
            [sg.Text("Quantidade:"), sg.Input(key="-QTD-", size=(10, 1))],
            [sg.Button("OK", key="-OK-"), sg.Button("Cancelar", key="-CANCEL-")],
        ]
        janela = sg.Window("Quantidade", layout, modal=True, finalize=True)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WINDOW_CLOSED, "-CANCEL-"):
                janela.close()
                return None
            if evento == "-OK-":
                try:
                    qtd = int(valores["-QTD-"].strip())
                    if qtd <= 0:
                        raise ValueError
                    janela.close()
                    return qtd
                except Exception:
                    self.mostrar_popup("Erro", "Quantidade inválida.")

    def confirmar_continuar(self) -> bool:
        return sg.popup_yes_no("Adicionar outro item?", title="Continuar?") == "Yes"

    def mostrar_resumo_venda(self, dados: dict):
        itens = dados.get("itens", [])
        linhas = []
        for i, it in enumerate(itens, 1):
            linhas.append(
                f"{i}. {it['produto']} x{it['quantidade']} = R$ {it['subtotal']:.2f}"
            )
        texto_itens = "\n".join(linhas) if linhas else "Sem itens."
        sg.Popup(
            "Venda Realizada",
            f"Cliente: {dados.get('cliente')}\nEvento: {dados.get('evento')}\nMétodo: {dados.get('metodo')}\nTotal: R$ {dados.get('total'):.2f}\n\nItens:\n{texto_itens}",
            keep_on_top=True,
        )

    def mostrar_lista_vendas(self, lista: List[dict]):
        if not lista:
            self.mostrar_popup("Info", "Nenhuma venda cadastrada.")
            return
        headings = ["ID", "Cliente", "Evento", "Data/Hora", "Método", "Total (R$)"]
        dados = [
            [
                v["id_venda"],
                v["cliente"],
                v["evento"],
                v["data"],
                v["metodo"],
                f"{v['total']:.2f}",
            ]
            for v in lista
        ]
        layout = [
            [sg.Text("Lista de Vendas", font=("Helvetica", 14, "bold"))],
            [
                sg.Table(
                    values=dados,
                    headings=headings,
                    key="-T-",
                    num_rows=min(len(dados), 12),
                )
            ],
            [sg.Button("Fechar")],
        ]
        janela = sg.Window("Vendas", layout, modal=True, finalize=True)
        janela.read()
        janela.close()
