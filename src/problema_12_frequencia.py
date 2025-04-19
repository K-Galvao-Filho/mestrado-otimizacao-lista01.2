# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização linear
import matplotlib.pyplot as plt  # Para criar gráficos
import networkx as nx  # Para criar e visualizar grafos

# Função que resolve o problema de coloração de grafos (atribuição de frequências)
def resolver_problema_frequencia(vertices, arestas, cores):
    # Cria um problema para minimizar o número de cores usadas
    problema = pulp.LpProblem("Problema_Frequencia", pulp.LpMinimize)

    # Variáveis binárias: x[v,c] = 1 se o vértice v usa a cor c, 0 caso contrário
    x = {(v, c): pulp.LpVariable(f"x_{v}_{c}", cat='Binary') for v in vertices for c in cores}
    # Variáveis binárias: y[c] = 1 se a cor c é usada, 0 caso contrário
    y = {c: pulp.LpVariable(f"y_{c}", cat='Binary') for c in cores}

    # Define o objetivo: minimizar o número de cores usadas
    problema += pulp.lpSum(y[c] for c in cores), "Minimizar_numero_frequencias"

    # Restrições: cada vértice deve receber exatamente uma cor
    for v in vertices:
        problema += pulp.lpSum(x[(v, c)] for c in cores) == 1, f"Uma_frequencia_para_{v}"

    # Restrições: vértices adjacentes não podem ter a mesma cor
    for (v1, v2) in arestas:
        for c in cores:
            problema += x[(v1, c)] + x[(v2, c)] <= 1, f"Aresta_{v1}_{v2}_cor_{c}"

    # Restrições: uma cor só é considerada usada se pelo menos um vértice a utiliza
    for v in vertices:
        for c in cores:
            problema += x[(v, c)] <= y[c], f"Ativar_cor_{c}_se_usada_por_{v}"

    # Resolve o problema
    problema.solve()

    # Organiza os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "cores_usadas": {v: c for v in vertices for c in cores if x[(v, c)].varValue == 1},  # Atribuição de cores
        "total_cores": pulp.value(problema.objective)  # Número total de cores usadas
    }

    return resultado  # Retorna os resultados

# Função para criar um grafo colorido mostrando a atribuição de cores
def plotar_frequencia(vertices, arestas, cores_usadas, titulo):
    G = nx.Graph()  # Cria um grafo não direcionado
    G.add_nodes_from(vertices)  # Adiciona os vértices
    G.add_edges_from(arestas)  # Adiciona as arestas

    # Define uma lista de cores disponíveis para visualização
    cores_disponiveis = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta']
    # Mapeia cada vértice para sua cor correspondente
    cor_vertex = {v: cores_disponiveis[cores_usadas[v]] for v in vertices}
    color_map = [cor_vertex[v] for v in G.nodes()]  # Lista de cores para os nós

    plt.figure(figsize=(8, 6))  # Define tamanho da figura
    nx.draw(G, with_labels=True, node_color=color_map, node_size=2000)  # Desenha o grafo
    plt.title(titulo)  # Título do gráfico
    plt.show()  # Exibe o gráfico

# Exemplo 1: Configuração inicial
vertices1 = ['A', 'B', 'C', 'D']  # Vértices do grafo
arestas1 = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]  # Arestas do grafo
cores1 = [0, 1, 2, 3]  # Cores disponíveis (representadas por índices)

dados_frequencia1 = resolver_problema_frequencia(vertices1, arestas1, cores1)

print("\nProblema de Frequencias - Exemplo 1:")
print("Status:", dados_frequencia1["status"])  # Status da solução
print("Atribuição de cores:", dados_frequencia1["cores_usadas"])  # Cores atribuídas a cada vértice
print("Total de cores usadas:", dados_frequencia1["total_cores"])  # Número de cores usadas
plotar_frequencia(vertices1, arestas1, dados_frequencia1['cores_usadas'], "Coloração de Grafos - Exemplo 1")  # Mostra o gráfico

# Exemplo 2: Grafo com mais vértices e conexões complexas
vertices2 = ['A', 'B', 'C', 'D', 'E', 'F']  # Vértices do grafo
arestas2 = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'F')]  # Arestas do grafo
cores2 = [0, 1, 2, 3, 4]  # Cores disponíveis

dados_frequencia2 = resolver_problema_frequencia(vertices2, arestas2, cores2)

print("\nProblema de Frequencias - Exemplo 2:")
print("Status:", dados_frequencia2["status"])
print("Atribuição de cores:", dados_frequencia2["cores_usadas"])
print("Total de cores usadas:", dados_frequencia2["total_cores"])
plotar_frequencia(vertices2, arestas2, dados_frequencia2['cores_usadas'], "Coloração de Grafos - Exemplo 2")

# Exemplo 3: Grafo em forma de ciclo
vertices3 = ['P', 'Q', 'R', 'S', 'T']  # Vértices do grafo
arestas3 = [('P', 'Q'), ('Q', 'R'), ('R', 'S'), ('S', 'T'), ('T', 'P')]  # Arestas formando um ciclo
cores3 = [0, 1, 2, 3]  # Cores disponíveis

dados_frequencia3 = resolver_problema_frequencia(vertices3, arestas3, cores3)

print("\nProblema de Frequencias - Exemplo 3:")
print("Status:", dados_frequencia3["status"])
print("Atribuição de cores:", dados_frequencia3["cores_usadas"])
print("Total de cores usadas:", dados_frequencia3["total_cores"])
plotar_frequencia(vertices3, arestas3, dados_frequencia3['cores_usadas'], "Coloração de Grafos - Exemplo 3")