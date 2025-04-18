import pulp
import matplotlib.pyplot as plt
import networkx as nx

# Função para resolver o problema de clique máxima
def resolver_problema_clique(vertices, arestas):
    problema = pulp.LpProblem("Problema_Clique_Maxima", pulp.LpMaximize)

    x = {v: pulp.LpVariable(f"x_{v}", cat='Binary') for v in vertices}

    problema += pulp.lpSum(x[v] for v in vertices), "Maximizar_Clique"

    for v1 in vertices:
        for v2 in vertices:
            if v1 != v2 and (v1, v2) not in arestas and (v2, v1) not in arestas:
                problema += x[v1] + x[v2] <= 1, f"Restricao_{v1}_{v2}"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "vertices_clique": [v for v in vertices if x[v].varValue == 1],
        "tamanho_clique": pulp.value(problema.objective)
    }

    return resultado

# Função para plotar o grafo destacando a clique
def plotar_clique(vertices, arestas, vertices_clique, titulo):
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(arestas)

    color_map = ['lightgreen' if v in vertices_clique else 'lightblue' for v in G.nodes()]

    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color=color_map, node_size=2000)
    plt.title(titulo)
    plt.show()

# Exemplo 1: Dados do problema
vertices1 = ['A', 'B', 'C', 'D']
arestas1 = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'C')]

dados_clique1 = resolver_problema_clique(vertices1, arestas1)

print("\nProblema da Clique Máxima - Exemplo 1:")
print("Status:", dados_clique1["status"])
print("Vertices na clique:", dados_clique1["vertices_clique"])
print("Tamanho da clique:", dados_clique1["tamanho_clique"])
plotar_clique(vertices1, arestas1, dados_clique1['vertices_clique'], "Clique Máxima - Exemplo 1")

# Exemplo 2: Grafo maior e mais conectado
vertices2 = ['P', 'Q', 'R', 'S', 'T', 'U']
arestas2 = [('P', 'Q'), ('P', 'R'), ('Q', 'R'), ('Q', 'S'), ('R', 'S'), ('S', 'T'), ('T', 'U')]

dados_clique2 = resolver_problema_clique(vertices2, arestas2)

print("\nProblema da Clique Máxima - Exemplo 2:")
print("Status:", dados_clique2["status"])
print("Vertices na clique:", dados_clique2["vertices_clique"])
print("Tamanho da clique:", dados_clique2["tamanho_clique"])
plotar_clique(vertices2, arestas2, dados_clique2['vertices_clique'], "Clique Máxima - Exemplo 2")

# Exemplo 3: Grafo em estrutura de quase-clique
vertices3 = ['X', 'Y', 'Z', 'W', 'V']
arestas3 = [('X', 'Y'), ('X', 'Z'), ('X', 'W'), ('Y', 'Z'), ('Y', 'W'), ('Z', 'W'), ('W', 'V')]

dados_clique3 = resolver_problema_clique(vertices3, arestas3)

print("\nProblema da Clique Máxima - Exemplo 3:")
print("Status:", dados_clique3["status"])
print("Vertices na clique:", dados_clique3["vertices_clique"])
print("Tamanho da clique:", dados_clique3["tamanho_clique"])
plotar_clique(vertices3, arestas3, dados_clique3['vertices_clique'], "Clique Máxima - Exemplo 3")
