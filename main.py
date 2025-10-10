 HEAD
from controllers.main_controller import MainController

def main():
    controller = MainController()
    controller.iniciar()

if __name__ == "__main__":
    main()
    

from datetime import date, datetime
try:
    from .usuario import Usuario
    from .festa import Festa
    from .happyhour import HappyHour
    from .bebida import Bebida
    from .camisa import Camisa
    from .copo import Copo
    from .feedback import Feedback
    from .venda import Venda
except ImportError:
    from usuario import Usuario  # type: ignore
    from festa import Festa  # type: ignore
    from happyhour import HappyHour  # type: ignore
    from bebida import Bebida  # type: ignore
    from camisa import Camisa  # type: ignore
    from copo import Copo  # type: ignore
    from feedback import Feedback  # type: ignore
    from venda import Venda  # type: ignore

def teste_produtos():
    """Testa criação e funcionalidades básicas dos produtos"""
    print("=== TESTE DE PRODUTOS ===")
    
    # Criar produtos
    cerveja = Bebida(1, "Cerveja Premium", 8.50, 100, 350, 4.5)
    camisa = Camisa(2, "Camisa da Festa", 25.0, 50, "M", "azul")
    copo = Copo(3, "Copo Personalizado", 5.0, 200, 300, "plastico")
    
    # Testar descrições
    print(f"Cerveja: {cerveja.descricao()}")
    print(f"Camisa: {camisa.descricao()}")
    print(f"Copo: {copo.descricao()}")
    
    # Testar propriedades
    print(f"Estoque cerveja: {cerveja.estoque}")
    print(f"Preço camisa: {camisa.preco}")
    print(f"Volume copo: {copo.capacidade_ml}ml")
    
    # Testar verificação de estoque
    print(f"Cerveja tem estoque para 10 unidades? {cerveja.verificar_estoque(10)}")
    print(f"Cerveja tem estoque para 150 unidades? {cerveja.verificar_estoque(150)}")
    
    # Testar baixa de estoque
    print(f"Estoque antes: {cerveja.estoque}")
    cerveja.baixar_estoque(5)
    print(f"Estoque após baixar 5: {cerveja.estoque}")
    
    print("✅ Teste de produtos concluído!\n")
    return cerveja, camisa, copo

def teste_usuario():
    """Testa criação e funcionalidades do usuário"""
    print("=== TESTE DE USUÁRIO ===")
    
    # Criar usuário
    usuario = Usuario("12345", "João Silva", "joao@email.com", False)
    admin = Usuario("99999", "Admin", "admin@email.com", True)
    
    # Testar propriedades
    print(f"Nome: {usuario.nome}")
    print(f"Matrícula: {usuario.matricula}")
    print(f"Email: {usuario.email}")
    print(f"É admin? {usuario.adm}")
    print(f"Admin é admin? {admin.adm}")
    
    # Testar login
    print(f"Login bem-sucedido? {usuario.fazer_login()}")
    
    print("✅ Teste de usuário concluído!\n")
    return usuario, admin

def teste_feedback():
    """Testa criação e funcionalidades do feedback"""
    print("=== TESTE DE FEEDBACK ===")
    
    # Criar feedbacks
    fb1 = Feedback(9, "Festa excelente!", date.today())
    fb2 = Feedback(7, "Boa organização", date.today())
    
    # Testar propriedades
    print(f"Feedback 1: {fb1.get_detalhes()}")
    print(f"Feedback 2: {fb2.get_detalhes()}")
    
    # Testar setter com validação
    try:
        fb1.nota = 11  # Deve dar erro
    except ValueError as e:
        print(f"Erro esperado: {e}")
    
    try:
        fb1.nota = 5  # Deve funcionar
        print(f"Nota alterada para: {fb1.nota}")
    except ValueError as e:
        print(f"Erro inesperado: {e}")
    
    print("✅ Teste de feedback concluído!\n")
    return fb1, fb2

