from models.usuario import Usuario


class UsuarioController:
    def __init__(self):
        self.__usuarios = []

    def incluir_usuario(self, dados_usuario):
       # Inclui um novo usuário no sistema
        # Verifica se já existe usuário com essa matrícula
        for usuario in self.__usuarios:
            if usuario.matricula == dados_usuario["matricula"]:
                return {"sucesso": False, "mensagem": "Já existe um usuário com essa matrícula"}
        
        # Cria o usuário
        usuario = Usuario(
            dados_usuario["matricula"], 
            dados_usuario["nome"], 
            dados_usuario["email"]
        )
        self.__usuarios.append(usuario)
        return {"sucesso": True, "mensagem": f"Usuário {dados_usuario['nome']} incluído com sucesso"}

    def listar_usuarios(self):
       # Lista todos os usuários
        return self.__usuarios

    def buscar_usuario_por_matricula(self, matricula):
       # Busca usuário pela matrícula
        for usuario in self.__usuarios:
            if usuario.matricula == matricula:
                return usuario
        return None

    def excluir_usuario(self, matricula):
       # Exclui um usuário pela matrícula
        usuario = self.buscar_usuario_por_matricula(matricula)
        if usuario is None:
            return {"sucesso": False, "mensagem": "Usuário não encontrado"}
        
        # Verifica se o usuário tem ingressos
        if len(usuario.ingressos_comprados) > 0:
            return {"sucesso": False, "mensagem": "Não é possível excluir usuário que possui ingressos"}
        
        self.__usuarios.remove(usuario)
        return {"sucesso": True, "mensagem": f"Usuário {usuario.nome} excluído com sucesso"}

    def avaliar_evento(self, matricula_usuario, evento, nota, comentario):
       # Permite que um usuário avalie um evento
        usuario = self.buscar_usuario_por_matricula(matricula_usuario)
        if usuario is None:
            return {"sucesso": False, "mensagem": "Usuário não encontrado"}
        
        if not isinstance(nota, int) or nota < 1 or nota > 5:
            return {"sucesso": False, "mensagem": "Nota deve ser um número entre 1 e 5"}
        
        feedback = usuario.avaliar_evento(evento, nota, comentario)
        return {"sucesso": True, "mensagem": "Avaliação realizada com sucesso", "feedback": feedback}

    def comprar_ingresso(self, matricula_usuario, evento, preco=None):
       # Permite que um usuário compre um ingresso
        usuario = self.buscar_usuario_por_matricula(matricula_usuario)
        if usuario is None:
            return {"sucesso": False, "mensagem": "Usuário não encontrado"}
        
        ingresso = usuario.comprar_ingresso(evento, preco)
        return {"sucesso": True, "mensagem": "Ingresso comprado com sucesso", "ingresso": ingresso}

    def ver_historico_compras(self, matricula_usuario):
       # Retorna o histórico de compras de um usuário
        usuario = self.buscar_usuario_por_matricula(matricula_usuario)
        if usuario is None:
            return {"sucesso": False, "mensagem": "Usuário não encontrado"}
        
        historico = usuario.ver_historico_compras()
        return {"sucesso": True, "historico": historico}

    def listar_ingressos_usuario(self, matricula_usuario):
       # Lista todos os ingressos de um usuário
        usuario = self.buscar_usuario_por_matricula(matricula_usuario)
        if usuario is None:
            return {"sucesso": False, "mensagem": "Usuário não encontrado"}
        
        ingressos = usuario.listar_ingressos()
        return {"sucesso": True, "ingressos": ingressos}

    def colocar_ingresso_a_venda(self, matricula_usuario, ingresso, novo_preco):
       # Coloca um ingresso à venda
        usuario = self.buscar_usuario_por_matricula(matricula_usuario)
        if usuario is None:
            return {"sucesso": False, "mensagem": "Usuário não encontrado"}
        
        if novo_preco <= 0:
            return {"sucesso": False, "mensagem": "Preço deve ser maior que zero"}
        
        if ingresso not in usuario.ingressos_comprados:
            return {"sucesso": False, "mensagem": "Este ingresso não pertence a este usuário"}
        
        ingresso.preco = novo_preco
        ingresso.revendedor = usuario
        return {"sucesso": True, "mensagem": f"Ingresso colocado à venda por R$ {novo_preco:.2f}"}

    def remover_ingresso_da_venda(self, matricula_usuario, ingresso):
       # Remove um ingresso da venda
        usuario = self.buscar_usuario_por_matricula(matricula_usuario)
        if usuario is None:
            return {"sucesso": False, "mensagem": "Usuário não encontrado"}
        
        if ingresso.revendedor != usuario:
            return {"sucesso": False, "mensagem": "Este ingresso não está sendo revendido por você"}
        
        ingresso.revendedor = None
        return {"sucesso": True, "mensagem": "Revenda do ingresso cancelada"}

    def comprar_ingresso_revenda(self, matricula_comprador, ingresso):
       # Compra um ingresso em revenda
        comprador = self.buscar_usuario_por_matricula(matricula_comprador)
        if comprador is None:
            return {"sucesso": False, "mensagem": "Usuário comprador não encontrado"}
        
        if ingresso.revendedor is None:
            return {"sucesso": False, "mensagem": "Este ingresso não está em revenda"}
        
        if comprador == ingresso.revendedor:
            return {"sucesso": False, "mensagem": "Você não pode comprar um ingresso de si mesmo"}
        
        # Transfere o ingresso
        revendedor = ingresso.revendedor
        if ingresso in revendedor.ingressos_comprados:
            revendedor.ingressos_comprados.remove(ingresso)
        
        ingresso.revendedor = None
        ingresso.comprador = comprador
        comprador.ingressos_comprados.append(ingresso)
        
        return {"sucesso": True, "mensagem": f"Ingresso comprado com sucesso de {revendedor.nome}"}

    def listar_ingressos_a_venda(self, matricula_usuario, lista_ingressos_geral):
       # Lista ingressos que um usuário está vendendo
        usuario = self.buscar_usuario_por_matricula(matricula_usuario)
        if usuario is None:
            return {"sucesso": False, "mensagem": "Usuário não encontrado"}
        
        ingressos_a_venda = usuario.listar_ingressos_a_venda(lista_ingressos_geral)
        return {"sucesso": True, "ingressos_a_venda": ingressos_a_venda}