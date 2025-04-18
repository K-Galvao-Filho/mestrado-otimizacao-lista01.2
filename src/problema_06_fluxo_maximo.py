import pulp
import matplotlib.pyplot as plt
import networkx as nx

# Função para resolver o problema de fluxo máximo
def resolver_problema_fluxo_maximo(capacidades, origem, destino):
    problema = pulp.LpProblem("Problema_Fluxo_Maximo", pulp.LpMaximize)

    variaveis = {(u, v): pulp.LpVariable(f"x_{u}_{v}", lowBound=0) for u in capacidades for v in capacidades[u]}

    problema += pulp.lpSum(variaveis[(origem, v)] for v in capacidades[origem]), "Fluxo_Total"

    nos = set(capacidades.keys()).union({v for dests in capacidades.values() for v in dests})
    intermediarios = nos - {origem, destino}
    for nodo in intermediarios:
        problema += (pulp.lpSum(variaveis[(u, nodo)] for u in capacidades if nodo in capacidades[u]) ==
                     pulp.lpSum(variaveis[(nodo, v)] for v in capacidades.get(nodo, {}))), f"Conservacao_fluxo_{nodo}"

    for u in capacidades:
        for v in capacidades[u]:
            problema += variaveis[(u, v)] <= capacidades[u][v], f"Capacidade_{u}_{v}"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "fluxos": {(u, v): variaveis[(u, v)].varValue for u in capacidades for v in capacidades[u]},
        "fluxo_total": pulp.value(problema.objective)
    }

    return resultado

# Função para plotar o grafo de fluxo
def plotar_fluxo(dados, capacidades, titulo):
    G = nx.DiGraph()

    for (u, v), fluxo in dados['fluxos'].items():
        if fluxo > 0:
            G.add_edge(u, v, label=f"{fluxo:.0f}/{capacidades[u][v]}")

    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_edge_attributes(G, 'label')

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, arrows=True, node_size=2500, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title(titulo)
    plt.axis('off')
    plt.show()

# Exemplo 1: Dados corrigidos conforme a apostila
capacidades1 = {
    's': {'a': 20, 'b': 10},
    'a': {'b': 5, 't': 10},
    'b': {'t': 20}
}

origem1 = 's'
destino1 = 't'

dados_fluxo1 = resolver_problema_fluxo_maximo(capacidades1, origem1, destino1)

print("\nProblema do Fluxo Máximo - Exemplo 1:")
print("Status:", dados_fluxo1["status"])
for (u, v), fluxo in dados_fluxo1["fluxos"].items():
    if fluxo > 0:
        print(f"Fluxo de {u} para {v}: {fluxo:.0f}")
print("Fluxo Total: ", dados_fluxo1["fluxo_total"])
plotar_fluxo(dados_fluxo1, capacidades1, "Fluxo Máximo na Rede - Exemplo 1")

# Exemplo 2: Novo conjunto de dados
capacidades2 = {
    's': {'a': 15, 'b': 10},
    'a': {'c': 10},
    'b': {'c': 5, 't': 10},
    'c': {'t': 10}
}

origem2 = 's'
destino2 = 't'

dados_fluxo2 = resolver_problema_fluxo_maximo(capacidades2, origem2, destino2)

print("\nProblema do Fluxo Máximo - Exemplo 2:")
print("Status:", dados_fluxo2["status"])
for (u, v), fluxo in dados_fluxo2["fluxos"].items():
    if fluxo > 0:
        print(f"Fluxo de {u} para {v}: {fluxo:.0f}")
print("Fluxo Total: ", dados_fluxo2["fluxo_total"])
plotar_fluxo(dados_fluxo2, capacidades2, "Fluxo Máximo na Rede - Exemplo 2")

# Exemplo 3: Outro conjunto novo
capacidades3 = {
    's': {'a': 25, 'b': 15},
    'a': {'c': 10, 'd': 10},
    'b': {'d': 5, 'e': 10},
    'c': {'t': 10},
    'd': {'t': 15},
    'e': {'t': 10}
}

origem3 = 's'
destino3 = 't'

dados_fluxo3 = resolver_problema_fluxo_maximo(capacidades3, origem3, destino3)

print("\nProblema do Fluxo Máximo - Exemplo 3:")
print("Status:", dados_fluxo3["status"])
for (u, v), fluxo in dados_fluxo3["fluxos"].items():
    if fluxo > 0:
        print(f"Fluxo de {u} para {v}: {fluxo:.0f}")
print("Fluxo Total: ", dados_fluxo3["fluxo_total"])
plotar_fluxo(dados_fluxo3, capacidades3, "Fluxo Máximo na Rede - Exemplo 3")
