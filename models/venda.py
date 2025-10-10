class Venda:
    def __init__(self, id_venda: int, metodo_pagamento: str, data_hora):
        self.id_venda = id_venda
        self.metodo_pagamento = metodo_pagamento
        self.data_hora = data_hora

    def __repr__(self):
        return f"Venda(id_venda={self.id_venda}, metodo_pagamento='{self.metodo_pagamento}', data_hora={self.data_hora})"