# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização linear
import matplotlib.pyplot as plt  # Para criar gráficos
import networkx as nx  # Para criar e visualizar redes de transporte

# Função que calcula a quantidade de produtos a transportar de fábricas para depósitos com menor custo
def resolver_problema_transporte(custos, ofertas, demandas):
    # Cria um problema para minimizar o custo total de transporte
    problema = pulp.LpProblem("Problema_Transporte", pulp.LpMinimize)

    # Dicionário para armazenar variáveis de decisão
    variaveis = {}
    fabricas = list(custos.keys())  # Lista de fábricas
    depositos = list(next(iter(custos.values())).keys())  # Lista de depósitos

    # Cria variáveis: quantidade a transportar de cada fábrica para cada depósito (não negativa)
    for f in fabricas:
        for d in depositos:
            variaveis[(f, d)] = pulp.LpVariable(f"x_{f}_{d}", lowBound=0)

    # Define o objetivo: minimizar o custo total (custo por unidade * quantidade transportada)
    problema += pulp.lpSum(custos[f][d] * variaveis[(f, d)] for f in fabricas for d in depositos), "Custo_Total"

    # Restrições: cada fábrica não pode enviar mais do que sua oferta
    for f in fabricas:
        problema += pulp.lpSum(variaveis[(f, d)] for d in depositos) <= ofertas[f], f"Oferta_{f}"

    # Restrições: cada depósito deve receber pelo menos sua demanda
    for d in depositos:
        problema += pulp.lpSum(variaveis[(f, d)] for f in fabricas) >= demandas[d], f"Demanda_{d}"

    # Resolve o problema
    problema.solve()

    # Organiza os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "quantidades": {(f, d): variaveis[(f, d)].varValue for f in fabricas for d in depositos},  # Quantidade transportada
        "custo_total": pulp.value(problema.objective)  # Custo total
    }

    return resultado  # Retorna os resultados

# Função para criar um gráfico de rede mostrando o transporte
def plotar_transporte(dados, titulo):
    G = nx.DiGraph()  # Cria um grafo direcionado
    fabricas = sorted(set(f for f, d in dados['quantidades'].keys()))  # Lista de fábricas
    depositos = sorted(set(d for f, d in dados['quantidades'].keys()))  # Lista de depósitos

    # Define posições dos nós (fábricas à esquerda, depósitos à direita)
    pos = {}
    for i, f in enumerate(fabricas):
        pos[f"Fábrica {f}"] = (0, -i)
    for j, d in enumerate(depositos):
        pos[f"Depósito {d}"] = (2, -j)

    # Adiciona arestas ao grafo para quantidades transportadas maiores que zero
    for (f, d), valor in dados['quantidades'].items():
        if valor > 0:
            G.add_edge(f"Fábrica {f}", f"Depósito {d}", weight=valor)

    edge_labels = nx.get_edge_attributes(G, 'weight')  # Rótulos com quantidades
    plt.figure(figsize=(10, 6))  # Define tamanho da figura
    # Desenha o grafo com nós, arestas e rótulos
    nx.draw(G, pos, with_labels=True, arrows=True, connectionstyle='arc3,rad=0.1', node_size=3000, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d:.0f}" for (u, v), d in edge_labels.items()}, font_size=10)
    plt.title(titulo)  # Título do gráfico
    plt.axis('off')  # Remove os eixos
    plt.show()  # Exibe o gráfico

# Função para executar e exibir resultados de um exemplo
def executar_exemplo(custos, ofertas, demandas, titulo):
    dados = resolver_problema_transporte(custos, ofertas, demandas)  # Resolve o problema
    print(f"\n{titulo}:")
    print("Status:", dados["status"])  # Status da solução
    for chave, valor in dados["quantidades"].items():
        print(f"Quantidade de Fábrica {chave[0]} para Depósito {chave[1]}: {valor:.2f}")  # Quantidades transportadas
    print("Custo Total: R$", dados["custo_total"])  # Custo total
    plotar_transporte(dados, titulo)  # Mostra o gráfico

# Exemplo 1: Configuração inicial
custos1 = {1: {1: 8, 2: 5, 3: 6}, 2: {1: 15, 2: 10, 3: 12}, 3: {1: 3, 2: 9, 3: 10}}  # Custos de transporte
ofertas1 = {1: 120, 2: 80, 3: 80}  # Oferta de cada fábrica
demandas1 = {1: 70, 2: 60, 3: 150}  # Demanda de cada depósito
executar_exemplo(custos1, ofertas1, demandas1, "Problema do Transporte - Exemplo 1")

# Exemplo 2: Custos, ofertas e demandas modificados
custos2 = {1: {1: 7, 2: 6, 3: 8}, 2: {1: 12, 2: 9, 3: 11}, 3: {1: 4, 2: 7, 3: 9}}  # Novos custos
ofertas2 = {1: 50, 2: 90, 3: 190}  # Novas ofertas
demandas2 = {1: 80, 2: 70, 3: 130}  # Novas demandas
executar_exemplo(custos2, ofertas2, demandas2, "Problema do Transporte - Exemplo 2")

# Exemplo 3: Outro conjunto de dados
custos3 = {1: {1: 9, 2: 7, 3: 5}, 2: {1: 14, 2: 11, 3: 13}, 3: {1: 5, 2: 8, 3: 6}}  # Novos custos
ofertas3 = {1: 70, 2: 90, 3: 50}  # Novas ofertas
demandas3 = {1: 90, 2: 60, 3: 140}  # Novas demandas
executar_exemplo(custos3, ofertas3, demandas3, "Problema do Transporte - Exemplo 3")