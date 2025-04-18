import pulp
import matplotlib.pyplot as plt
import networkx as nx

# Função para resolver o problema das facilidades
def resolver_problema_facilidades(custos_fixos, custos_atendimento):
    problema = pulp.LpProblem("Problema_Facilidades", pulp.LpMinimize)

    locais = list(custos_fixos.keys())
    clientes = list(next(iter(custos_atendimento.values())).keys())

    y = {l: pulp.LpVariable(f"y_{l}", cat='Binary') for l in locais}
    x = {(l, c): pulp.LpVariable(f"x_{l}_{c}", cat='Binary') for l in locais for c in clientes}

    problema += pulp.lpSum(custos_fixos[l] * y[l] + custos_atendimento[l][c] * x[(l, c)] for l in locais for c in clientes), "Minimizar_Custo_Total"

    for c in clientes:
        problema += pulp.lpSum(x[(l, c)] for l in locais) == 1, f"Atender_cliente_{c}"

    for l in locais:
        for c in clientes:
            problema += x[(l, c)] <= y[l], f"Cliente_{c}_so_se_local_{l}_aberto"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "locais_abertos": [l for l in locais if y[l].varValue == 1],
        "atendimentos": {(l, c): x[(l, c)].varValue for l in locais for c in clientes if x[(l, c)].varValue == 1},
        "custo_total": pulp.value(problema.objective)
    }

    return resultado

# Função para plotar a rede de atendimento
def plotar_facilidades(locais_abertos, atendimentos, titulo):
    G = nx.DiGraph()
    locais = set(l for l, c in atendimentos.keys())
    clientes = set(c for l, c in atendimentos.keys())

    for l in locais:
        G.add_node(l, bipartite=0)
    for c in clientes:
        G.add_node(c, bipartite=1)

    for (l, c) in atendimentos:
        G.add_edge(l, c)

    pos = {}
    pos.update((n, (0, -i)) for i, n in enumerate(sorted(locais)))
    pos.update((n, (2, -i)) for i, n in enumerate(sorted(clientes)))

    plt.figure(figsize=(12, 7))
    nx.draw(G, pos, with_labels=True, node_color=['lightgreen' if n in locais_abertos else 'lightblue' for n in G.nodes()], node_size=2500)
    plt.title(titulo)
    plt.axis('off')
    plt.show()

# Exemplo 1: Dados da apostila
custos_fixos1 = {'Local1': 100, 'Local2': 120, 'Local3': 90}
custos_atendimento1 = {
    'Local1': {'A': 20, 'B': 24, 'C': 18},
    'Local2': {'A': 28, 'B': 20, 'C': 26},
    'Local3': {'A': 22, 'B': 23, 'C': 20}
}

dados_facilidades1 = resolver_problema_facilidades(custos_fixos1, custos_atendimento1)

print("\nProblema das Facilidades - Exemplo 1:")
print("Status:", dados_facilidades1["status"])
print("Locais abertos:", dados_facilidades1["locais_abertos"])
print("Atendimentos:", dados_facilidades1["atendimentos"])
print("Custo total: R$", dados_facilidades1["custo_total"])
plotar_facilidades(dados_facilidades1['locais_abertos'], dados_facilidades1['atendimentos'], "Rede de Atendimento - Exemplo 1")

# Exemplo 2: Novo conjunto com mais opções
custos_fixos2 = {'LocalA': 80, 'LocalB': 110, 'LocalC': 95, 'LocalD': 70}
custos_atendimento2 = {
    'LocalA': {'D': 15, 'E': 25, 'F': 22},
    'LocalB': {'D': 20, 'E': 18, 'F': 21},
    'LocalC': {'D': 22, 'E': 20, 'F': 24},
    'LocalD': {'D': 17, 'E': 19, 'F': 20}
}

dados_facilidades2 = resolver_problema_facilidades(custos_fixos2, custos_atendimento2)

print("\nProblema das Facilidades - Exemplo 2:")
print("Status:", dados_facilidades2["status"])
print("Locais abertos:", dados_facilidades2["locais_abertos"])
print("Atendimentos:", dados_facilidades2["atendimentos"])
print("Custo total: R$", dados_facilidades2["custo_total"])
plotar_facilidades(dados_facilidades2['locais_abertos'], dados_facilidades2['atendimentos'], "Rede de Atendimento - Exemplo 2")

# Exemplo 3: Outro conjunto variado e maior
custos_fixos3 = {'Centro1': 130, 'Centro2': 90, 'Centro3': 120, 'Centro4': 85}
custos_atendimento3 = {
    'Centro1': {'G': 30, 'H': 35, 'I': 28, 'J': 32},
    'Centro2': {'G': 25, 'H': 30, 'I': 20, 'J': 24},
    'Centro3': {'G': 32, 'H': 29, 'I': 27, 'J': 30},
    'Centro4': {'G': 26, 'H': 27, 'I': 25, 'J': 28}
}

dados_facilidades3 = resolver_problema_facilidades(custos_fixos3, custos_atendimento3)

print("\nProblema das Facilidades - Exemplo 3:")
print("Status:", dados_facilidades3["status"])
print("Locais abertos:", dados_facilidades3["locais_abertos"])
print("Atendimentos:", dados_facilidades3["atendimentos"])
print("Custo total: R$", dados_facilidades3["custo_total"])
plotar_facilidades(dados_facilidades3['locais_abertos'], dados_facilidades3['atendimentos'], "Rede de Atendimento - Exemplo 3")