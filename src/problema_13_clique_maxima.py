import pulp
import matplotlib.pyplot as plt
import networkx as nx

def resolver_problema_designacao(custos):
    problema = pulp.LpProblem("Problema_Designacao", pulp.LpMinimize)

    agentes = list(custos.keys())
    tarefas = list(next(iter(custos.values())).keys())

    variaveis = {(a, t): pulp.LpVariable(f"x_{a}_{t}", cat='Binary') for a in agentes for t in tarefas}

    problema += pulp.lpSum(custos[a][t] * variaveis[(a, t)] for a in agentes for t in tarefas), "Custo_Total"

    for a in agentes:
        problema += pulp.lpSum(variaveis[(a, t)] for t in tarefas) == 1, f"Um_trabalho_por_agente_{a}"

    for t in tarefas:
        problema += pulp.lpSum(variaveis[(a, t)] for a in agentes) == 1, f"Uma_tarefa_por_trabalho_{t}"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "designacoes": {(a, t): variaveis[(a, t)].varValue for a in agentes for t in tarefas},
        "custo_total": pulp.value(problema.objective)
    }

    return resultado

def plotar_designacao(dados, titulo):
    G = nx.DiGraph()
    agentes = sorted(set(a for a, t in dados['designacoes'].keys()))
    tarefas = sorted(set(t for a, t in dados['designacoes'].keys()))

    pos = {}
    for i, a in enumerate(agentes):
        pos[f"Agente {a}"] = (0, -i)
    for j, t in enumerate(tarefas):
        pos[f"Tarefa {t}"] = (2, -j)

    for (a, t), valor in dados['designacoes'].items():
        if valor == 1:
            G.add_edge(f"Agente {a}", f"Tarefa {t}")

    plt.figure(figsize=(8, 5))
    nx.draw(G, pos, with_labels=True, arrows=True, connectionstyle='arc3,rad=0.1', node_size=2500, node_color='lightgreen')
    plt.title(titulo)
    plt.axis('off')
    plt.show()

# Exemplo 1: Dados originais
custos1 = {
    1: {1: 13, 2: 20, 3: 15},
    2: {1: 12, 2: 17, 3: 18},
    3: {1: 16, 2: 18, 3: 14}
}

dados_designacao1 = resolver_problema_designacao(custos1)

print("\nProblema de Designacao - Exemplo 1:")
print("Status:", dados_designacao1["status"])
for (a, t), valor in dados_designacao1["designacoes"].items():
    if valor == 1:
        print(f"Agente {a} foi designado para Tarefa {t}")
print("Custo Total: R$", dados_designacao1["custo_total"])
plotar_designacao(dados_designacao1, "Designação de Agentes para Tarefas - Exemplo 1")

# Exemplo 2: Novos dados
custos2 = {
    1: {1: 22, 2: 25, 3: 20},
    2: {1: 18, 2: 17, 3: 21},
    3: {1: 24, 2: 19, 3: 23}
}

dados_designacao2 = resolver_problema_designacao(custos2)

print("\nProblema de Designacao - Exemplo 2:")
print("Status:", dados_designacao2["status"])
for (a, t), valor in dados_designacao2["designacoes"].items():
    if valor == 1:
        print(f"Agente {a} foi designado para Tarefa {t}")
print("Custo Total: R$", dados_designacao2["custo_total"])
plotar_designacao(dados_designacao2, "Designação de Agentes para Tarefas - Exemplo 2")

# Exemplo 3: Outro conjunto novo
custos3 = {
    1: {1: 30, 2: 28, 3: 35},
    2: {1: 26, 2: 32, 3: 29},
    3: {1: 27, 2: 30, 3: 25}
}

dados_designacao3 = resolver_problema_designacao(custos3)

print("\nProblema de Designacao - Exemplo 3:")
print("Status:", dados_designacao3["status"])
for (a, t), valor in dados_designacao3["designacoes"].items():
    if valor == 1:
        print(f"Agente {a} foi designado para Tarefa {t}")
print("Custo Total: R$", dados_designacao3["custo_total"])
plotar_designacao(dados_designacao3, "Designação de Agentes para Tarefas - Exemplo 3")