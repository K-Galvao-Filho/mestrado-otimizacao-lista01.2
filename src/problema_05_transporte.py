import pulp
import matplotlib.pyplot as plt
import networkx as nx

def resolver_problema_transporte(custos, ofertas, demandas):
    problema = pulp.LpProblem("Problema_Transporte", pulp.LpMinimize)

    variaveis = {}
    fabricas = list(custos.keys())
    depositos = list(next(iter(custos.values())).keys())

    for f in fabricas:
        for d in depositos:
            variaveis[(f, d)] = pulp.LpVariable(f"x_{f}_{d}", lowBound=0)

    problema += pulp.lpSum(custos[f][d] * variaveis[(f, d)] for f in fabricas for d in depositos), "Custo_Total"

    for f in fabricas:
        problema += pulp.lpSum(variaveis[(f, d)] for d in depositos) <= ofertas[f], f"Oferta_{f}"

    for d in depositos:
        problema += pulp.lpSum(variaveis[(f, d)] for f in fabricas) >= demandas[d], f"Demanda_{d}"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "quantidades": {(f, d): variaveis[(f, d)].varValue for f in fabricas for d in depositos},
        "custo_total": pulp.value(problema.objective)
    }

    return resultado

def plotar_transporte(dados, titulo):
    G = nx.DiGraph()
    fabricas = sorted(set(f for f, d in dados['quantidades'].keys()))
    depositos = sorted(set(d for f, d in dados['quantidades'].keys()))

    pos = {}
    for i, f in enumerate(fabricas):
        pos[f"Fábrica {f}"] = (0, -i)
    for j, d in enumerate(depositos):
        pos[f"Depósito {d}"] = (2, -j)

    for (f, d), valor in dados['quantidades'].items():
        if valor > 0:
            G.add_edge(f"Fábrica {f}", f"Depósito {d}", weight=valor)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, arrows=True, connectionstyle='arc3,rad=0.1', node_size=3000, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d:.0f}" for (u, v), d in edge_labels.items()}, font_size=10)
    plt.title(titulo)
    plt.axis('off')
    plt.show()

# Função para executar um exemplo
def executar_exemplo(custos, ofertas, demandas, titulo):
    dados = resolver_problema_transporte(custos, ofertas, demandas)
    print(f"\n{titulo}:")
    print("Status:", dados["status"])
    for chave, valor in dados["quantidades"].items():
        print(f"Quantidade de Fábrica {chave[0]} para Depósito {chave[1]}: {valor:.2f}")
    print("Custo Total: R$", dados["custo_total"])
    plotar_transporte(dados, titulo)

# Exemplo 1: Dados originais
custos1 = {1: {1: 8, 2: 5, 3: 6}, 2: {1: 15, 2: 10, 3: 12}, 3: {1: 3, 2: 9, 3: 10}}
ofertas1 = {1: 120, 2: 80, 3: 80}
demandas1 = {1: 70, 2: 60, 3: 150}
executar_exemplo(custos1, ofertas1, demandas1, "Problema do Transporte - Exemplo 1")

# Exemplo 2: Dados modificados
custos2 = {1: {1: 7, 2: 6, 3: 8}, 2: {1: 12, 2: 9, 3: 11}, 3: {1: 4, 2: 7, 3: 9}}
ofertas2 = {1: 50, 2: 90, 3: 190}
demandas2 = {1: 80, 2: 70, 3: 130}
executar_exemplo(custos2, ofertas2, demandas2, "Problema do Transporte - Exemplo 2")

# Exemplo 3: Outro conjunto de dados
custos3 = {1: {1: 9, 2: 7, 3: 5}, 2: {1: 14, 2: 11, 3: 13}, 3: {1: 5, 2: 8, 3: 6}}
ofertas3 = {1: 70, 2: 90, 3: 50}
demandas3 = {1: 90, 2: 60, 3: 140}
executar_exemplo(custos3, ofertas3, demandas3, "Problema do Transporte - Exemplo 3")
