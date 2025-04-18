import pulp
import matplotlib.pyplot as plt
import networkx as nx

# Função para resolver o problema de frequências (coloração de grafos)
def resolver_problema_frequencia(vertices, arestas, cores):
    problema = pulp.LpProblem("Problema_Frequencia", pulp.LpMinimize)

    x = {(v, c): pulp.LpVariable(f"x_{v}_{c}", cat='Binary') for v in vertices for c in cores}
    y = {c: pulp.LpVariable(f"y_{c}", cat='Binary') for c in cores}

    problema += pulp.lpSum(y[c] for c in cores), "Minimizar_numero_frequencias"

    for v in vertices:
        problema += pulp.lpSum(x[(v, c)] for c in cores) == 1, f"Uma_frequencia_para_{v}"

    for (v1, v2) in arestas:
        for c in cores:
            problema += x[(v1, c)] + x[(v2, c)] <= 1, f"Aresta_{v1}_{v2}_cor_{c}"

    for v in vertices:
        for c in cores:
            problema += x[(v, c)] <= y[c], f"Ativar_cor_{c}_se_usada_por_{v}"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "cores_usadas": {v: c for v in vertices for c in cores if x[(v, c)].varValue == 1},
        "total_cores": pulp.value(problema.objective)
    }

    return resultado

# Função para plotar o grafo colorido
def plotar_frequencia(vertices, arestas, cores_usadas, titulo):
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(arestas)

    color_map = []
    cores_disponiveis = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta']
    cor_vertex = {v: cores_disponiveis[cores_usadas[v]] for v in vertices}

    for v in G.nodes():
        color_map.append(cor_vertex[v])

    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color=color_map, node_size=2000)
    plt.title(titulo)
    plt.show()

# Exemplo 1: Dados do problema
vertices1 = ['A', 'B', 'C', 'D']
arestas1 = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
cores1 = [0, 1, 2, 3]

dados_frequencia1 = resolver_problema_frequencia(vertices1, arestas1, cores1)

print("\nProblema de Frequencias - Exemplo 1:")
print("Status:", dados_frequencia1["status"])
print("Atribuição de cores:", dados_frequencia1["cores_usadas"])
print("Total de cores usadas:", dados_frequencia1["total_cores"])
plotar_frequencia(vertices1, arestas1, dados_frequencia1['cores_usadas'], "Coloração de Grafos - Exemplo 1")

# Exemplo 2: Mais vértices e conexões complexas
vertices2 = ['A', 'B', 'C', 'D', 'E', 'F']
arestas2 = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'F')]
cores2 = [0, 1, 2, 3, 4]

dados_frequencia2 = resolver_problema_frequencia(vertices2, arestas2, cores2)

print("\nProblema de Frequencias - Exemplo 2:")
print("Status:", dados_frequencia2["status"])
print("Atribuição de cores:", dados_frequencia2["cores_usadas"])
print("Total de cores usadas:", dados_frequencia2["total_cores"])
plotar_frequencia(vertices2, arestas2, dados_frequencia2['cores_usadas'], "Coloração de Grafos - Exemplo 2")

# Exemplo 3: Estrutura de grafo em ciclo
vertices3 = ['P', 'Q', 'R', 'S', 'T']
arestas3 = [('P', 'Q'), ('Q', 'R'), ('R', 'S'), ('S', 'T'), ('T', 'P')]
cores3 = [0, 1, 2, 3]

dados_frequencia3 = resolver_problema_frequencia(vertices3, arestas3, cores3)

print("\nProblema de Frequencias - Exemplo 3:")
print("Status:", dados_frequencia3["status"])
print("Atribuição de cores:", dados_frequencia3["cores_usadas"])
print("Total de cores usadas:", dados_frequencia3["total_cores"])
plotar_frequencia(vertices3, arestas3, dados_frequencia3['cores_usadas'], "Coloração de Grafos - Exemplo 3")