def teste_venda(produtos):
    """Testa criação e funcionalidades da venda"""
    print("=== TESTE DE VENDA ===")
    
    cerveja, camisa, copo = produtos
    
    # Criar venda
    venda = Venda(1, "pix", datetime.now())
    
    # Adicionar itens
    print("Adicionando itens à venda...")
    venda.adicionar_item(cerveja, 3)
    venda.adicionar_item(camisa, 1)
    venda.adicionar_item(copo, 2)
    
    # Testar propriedades
    print(f"ID da venda: {venda.id_venda}")
    print(f"Método de pagamento: {venda.metodo_pagamento}")
    print(f"Data/hora: {venda.data_hora}")
    print(f"Número de itens: {len(venda.itens)}")
    print(f"Valor total: R$ {venda.valor_total}")
    
    # Listar itens
    print("Itens da venda:")
    for item in venda.itens:
        print(f"  - {item.produto.nome}: {item.quantidade}x R$ {item.preco_unitario_momento} = R$ {item.subtotal}")
    
    # Finalizar venda
    total = venda.finalizar_venda()
    print(f"Venda finalizada. Total: R$ {total}")
    
    print("✅ Teste de venda concluído!\n")
    return venda

def teste_evento_festa(usuario, produtos, feedbacks):
    """Testa criação e funcionalidades da festa"""
    print("=== TESTE DE FESTA ===")
    
    cerveja, camisa, copo = produtos
    fb1, fb2 = feedbacks
    
    # Criar festa
    festa = Festa("Festa de Formatura", "2025-12-15", "Salão Central", 50.0)
    
    # Testar propriedades básicas
    print(f"Nome: {festa.nome}")
    print(f"Data: {festa.data}")
    print(f"Local: {festa.local}")
    print(f"Preço entrada: R$ {festa.preco_entrada}")
    
    # Adicionar produtos
    festa.adicionar_produto(cerveja)
    festa.adicionar_produto(camisa)
    festa.adicionar_produto(copo)
    print(f"Produtos adicionados: {len(festa.produtos)}")
    
    # Adicionar feedbacks
    festa.adicionar_feedback(fb1)
    festa.adicionar_feedback(fb2)
    print(f"Feedbacks adicionados: {len(festa.feedbacks)}")
    
    # Listar feedbacks
    feedbacks_lista = festa.listar_feedback()
    print("Feedbacks da festa:")
    for fb in feedbacks_lista:
        print(f"  - {fb.get_detalhes()}")
    
    # Testar realizar venda
    print("Realizando venda na festa...")
    venda_festa = festa.realizar_venda(usuario, {cerveja: 2, camisa: 1})
    print(f"Venda realizada. Total: R$ {venda_festa.valor_total}")
    
    # Testar faturamento
    faturamento = festa.get_faturamento_total()
    print(f"Faturamento total da festa: R$ {faturamento}")
    
    print("✅ Teste de festa concluído!\n")
    return festa

def teste_evento_happyhour(usuario, produtos):
    """Testa criação e funcionalidades do happy hour"""
    print("=== TESTE DE HAPPY HOUR ===")
    
    cerveja, camisa, copo = produtos
    
    # Criar happy hour
    hh = HappyHour("Happy Hour Sexta", "2025-10-25", "Bar do Campus", "18:00", "22:00", True, True)
    
    # Testar propriedades
    print(f"Nome: {hh.nome}")
    print(f"Data: {hh.data}")
    print(f"Local: {hh.local}")
    print(f"Horário: {hh.horario_inicio} às {hh.horario_fim}")
    print(f"É open bar? {hh.eh_open_bar}")
    print(f"Entrada gratuita? {hh.entrada_gratuita}")
    
    # Adicionar produtos
    hh.adicionar_produto(cerveja)
    hh.adicionar_produto(copo)
    print(f"Produtos adicionados: {len(hh.produtos)}")
    
    # Criar e registrar venda manual
    venda_hh = Venda(1, "dinheiro", datetime.now())
    venda_hh.adicionar_item(cerveja, 5)
    hh.registrar_venda(venda_hh)
    
    print(f"Venda registrada. Vendas totais: {len(hh.vendas)}")
    
    # Testar faturamento
    faturamento = hh.get_faturamento_total()
    print(f"Faturamento total do happy hour: R$ {faturamento}")
    
    print("✅ Teste de happy hour concluído!\n")
    return hh

