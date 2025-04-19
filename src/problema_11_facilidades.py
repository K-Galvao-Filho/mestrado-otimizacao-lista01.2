# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização linear
import matplotlib.pyplot as plt  # Para criar gráficos
import networkx as nx  # Para criar e visualizar grafos

# Função que decide quais locais abrir e como atender clientes para minimizar custos
def resolver_problema_facilidades(custos_fixos, custos_atendimento):
    # Cria um problema para minimizar o custo total
    problema = pulp.LpProblem("Problema_Facilidades", pulp.LpMinimize)

    locais = list(custos_fixos.keys())  # Lista de locais (ex.: Local1, Local2)
    clientes = list(next(iter(custos_atendimento.values())).keys())  # Lista de clientes (ex.: A, B)

    # Variáveis binárias: y[l] = 1 se o local l está aberto, 0 caso contrário
    y = {l: pulp.LpVariable(f"y_{l}", cat='Binary') for l in locais}
    # Variáveis binárias: x[l,c] = 1 se o local l atende o cliente c, 0 caso contrário
    x = {(l, c): pulp.LpVariable(f"x_{l}_{c}", cat='Binary') for l in locais for c in clientes}

    # Define o objetivo: minimizar custos fixos (de abrir locais) + custos de atendimento
    problema += pulp.lpSum(custos_fixos[l] * y[l] + custos_atendimento[l][c] * x[(l, c)] for l in locais for c in clientes), "Minimizar_Custo_Total"

    # Restrições: cada cliente deve ser atendido exatamente por um local
    for c in clientes:
        problema += pulp.lpSum(x[(l, c)] for l in locais) == 1, f"Atender_cliente_{c}"

    # Restrições: um cliente só pode ser atendido por um local se esse local estiver aberto
    for l in locais:
        for c in clientes:
            problema += x[(l, c)] <= y[l], f"Cliente_{c}_so_se_local_{l}_aberto"

    # Resolve o problema
    problema.solve()

    # Organiza os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "locais_abertos": [l for l in locais if y[l].varValue == 1],  # Locais abertos
        "atendimentos": {(l, c): x[(l, c)].varValue for l in locais for c in clientes if x[(l, c)].varValue == 1},  # Atendimentos realizados
        "custo_total": pulp.value(problema.objective)  # Custo total
    }

    return resultado  # Retorna os resultados

# Função para criar um grafo direcionado mostrando a rede de atendimento
def plotar_facilidades(locais_abertos, atendimentos, titulo):
    G = nx.DiGraph()  # Cria um grafo direcionado

    # Identifica locais e clientes a partir dos atendimentos
    locais = set(l for l, c in atendimentos.keys())
    clientes = set(c for l, c in atendimentos.keys())

    # Adiciona nós para locais (lado esquerdo) e clientes (lado direito)
    for l in locais:
        G.add_node(l, bipartite=0)
    for c in clientes:
        G.add_node(c, bipartite=1)

    # Adiciona arestas para os atendimentos (local -> cliente)
    for (l, c) in atendimentos:
        G.add_edge(l, c)

    # Define posições: locais à esquerda, clientes à direita
    pos = {}
    pos.update((n, (0, -i)) for i, n in enumerate(sorted(locais)))
    pos.update((n, (2, -i)) for i, n in enumerate(sorted(clientes)))

    # Desenha o grafo, destacando locais abertos em verde
    plt.figure(figsize=(12, 7))
    nx.draw(G, pos, with_labels=True, node_color=['lightgreen' if n in locais_abertos else 'lightblue' for n in G.nodes()], node_size=2500)
    plt.title(titulo)  # Título do gráfico
    plt.axis('off')  # Remove os eixos
    plt.show()  # Exibe o gráfico

# Exemplo 1: Configuração inicial (dados da apostila)
custos_fixos1 = {'Local1': 100, 'Local2': 120, 'Local3': 90}  # Custos fixos para abrir cada local
custos_atendimento1 = {
    'Local1': {'A': 20, 'B': 24, 'C': 18},  # Custos de atendimento do Local1 para cada cliente
    'Local2': {'A': 28, 'B': 20, 'C': 26},  # Custos de atendimento do Local2
    'Local3': {'A': 22, 'B': 23, 'C': 20}   # Custos de atendimento do Local3
}

dados_facilidades1 = resolver_problema_facilidades(custos_fixos1, custos_atendimento1)

print("\nProblema das Facilidades - Exemplo 1:")
print("Status:", dados_facilidades1["status"])  # Status da solução
print("Locais abertos:", dados_facilidades1["locais_abertos"])  # Locais abertos
print("Atendimentos:", dados_facilidades1["atendimentos"])  # Atendimentos realizados
print("Custo total: R$", dados_facilidades1["custo_total"])  # Custo total
plotar_facilidades(dados_facilidades1['locais_abertos'], dados_facilidades1['atendimentos'], "Rede de Atendimento - Exemplo 1")  # Mostra o gráfico

# Exemplo 2: Conjunto com mais locais
custos_fixos2 = {'LocalA': 80, 'LocalB': 110, 'LocalC': 95, 'LocalD': 70}  # Custos fixos
custos_atendimento2 = {
    'LocalA': {'D': 15, 'E': 25, 'F': 22},  # Custos de atendimento do LocalA
    'LocalB': {'D': 20, 'E': 18, 'F': 21},  # Custos de atendimento do LocalB
    'LocalC': {'D': 22, 'E': 20, 'F': 24},  # Custos de atendimento do LocalC
    'LocalD': {'D': 17, 'E': 19, 'F': 20}   # Custos de atendimento do LocalD
}

dados_facilidades2 = resolver_problema_facilidades(custos_fixos2, custos_atendimento2)

print("\nProblema das Facilidades - Exemplo 2:")
print("Status:", dados_facilidades2["status"])
print("Locais abertos:", dados_facilidades2["locais_abertos"])
print("Atendimentos:", dados_facilidades2["atendimentos"])
print("Custo total: R$", dados_facilidades2["custo_total"])
plotar_facilidades(dados_facilidades2['locais_abertos'], dados_facilidades2['atendimentos'], "Rede de Atendimento - Exemplo 2")

# Exemplo 3: Conjunto maior com mais clientes
custos_fixos3 = {'Centro1': 130, 'Centro2': 90, 'Centro3': 120, 'Centro4': 85}  # Custos fixos
custos_atendimento3 = {
    'Centro1': {'G': 30, 'H': 35, 'I': 28, 'J': 32},  # Custos de atendimento do Centro1
    'Centro2': {'G': 25, 'H': 30, 'I': 20, 'J': 24},  # Custos de atendimento do Centro2
    'Centro3': {'G': 32, 'H': 29, 'I': 27, 'J': 30},  # Custos de atendimento do Centro3
    'Centro4': {'G': 26, 'H': 27, 'I': 25, 'J': 28}   # Custos de atendimento do Centro4
}

dados_facilidades3 = resolver_problema_facilidades(custos_fixos3, custos_atendimento3)

print("\nProblema das Facilidades - Exemplo 3:")
print("Status:", dados_facilidades3["status"])
print("Locais abertos:", dados_facilidades3["locais_abertos"])
print("Atendimentos:", dados_facilidades3["atendimentos"])
print("Custo total: R$", dados_facilidades3["custo_total"])
plotar_facilidades(dados_facilidades3['locais_abertos'], dados_facilidades3['atendimentos'], "Rede de Atendimento - Exemplo 3")