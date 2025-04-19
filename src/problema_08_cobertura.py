# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização linear
import matplotlib.pyplot as plt  # Para criar gráficos
import networkx as nx  # Para criar e visualizar grafos

# Função que encontra o menor número de subconjuntos para cobrir todos os elementos
def resolver_problema_cobertura(elementos, subconjuntos):
    # Cria um problema para minimizar o número de subconjuntos usados
    problema = pulp.LpProblem("Problema_Cobertura", pulp.LpMinimize)

    # Cria variáveis binárias: 1 se o subconjunto é escolhido, 0 caso contrário
    x = {s: pulp.LpVariable(f"x_{s}", cat='Binary') for s in subconjuntos}

    # Define o objetivo: minimizar o total de subconjuntos escolhidos
    problema += pulp.lpSum(x[s] for s in subconjuntos), "Minimizar_numero_subconjuntos"

    # Restrições: cada elemento deve ser coberto por pelo menos um subconjunto
    for e in elementos:
        problema += pulp.lpSum(x[s] for s in subconjuntos if e in subconjuntos[s]) >= 1, f"Cobertura_elemento_{e}"

    # Resolve o problema
    problema.solve()

    # Organiza os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "subconjuntos_escolhidos": [s for s in subconjuntos if x[s].varValue == 1],  # Subconjuntos selecionados
        "total_subconjuntos": pulp.value(problema.objective)  # Número total de subconjuntos usados
    }

    return resultado  # Retorna os resultados

# Função para criar um grafo bipartido mostrando a cobertura
def plotar_cobertura(elementos, subconjuntos, subconjuntos_escolhidos, titulo):
    G = nx.Graph()  # Cria um grafo não direcionado

    # Adiciona nós para subconjuntos (lado esquerdo) e elementos (lado direito)
    for s in subconjuntos:
        G.add_node(s, bipartite=0)
    for e in elementos:
        G.add_node(e, bipartite=1)

    # Adiciona arestas entre subconjuntos e os elementos que eles cobrem
    for s, elems in subconjuntos.items():
        for e in elems:
            G.add_edge(s, e)

    # Define posições dos nós: subconjuntos à esquerda, elementos à direita
    pos = {}
    pos.update((n, (0, -i)) for i, n in enumerate(subconjuntos.keys()))
    pos.update((n, (2, -i)) for i, n in enumerate(elementos))

    # Desenha o grafo, destacando subconjuntos escolhidos em verde
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color=["lightgreen" if n in subconjuntos_escolhidos else "lightblue" for n in G.nodes()], node_size=2000)
    plt.title(titulo)  # Título do gráfico
    plt.axis('off')  # Remove os eixos
    plt.show()  # Exibe o gráfico

# Exemplo 1: Configuração inicial (dados da apostila)
print("\nProblema de Cobertura - Exemplo 1:")
elementos1 = {1, 2, 3, 4, 5}  # Elementos que precisam ser cobertos
subconjuntos1 = {
    'A': {1, 2, 3},  # Subconjunto A cobre os elementos 1, 2, 3
    'B': {2, 4},     # Subconjunto B cobre os elementos 2, 4
    'C': {3, 4},     # Subconjunto C cobre os elementos 3, 4
    'D': {4, 5}      # Subconjunto D cobre os elementos 4, 5
}
dados_cobertura1 = resolver_problema_cobertura(elementos1, subconjuntos1)
print("Status:", dados_cobertura1["status"])  # Status da solução
print("Subconjuntos escolhidos:", dados_cobertura1["subconjuntos_escolhidos"])  # Subconjuntos selecionados
print("Total de subconjuntos usados:", dados_cobertura1["total_subconjuntos"])  # Número de subconjuntos
plotar_cobertura(elementos1, subconjuntos1, dados_cobertura1['subconjuntos_escolhidos'], "Cobertura - Exemplo 1")  # Mostra o gráfico

# Exemplo 2: Novo conjunto de dados
print("\nProblema de Cobertura - Exemplo 2:")
elementos2 = {1, 2, 3, 4, 5, 6}  # Elementos que precisam ser cobertos
subconjuntos2 = {
    'X': {1, 4},     # Subconjunto X cobre os elementos 1, 4
    'Y': {2, 5},     # Subconjunto Y cobre os elementos 2, 5
    'Z': {3, 6},     # Subconjunto Z cobre os elementos 3, 6
    'W': {1, 2, 3},  # Subconjunto W cobre os elementos 1, 2, 3
    'V': {4, 5, 6}   # Subconjunto V cobre os elementos 4, 5, 6
}
dados_cobertura2 = resolver_problema_cobertura(elementos2, subconjuntos2)
print("Status:", dados_cobertura2["status"])
print("Subconjuntos escolhidos:", dados_cobertura2["subconjuntos_escolhidos"])
print("Total de subconjuntos usados:", dados_cobertura2["total_subconjuntos"])
plotar_cobertura(elementos2, subconjuntos2, dados_cobertura2['subconjuntos_escolhidos'], "Cobertura - Exemplo 2")

# Exemplo 3: Outro conjunto de dados
print("\nProblema de Cobertura - Exemplo 3:")
elementos3 = {1, 2, 3, 4, 5, 6, 7}  # Elementos que precisam ser cobertos
subconjuntos3 = {
    'M': {1, 2},     # Subconjunto M cobre os elementos 1, 2
    'N': {2, 3, 4},  # Subconjunto N cobre os elementos 2, 3, 4
    'O': {4, 5},     # Subconjunto O cobre os elementos 4, 5
    'P': {5, 6},     # Subconjunto P cobre os elementos 5, 6
    'Q': {6, 7},     # Subconjunto Q cobre os elementos 6, 7
    'R': {1, 7}      # Subconjunto R cobre os elementos 1, 7
}
dados_cobertura3 = resolver_problema_cobertura(elementos3, subconjuntos3)
print("Status:", dados_cobertura3["status"])
print("Subconjuntos escolhidos:", dados_cobertura3["subconjuntos_escolhidos"])
print("Total de subconjuntos usados:", dados_cobertura3["total_subconjuntos"])
plotar_cobertura(elementos3, subconjuntos3, dados_cobertura3['subconjuntos_escolhidos'], "Cobertura - Exemplo 3")