def teste_sistema_ingressos(usuario, admin, festa):
    """Testa sistema completo de ingressos"""
    print("=== TESTE DE SISTEMA DE INGRESSOS ===")
    
    # Criar mais usuários para teste
    usuario2 = Usuario("54321", "Maria Santos", "maria@email.com", False)
    usuario3 = Usuario("98765", "Pedro Oliveira", "pedro@email.com", False)
    
    # Usuários comprando ingressos
    print("Comprando ingressos...")
    ingresso1 = usuario.comprar_ingresso(festa)
    ingresso2 = usuario2.comprar_ingresso(festa)
    ingresso3 = admin.comprar_ingresso(festa)
    
    print(f"Ingresso 1: {usuario.nome} - R$ {ingresso1.preco}")
    print(f"Ingresso 2: {usuario2.nome} - R$ {ingresso2.preco}")
    print(f"Ingresso 3: {admin.nome} - R$ {ingresso3.preco}")
    
    # Listar compradores
    print("\n--- Lista de Compradores ---")
    compradores = festa.listar_compradores_ingressos()
    for matricula, data_compra, preco in compradores:
        print(f"Matrícula: {matricula} | Data: {data_compra} | Preço: R$ {preco}")
    
    # Estatísticas do evento
    print(f"\nTotal de ingressos vendidos: {festa.obter_total_ingressos_vendidos()}")
    print(f"Receita dos ingressos: R$ {festa.obter_receita_ingressos()}")
    
    # Listar ingressos de um usuário específico
    print(f"\nIngressos do {usuario.nome}:")
    ingressos_usuario = usuario.listar_ingressos()
    for ing in ingressos_usuario:
        print(f"  - Evento: {ing.evento.nome} | Data compra: {ing.data_compra} | Preço: R$ {ing.preco}")
    
    print("✅ Teste de sistema de ingressos concluído!\n")
    return [usuario2, usuario3]

def teste_sistema_vendas_completo(usuario, festa, produtos):
    """Testa sistema completo de vendas de produtos"""
    print("=== TESTE DE SISTEMA DE VENDAS COMPLETO ===")
    
    cerveja, camisa, copo = produtos
    
    # Realizar várias vendas
    print("Realizando vendas...")
    
    # Venda 1
    venda1 = festa.realizar_venda(usuario, {cerveja: 2, copo: 1})
    print(f"Venda 1: R$ {venda1.valor_total}")
    
    # Venda 2 
    venda2 = festa.realizar_venda(usuario, {camisa: 1, cerveja: 1})
    print(f"Venda 2: R$ {venda2.valor_total}")
    
    # Listar todas as vendas da festa
    print("\n--- Todas as Vendas da Festa ---")
    vendas_festa = festa.listar_vendas()
    for i, venda in enumerate(vendas_festa, 1):
        print(f"Venda {i}: R$ {venda.valor_total} | {len(venda.itens)} itens | {venda.metodo_pagamento}")
    
    # Histórico de compras do usuário
    print(f"\n--- Histórico de Compras - {usuario.nome} ---")
    historico = usuario.ver_historico_compras()
    for i, compra in enumerate(historico, 1):
        print(f"Compra {i}: R$ {compra.valor_total} | Data: {compra.data_hora.strftime('%d/%m/%Y %H:%M')}")
    
    # Vendas por produto específico
    print(f"\n--- Vendas de {cerveja.nome} ---")
    vendas_cerveja = festa.obter_vendas_por_produto(cerveja)
    for venda, quantidade in vendas_cerveja:
        print(f"Venda ID {venda.id_venda}: {quantidade} unidades")
    
    print("✅ Teste de sistema de vendas completo concluído!\n")

def main():
    """Função principal que executa todos os testes"""
    print("🎉 INICIANDO TESTES COMPLETOS DO SISTEMA DE FESTAS 🎉\n")
    
    try:
        # Executar testes básicos
        produtos = teste_produtos()
        usuario, admin = teste_usuario()
        feedbacks = teste_feedback()
        venda = teste_venda(produtos)
        festa = teste_evento_festa(usuario, produtos, feedbacks)
        happyhour = teste_evento_happyhour(usuario, produtos)
        
        # Novos testes de funcionalidades completas
        usuarios_extras = teste_sistema_ingressos(usuario, admin, festa)
        teste_sistema_vendas_completo(usuario, festa, produtos)
        
        print("🎊 TODOS OS TESTES FORAM EXECUTADOS COM SUCESSO! 🎊")
        print("\nResumo final:")
        print(f"- Produtos testados: {len(produtos)}")
        print(f"- Usuários criados: {2 + len(usuarios_extras)}")
        print(f"- Feedbacks criados: {len(feedbacks)}")
        print(f"- Festa com faturamento: R$ {festa.get_faturamento_total()}")
        print(f"- Happy Hour com faturamento: R$ {happyhour.get_faturamento_total()}")
        print(f"- Ingressos vendidos na festa: {festa.obter_total_ingressos_vendidos()}")
        print(f"- Vendas de produtos na festa: {len(festa.listar_vendas())}")
        
    except Exception as e:
        print(f"❌ ERRO durante os testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
>>>>>>> 7b817db3fd467c57976c686791a8df80122fc8f2
