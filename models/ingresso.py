class Ingresso:
    def __init__(self, evento, comprador, data_compra, preco):
        self.evento = evento
        self.comprador = comprador
        self.data_compra = data_compra
        self.preco = preco
        self.revendedor = None

    def __repr__(self):
        return f"Ingresso(evento={self.evento}, comprador={self.comprador}, data_compra={self.data_compra}, preco={self.preco})"