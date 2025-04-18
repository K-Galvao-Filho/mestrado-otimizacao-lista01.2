import pulp
import matplotlib.pyplot as plt

# Função para resolver o problema de cobertura
def resolver_problema_cobertura(elementos, subconjuntos):
    problema = pulp.LpProblem("Problema_Cobertura", pulp.LpMinimize)

    x = {s: pulp.LpVariable(f"x_{s}", cat='Binary') for s in subconjuntos}

    problema += pulp.lpSum(x[s] for s in subconjuntos), "Minimizar_numero_subconjuntos"

    for e in elementos:
        problema += pulp.lpSum(x[s] for s in subconjuntos if e in subconjuntos[s]) >= 1, f"Cobertura_elemento_{e}"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "subconjuntos_escolhidos": [s for s in subconjuntos if x[s].varValue == 1],
        "total_subconjuntos": pulp.value(problema.objective)
    }

    return resultado

# Função para plotar o resultado de cobertura
def plotar_cobertura(elementos, subconjuntos, subconjuntos_escolhidos, titulo):
    cores = ['lightblue' if s not in subconjuntos_escolhidos else 'lightgreen' for s in subconjuntos]
    fig, ax = plt.subplots()
    ax.bar(subconjuntos.keys(), [len(subconjuntos[s]) for s in subconjuntos], color=cores)
    plt.xlabel('Subconjuntos')
    plt.ylabel('Elementos cobertos')
    plt.title(titulo)
    plt.show()

# Exemplo 1: Dados da apostila
print("\nProblema de Cobertura - Exemplo 1:")
elementos1 = {1, 2, 3, 4, 5}
subconjuntos1 = {
    'A': {1, 2, 3},
    'B': {2, 4},
    'C': {3, 4},
    'D': {4, 5}
}
dados_cobertura1 = resolver_problema_cobertura(elementos1, subconjuntos1)
print("Status:", dados_cobertura1["status"])
print("Subconjuntos escolhidos:", dados_cobertura1["subconjuntos_escolhidos"])
print("Total de subconjuntos usados:", dados_cobertura1["total_subconjuntos"])
plotar_cobertura(elementos1, subconjuntos1, dados_cobertura1['subconjuntos_escolhidos'], "Cobertura - Exemplo 1")

# Exemplo 2: Novo conjunto de dados
print("\nProblema de Cobertura - Exemplo 2:")
elementos2 = {1, 2, 3, 4, 5, 6}
subconjuntos2 = {
    'X': {1, 4},
    'Y': {2, 5},
    'Z': {3, 6},
    'W': {1, 2, 3},
    'V': {4, 5, 6}
}
dados_cobertura2 = resolver_problema_cobertura(elementos2, subconjuntos2)
print("Status:", dados_cobertura2["status"])
print("Subconjuntos escolhidos:", dados_cobertura2["subconjuntos_escolhidos"])
print("Total de subconjuntos usados:", dados_cobertura2["total_subconjuntos"])
plotar_cobertura(elementos2, subconjuntos2, dados_cobertura2['subconjuntos_escolhidos'], "Cobertura - Exemplo 2")

# Exemplo 3: Outro conjunto diferente
print("\nProblema de Cobertura - Exemplo 3:")
elementos3 = {1, 2, 3, 4, 5, 6, 7}
subconjuntos3 = {
    'M': {1, 2},
    'N': {2, 3, 4},
    'O': {4, 5},
    'P': {5, 6},
    'Q': {6, 7},
    'R': {1, 7}
}
dados_cobertura3 = resolver_problema_cobertura(elementos3, subconjuntos3)
print("Status:", dados_cobertura3["status"])
print("Subconjuntos escolhidos:", dados_cobertura3["subconjuntos_escolhidos"])
print("Total de subconjuntos usados:", dados_cobertura3["total_subconjuntos"])
plotar_cobertura(elementos3, subconjuntos3, dados_cobertura3['subconjuntos_escolhidos'], "Cobertura - Exemplo 3")