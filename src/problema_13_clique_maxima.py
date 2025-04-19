# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização linear
import matplotlib.pyplot as plt  # Para criar gráficos
import networkx as nx  # Para criar e visualizar grafos

# Função que encontra a maior clique em um grafo
def resolver_problema_clique(vertices, arestas):
    # Cria um problema para maximizar o tamanho da clique
    problema = pulp.LpProblem("Problema_Clique_Maxima", pulp.LpMaximize)

    # Variáveis binárias: x[v] = 1 se o vértice v está na clique, 0 caso contrário
    x = {v: pulp.LpVariable(f"x_{v}", cat='Binary') for v in vertices}

    # Define o objetivo: maximizar o número de vértices na clique
    problema += pulp.lpSum(x[v] for v in vertices), "Maximizar_Clique"

    # Restrições: vértices não conectados por uma aresta não podem estar na mesma clique
    for v1 in vertices:
        for v2 in vertices:
            if v1 != v2 and (v1, v2) not in arestas and (v2, v1) not in arestas:
                problema += x[v1] + x[v2] <= 1, f"Restricao_{v1}_{v2}"

    # Resolve o problema
    problema.solve()

    # Organiza os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "vertices_clique": [v for v in vertices if x[v].varValue == 1],  # Vértices na clique
        "tamanho_clique": pulp.value(problema.objective)  # Tamanho da clique
    }

    return resultado  # Retorna os resultados

# Função para criar um grafo destacando os vértices da clique
def plotar_clique(vertices, arestas, vertices_clique, titulo):
    G = nx.Graph()  # Cria um grafo não direcionado
    G.add_nodes_from(vertices)  # Adiciona os vértices
    G.add_edges_from(arestas)  # Adiciona as arestas

    # Define cores: verde para vértices na clique, azul para os demais
    color_map = ['lightgreen' if v in vertices_clique else 'lightblue' for v in G.nodes()]

    plt.figure(figsize=(8, 6))  # Define tamanho da figura
    nx.draw(G, with_labels=True, node_color=color_map, node_size=2000)  # Desenha o grafo
    plt.title(titulo)  # Título do gráfico
    plt.show()  # Exibe o gráfico

# Exemplo 1: Configuração inicial
vertices1 = ['A', 'B', 'C', 'D']  # Vértices do grafo
arestas1 = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'C')]  # Arestas do grafo

dados_clique1 = resolver_problema_clique(vertices1, arestas1)

print("\nProblema da Clique Máxima - Exemplo 1:")
print("Status:", dados_clique1["status"])  # Status da solução
print("Vertices na clique:", dados_clique1["vertices_clique"])  # Vértices selecionados
print("Tamanho da clique:", dados_clique1["tamanho_clique"])  # Tamanho da clique
plotar_clique(vertices1, arestas1, dados_clique1['vertices_clique'], "Clique Máxima - Exemplo 1")  # Mostra o gráfico

# Exemplo 2: Grafo maior e mais conectado
vertices2 = ['P', 'Q', 'R', 'S', 'T', 'U']  # Vértices do grafo
arestas2 = [('P', 'Q'), ('P', 'R'), ('Q', 'R'), ('Q', 'S'), ('R', 'S'), ('S', 'T'), ('T', 'U')]  # Arestas do grafo

dados_clique2 = resolver_problema_clique(vertices2, arestas2)

print("\nProblema da Clique Máxima - Exemplo 2:")
print("Status:", dados_clique2["status"])
print("Vertices na clique:", dados_clique2["vertices_clique"])
print("Tamanho da clique:", dados_clique2["tamanho_clique"])
plotar_clique(vertices2, arestas2, dados_clique2['vertices_clique'], "Clique Máxima - Exemplo 2")

# Exemplo 3: Grafo com estrutura de quase-clique
vertices3 = ['X', 'Y', 'Z', 'W', 'V']  # Vértices do grafo
arestas3 = [('X', 'Y'), ('X', 'Z'), ('X', 'W'), ('Y', 'Z'), ('Y', 'W'), ('Z', 'W'), ('W', 'V')]  # Arestas do grafo

dados_clique3 = resolver_problema_clique(vertices3, arestas3)

print("\nProblema da Clique Máxima - Exemplo 3:")
print("Status:", dados_clique3["status"])
print("Vertices na clique:", dados_clique3["vertices_clique"])
print("Tamanho da clique:", dados_clique3["tamanho_clique"])
plotar_clique(vertices3, arestas3, dados_clique3['vertices_clique'], "Clique Máxima - Exemplo 3")