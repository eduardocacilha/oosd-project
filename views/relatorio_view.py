from typing import List
import PySimpleGUI as sg

class RelatorioView:
    
    def tela_opcoes(self) -> int:
        print("\n======== MENU RELATORIOS ========")
        print("1 - Relatorios de Eventos")
        print("2 - Relatorios de Produtos")
        print("3 - Relatorios de Vendas")
        print("4 - Relatorios de Usuarios")
        print("0 - Retornar ao Menu Principal")
        
        try:
            return int(input("Escolha a opcao: "))
        except ValueError:
            return -1

    def tela_opcoes_eventos(self) -> int:
        print("\n-------- RELATORIOS DE EVENTOS ----------")
        print("1 - Eventos Mais Caros e Mais Baratos")
        print("2 - Eventos com Melhores Avaliacoes")
        print("3 - Eventos com Mais Ingressos Vendidos")
        print("4 - Ranking Completo de Eventos")
        print("0 - Voltar")
        
        try:
            return int(input("Escolha a opcao: "))
        except ValueError:
            return -1

    def tela_opcoes_produtos(self) -> int:
        print("\n-------- RELATORIOS DE PRODUTOS ----------")
        print("1 - Produtos Mais Caros e Mais Baratos")
        print("2 - Produtos Mais Vendidos")
        print("3 - Produtos com Maior Faturamento")
        print("4 - Relatorio de Estoque")
        print("5 - Ranking Completo de Produtos")
        print("0 - Voltar")
        
        try:
            return int(input("Escolha a opcao: "))
        except ValueError:
            return -1

    def tela_opcoes_vendas(self) -> int:
        print("\n-------- RELATORIOS DE VENDAS ----------")
        print("1 - Vendas por Metodo de Pagamento")
        print("2 - Faturamento por Evento")
        print("3 - Vendas por Periodo")
        print("4 - Top Clientes")
        print("0 - Voltar")
        
        try:
            return int(input("Escolha a opcao: "))
        except ValueError:
            return -1

    def tela_opcoes_usuarios(self) -> int:
        print("\n-------- RELATORIOS DE USUARIOS ----------")
        print("1 - Usuarios que Mais Gastaram")
        print("2 - Usuarios Mais Ativos")
        print("3 - Usuarios por Quantidade de Ingressos")
        print("0 - Voltar")
        
        try:
            return int(input("Escolha a opcao: "))
        except ValueError:
            return -1

    def mostra_eventos_preco(self, mais_caros: List[dict], mais_baratos: List[dict]):
        print("\n======== EVENTOS POR PRECO ========")
        
        print("\nEVENTOS MAIS CAROS:")
        if mais_caros:
            for i, evento in enumerate(mais_caros, 1):
                print(f"{i}. {evento['nome']} - R$ {evento['preco']:.2f}")
                print(f"   Data: {evento['data']} Local: {evento['local']}")
        else:
            print("Nenhum evento cadastrado.")
        
        print("\nEVENTOS MAIS BARATOS:")
        if mais_baratos:
            for i, evento in enumerate(mais_baratos, 1):
                print(f"{i}. {evento['nome']} - R$ {evento['preco']:.2f}")
                print(f"   Data: {evento['data']} Local: {evento['local']}")
        else:
            print("Nenhum evento cadastrado.")

    def mostra_eventos_avaliacao(self, eventos: List[dict]):
        print("\n======== EVENTOS MAIS BEM AVALIADOS ========")
        
        if not eventos:
            print("Nenhum evento com avaliacoes encontrado.")
            return
        
        for i, evento in enumerate(eventos, 1):
            print(f"{i}. {evento['nome']} - {evento['nota_media']:.1f}/5.0")
            print(f"   {evento['total_avaliacoes']} avaliacoes")
            print(f"   Data: {evento['data']} Local: {evento['local']}")
            print(f"   R$ {evento['preco']:.2f}")
            print()

    def mostra_eventos_vendas(self, eventos: List[dict]):
        print("\n======== EVENTOS COM MAIS INGRESSOS VENDIDOS ========")
        
        if not eventos:
            print("Nenhuma venda de ingresso encontrada.")
            return
        
        for i, evento in enumerate(eventos, 1):
            print(f"{i}. {evento['nome']} - {evento['ingressos_vendidos']} ingressos")
            print(f"   Faturamento: R$ {evento['faturamento']:.2f}")
            print(f"   Data: {evento['data']} Local: {evento['local']}")
            print()

    def mostra_ranking_eventos(self, eventos: List[dict]):
        print("\n======== RANKING COMPLETO DE EVENTOS ========")
        
        if not eventos:
            print("Nenhum evento cadastrado.")
            return
        
        for i, evento in enumerate(eventos, 1):
            nota_str = f"{evento['nota_media']:.1f}" if evento['nota_media'] > 0 else "Sem avaliacoes"
            print(f"{i}. {evento['nome']}")
            print(f"   {nota_str} | {evento['ingressos_vendidos']} ingressos | R$ {evento['faturamento']:.2f}")
            print(f"   Data: {evento['data']} Local: {evento['local']} | Preco: R$ {evento['preco']:.2f}")
            print()

    def mostra_produtos_preco(self, mais_caros: List[dict], mais_baratos: List[dict]):
        print("\n======== PRODUTOS POR PRECO ========")
        
        print("\nPRODUTOS MAIS CAROS:")
        if mais_caros:
            for i, produto in enumerate(mais_caros, 1):
                print(f"{i}. {produto['nome']} - R$ {produto['preco']:.2f}")
                print(f"   Estoque: {produto['estoque']} | Evento: {produto['evento']}")
        else:
            print("Nenhum produto cadastrado.")
        
        print("\nPRODUTOS MAIS BARATOS:")
        if mais_baratos:
            for i, produto in enumerate(mais_baratos, 1):
                print(f"{i}. {produto['nome']} - R$ {produto['preco']:.2f}")
                print(f"   Estoque: {produto['estoque']} | Evento: {produto['evento']}")
        else:
            print("Nenhum produto cadastrado.")

    def mostra_produtos_vendidos(self, produtos: List[dict]):
        print("\n======== PRODUTOS MAIS VENDIDOS ========")
        
        if not produtos:
            print("Nenhuma venda de produto encontrada.")
            return
        
        for i, produto in enumerate(produtos, 1):
            print(f"{i}. {produto['nome']} - {produto['quantidade_vendida']} unidades")
            print(f"   Faturamento: R$ {produto['faturamento']:.2f}")
            print(f"   Estoque atual: {produto['estoque']}")
            print()

    def mostra_produtos_faturamento(self, produtos: List[dict]):
        print("\n======== PRODUTOS COM MAIOR FATURAMENTO ========")
        
        if not produtos:
            print("Nenhuma venda de produto encontrada.")
            return
        
        for i, produto in enumerate(produtos, 1):
            print(f"{i}. {produto['nome']} - R$ {produto['faturamento']:.2f}")
            print(f"   {produto['quantidade_vendida']} unidades vendidas")
            print(f"   Preco unitario: R$ {produto['preco']:.2f}")
            print()

    def mostra_relatorio_estoque(self, produtos: List[dict]):
        print("\n======== RELATORIO DE ESTOQUE ========")
        
        if not produtos:
            print("Nenhum produto cadastrado.")
            return
        
        print("PRODUTOS COM ESTOQUE BAIXO (<=5):")
        estoque_baixo = [p for p in produtos if p['estoque'] <= 5]
        if estoque_baixo:
            for produto in estoque_baixo:
                print(f"  {produto['nome']} - {produto['estoque']} unidades")
        else:
            print("Nenhum produto com estoque baixo.")
        
        print("\nPRODUTOS COM BOM ESTOQUE (>5):")
        bom_estoque = [p for p in produtos if p['estoque'] > 5]
        if bom_estoque:
            for produto in bom_estoque:
                print(f"{produto['nome']} - {produto['estoque']} unidades")
        else:
            print("Nenhum produto com bom estoque.")

    def mostra_vendas_pagamento(self, dados: dict):
        print("\n======== VENDAS POR METODO DE PAGAMENTO ========")
        
        total_geral = sum(dados.values())
        
        for metodo, valor in dados.items():
            percentual = (valor / total_geral * 100) if total_geral > 0 else 0
            print(f"{metodo}: R$ {valor:.2f} ({percentual:.1f}%)")
        
        print(f"\nTOTAL GERAL: R$ {total_geral:.2f}")

    def mostra_faturamento_evento(self, eventos: List[dict]):
        print("\n======== FATURAMENTO POR EVENTO ========")
        
        if not eventos:
            print("Nenhuma venda encontrada.")
            return
        
        total_sistema = 0
        for i, evento in enumerate(eventos, 1):
            faturamento_total = evento['faturamento_ingressos'] + evento['faturamento_produtos']
            total_sistema += faturamento_total
            
            print(f"{i}. {evento['nome']}")
            print(f"   Ingressos: R$ {evento['faturamento_ingressos']:.2f}")
            print(f"   Produtos: R$ {evento['faturamento_produtos']:.2f}")
            print(f"   TOTAL: R$ {faturamento_total:.2f}")
            print()
        
        print(f"FATURAMENTO TOTAL DO SISTEMA: R$ {total_sistema:.2f}")

    def mostra_top_clientes(self, clientes: List[dict]):
        print("\n======== TOP CLIENTES ========")
        
        if not clientes:
            print("Nenhuma compra encontrada.")
            return
        
        for i, cliente in enumerate(clientes, 1):
            print(f"{i}. {cliente['nome']} (Mat: {cliente['matricula']})")
            print(f"   Total gasto: R$ {cliente['total_gasto']:.2f}")
            print(f"   Ingressos: {cliente['ingressos_comprados']}")
            print(f"   Produtos: {cliente['produtos_comprados']} itens")
            print()

    def mostra_relatorio_geral(self, dados: dict):
        print("\n======== RELATORIO GERAL DO SISTEMA ========")
        
        print(f"ESTATISTICAS GERAIS:")
        print(f"   Usuarios cadastrados: {dados['total_usuarios']}")
        print(f"   Eventos cadastrados: {dados['total_eventos']}")
        print(f"   Produtos cadastrados: {dados['total_produtos']}")
        print(f"   Ingressos vendidos: {dados['total_ingressos_vendidos']}")
        print(f"   Itens de produtos vendidos: {dados['total_produtos_vendidos']}")
        
        print(f"\nFATURAMENTO:")
        print(f"   Ingressos: R$ {dados['faturamento_ingressos']:.2f}")
        print(f"   Produtos: R$ {dados['faturamento_produtos']:.2f}")
        print(f"   TOTAL: R$ {dados['faturamento_total']:.2f}")
        
        if dados.get('evento_mais_popular'):
            print(f"\nDESTAQUES:")
            print(f"   Evento mais popular: {dados['evento_mais_popular']}")
            print(f"   Produto mais vendido: {dados['produto_mais_vendido']}")
            print(f"   Melhor cliente: {dados['melhor_cliente']}")

    def mostra_mensagem(self, msg: str):
        print(f"\n{msg}\n")