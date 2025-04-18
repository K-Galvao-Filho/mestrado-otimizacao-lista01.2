import pulp
import matplotlib.pyplot as plt

# Função para resolver o problema de escalonamento de horários
def resolver_problema_escalonamento(demanda):
    dias = len(demanda)
    problema = pulp.LpProblem("Problema_Escalonamento", pulp.LpMinimize)

    x = {i: pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(dias)}

    problema += pulp.lpSum(x[i] for i in range(dias)), "Minimizar_total_enfermeiras"

    for d in range(dias):
        problema += pulp.lpSum(x[(d - i) % dias] for i in range(5)) >= demanda[d], f"Demanda_dia_{d}"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "inicio_enfermeiras": {i: x[i].varValue for i in range(dias)},
        "total_enfermeiras": pulp.value(problema.objective)
    }

    return resultado

# Função para plotar o resultado
def plotar_escalonamento(dados, titulo):
    dias = sorted(dados['inicio_enfermeiras'].keys())
    valores = [dados['inicio_enfermeiras'][d] for d in dias]

    fig, ax = plt.subplots()
    ax.bar(dias, valores, color='lightblue')
    ax.set_xlabel('Dia da semana')
    ax.set_ylabel('Enfermeiras iniciando')
    ax.set_title(titulo)
    ax.set_xticks(dias)
    ax.set_xticklabels(['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'])
    plt.show()

# Exemplo 1: Dados da apostila
demanda1 = [17, 13, 15, 19, 14, 16, 11]

print("\nProblema de Escalonamento de Horários - Exemplo 1:")
dados_escalonamento1 = resolver_problema_escalonamento(demanda1)
print("Status:", dados_escalonamento1["status"])
for dia, valor in dados_escalonamento1["inicio_enfermeiras"].items():
    print(f"Dia {dia} - Enfermeiras iniciando: {valor:.0f}")
print("Total de enfermeiras: ", dados_escalonamento1["total_enfermeiras"])
plotar_escalonamento(dados_escalonamento1, "Escalonamento de Enfermeiras - Exemplo 1")

# Exemplo 2: Demanda mais alta no meio da semana
demanda2 = [10, 12, 20, 25, 23, 18, 14]

print("\nProblema de Escalonamento de Horários - Exemplo 2:")
dados_escalonamento2 = resolver_problema_escalonamento(demanda2)
print("Status:", dados_escalonamento2["status"])
for dia, valor in dados_escalonamento2["inicio_enfermeiras"].items():
    print(f"Dia {dia} - Enfermeiras iniciando: {valor:.0f}")
print("Total de enfermeiras: ", dados_escalonamento2["total_enfermeiras"])
plotar_escalonamento(dados_escalonamento2, "Escalonamento de Enfermeiras - Exemplo 2")

# Exemplo 3: Demanda alta no fim de semana
demanda3 = [8, 9, 11, 10, 12, 20, 22]

print("\nProblema de Escalonamento de Horários - Exemplo 3:")
dados_escalonamento3 = resolver_problema_escalonamento(demanda3)
print("Status:", dados_escalonamento3["status"])
for dia, valor in dados_escalonamento3["inicio_enfermeiras"].items():
    print(f"Dia {dia} - Enfermeiras iniciando: {valor:.0f}")
print("Total de enfermeiras: ", dados_escalonamento3["total_enfermeiras"])
plotar_escalonamento(dados_escalonamento3, "Escalonamento de Enfermeiras - Exemplo 3")
