# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização linear
import matplotlib.pyplot as plt  # Para criar gráficos
import networkx as nx  # Para criar e visualizar redes de fluxo

# Função que calcula o fluxo máximo em uma rede, de uma origem a um destino
def resolver_problema_fluxo_maximo(capacidades, origem, destino):
    # Cria um problema para maximizar o fluxo total
    problema = pulp.LpProblem("Problema_Fluxo_Maximo", pulp.LpMaximize)

    # Cria variáveis: fluxo em cada arco (não negativo)
    variaveis = {(u, v): pulp.LpVariable(f"x_{u}_{v}", lowBound=0) for u in capacidades for v in capacidades[u]}

    # Define o objetivo: maximizar o fluxo que sai da origem
    problema += pulp.lpSum(variaveis[(origem, v)] for v in capacidades[origem]), "Fluxo_Total"

    # Identifica todos os nós (incluindo origem, destino e intermediários)
    nos = set(capacidades.keys()).union({v for dests in capacidades.values() for v in dests})
    intermediarios = nos - {origem, destino}  # Nós que não são origem nem destino

    # Restrições: conservação de fluxo (o que entra em um nó intermediário deve sair)
    for nodo in intermediarios:
        problema += (pulp.lpSum(variaveis[(u, nodo)] for u in capacidades if nodo in capacidades[u]) ==
                     pulp.lpSum(variaveis[(nodo, v)] for v in capacidades.get(nodo, {}))), f"Conservacao_fluxo_{nodo}"

    # Restrições: fluxo em cada arco não pode exceder a capacidade
    for u in capacidades:
        for v in capacidades[u]:
            problema += variaveis[(u, v)] <= capacidades[u][v], f"Capacidade_{u}_{v}"

    # Resolve o problema
    problema.solve()

    # Organiza os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "fluxos": {(u, v): variaveis[(u, v)].varValue for u in capacidades for v in capacidades[u]},  # Fluxo em cada arco
        "fluxo_total": pulp.value(problema.objective)  # Fluxo total
    }

    return resultado  # Retorna os resultados

# Função para criar um gráfico de rede mostrando os fluxos
def plotar_fluxo(dados, capacidades, titulo):
    G = nx.DiGraph()  # Cria um grafo direcionado

    # Adiciona arestas com fluxos maiores que zero, incluindo fluxo/capacidade
    for (u, v), fluxo in dados['fluxos'].items():
        if fluxo > 0:
            G.add_edge(u, v, label=f"{fluxo:.0f}/{capacidades[u][v]}")

    pos = nx.spring_layout(G, seed=42)  # Define posições dos nós
    labels = nx.get_edge_attributes(G, 'label')  # Rótulos com fluxo/capacidade

    plt.figure(figsize=(10, 6))  # Define tamanho da figura
    # Desenha o grafo com nós, arestas e rótulos
    nx.draw(G, pos, with_labels=True, arrows=True, node_size=2500, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title(titulo)  # Título do gráfico
    plt.axis('off')  # Remove os eixos
    plt.show()  # Exibe o gráfico

# Exemplo 1: Configuração inicial
capacidades1 = {
    's': {'a': 20, 'b': 10},  # Capacidades dos arcos saindo da origem 's'
    'a': {'b': 5, 't': 10},   # Capacidades dos arcos saindo de 'a'
    'b': {'t': 20}            # Capacidades dos arcos saindo de 'b'
}
origem1 = 's'  # Nó de origem
destino1 = 't'  # Nó de destino

dados_fluxo1 = resolver_problema_fluxo_maximo(capacidades1, origem1, destino1)

# Mostra os resultados do Exemplo 1
print("\nProblema do Fluxo Máximo - Exemplo 1:")
print("Status:", dados_fluxo1["status"])  # Status da solução
for (u, v), fluxo in dados_fluxo1["fluxos"].items():
    if fluxo > 0:
        print(f"Fluxo de {u} para {v}: {fluxo:.0f}")  # Fluxos não nulos
print("Fluxo Total: ", dados_fluxo1["fluxo_total"])  # Fluxo total
plotar_fluxo(dados_fluxo1, capacidades1, "Fluxo Máximo na Rede - Exemplo 1")  # Mostra o gráfico

# Exemplo 2: Novo conjunto de dados
capacidades2 = {
    's': {'a': 15, 'b': 10},  # Capacidades dos arcos saindo de 's'
    'a': {'c': 10},           # Capacidades dos arcos saindo de 'a'
    'b': {'c': 5, 't': 10},   # Capacidades dos arcos saindo de 'b'
    'c': {'t': 10}            # Capacidades dos arcos saindo de 'c'
}
origem2 = 's'
destino2 = 't'

dados_fluxo2 = resolver_problema_fluxo_maximo(capacidades2, origem2, destino2)

# Mostra os resultados do Exemplo 2
print("\nProblema do Fluxo Máximo - Exemplo 2:")
print("Status:", dados_fluxo2["status"])
for (u, v), fluxo in dados_fluxo2["fluxos"].items():
    if fluxo > 0:
        print(f"Fluxo de {u} para {v}: {fluxo:.0f}")
print("Fluxo Total: ", dados_fluxo2["fluxo_total"])
plotar_fluxo(dados_fluxo2, capacidades2, "Fluxo Máximo na Rede - Exemplo 2")

# Exemplo 3: Outro conjunto de dados
capacidades3 = {
    's': {'a': 25, 'b': 15},  # Capacidades dos arcos saindo de 's'
    'a': {'c': 10, 'd': 10},  # Capacidades dos arcos saindo de 'a'
    'b': {'d': 5, 'e': 10},   # Capacidades dos arcos saindo de 'b'
    'c': {'t': 10},           # Capacidades dos arcos saindo de 'c'
    'd': {'t': 15},           # Capacidades dos arcos saindo de 'd'
    'e': {'t': 10}            # Capacidades dos arcos saindo de 'e'
}
origem3 = 's'
destino3 = 't'

dados_fluxo3 = resolver_problema_fluxo_maximo(capacidades3, origem3, destino3)

# Mostra os resultados do Exemplo 3
print("\nProblema do Fluxo Máximo - Exemplo 3:")
print("Status:", dados_fluxo3["status"])
for (u, v), fluxo in dados_fluxo3["fluxos"].items():
    if fluxo > 0:
        print(f"Fluxo de {u} para {v}: {fluxo:.0f}")
print("Fluxo Total: ", dados_fluxo3["fluxo_total"])
plotar_fluxo(dados_fluxo3, capacidades3, "Fluxo Máximo na Rede - Exemplo 3")