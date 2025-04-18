import pulp
import matplotlib.pyplot as plt

# Função para resolver o problema da mochila
def resolver_problema_mochila(valores, pesos, capacidade):
    problema = pulp.LpProblem("Problema_Mochila", pulp.LpMaximize)

    n = len(valores)
    x = [pulp.LpVariable(f"x_{i}", cat='Binary') for i in range(n)]

    problema += pulp.lpSum(valores[i] * x[i] for i in range(n)), "Maximizar_valor"
    problema += pulp.lpSum(pesos[i] * x[i] for i in range(n)) <= capacidade, "Restricao_capacidade"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "itens_escolhidos": [i for i in range(n) if x[i].varValue == 1],
        "valor_total": pulp.value(problema.objective),
        "peso_total": sum(pesos[i] for i in range(n) if x[i].varValue == 1)
    }

    return resultado

# Função para plotar os itens selecionados
def plotar_mochila(valores, pesos, itens_escolhidos, titulo):
    fig, ax = plt.subplots()
    indices = list(range(len(valores)))
    cores = ['lightgreen' if i in itens_escolhidos else 'lightblue' for i in indices]
    ax.bar(indices, [valores[i] for i in indices], color=cores)
    ax.set_xlabel('Itens')
    ax.set_ylabel('Valor')
    ax.set_title(titulo)
    plt.xticks(indices)
    plt.show()

# Exemplo 1: Dados do problema
valores1 = [60, 100, 120]
pesos1 = [10, 20, 30]
capacidade1 = 50

dados_mochila1 = resolver_problema_mochila(valores1, pesos1, capacidade1)

print("\nProblema da Mochila - Exemplo 1:")
print("Status:", dados_mochila1["status"])
print("Itens escolhidos:", dados_mochila1["itens_escolhidos"])
print("Valor total: R$", dados_mochila1["valor_total"])
print("Peso total: ", dados_mochila1["peso_total"])
plotar_mochila(valores1, pesos1, dados_mochila1['itens_escolhidos'], "Mochila - Exemplo 1")

# Exemplo 2: Outro conjunto de dados
valores2 = [90, 20, 60, 40, 30]
pesos2 = [15, 5, 10, 8, 6]
capacidade2 = 25

dados_mochila2 = resolver_problema_mochila(valores2, pesos2, capacidade2)

print("\nProblema da Mochila - Exemplo 2:")
print("Status:", dados_mochila2["status"])
print("Itens escolhidos:", dados_mochila2["itens_escolhidos"])
print("Valor total: R$", dados_mochila2["valor_total"])
print("Peso total: ", dados_mochila2["peso_total"])
plotar_mochila(valores2, pesos2, dados_mochila2['itens_escolhidos'], "Mochila - Exemplo 2")

# Exemplo 3: Mochila com mais itens
valores3 = [45, 60, 75, 40, 30, 20]
pesos3 = [3, 8, 7, 4, 2, 1]
capacidade3 = 15

dados_mochila3 = resolver_problema_mochila(valores3, pesos3, capacidade3)

print("\nProblema da Mochila - Exemplo 3:")
print("Status:", dados_mochila3["status"])
print("Itens escolhidos:", dados_mochila3["itens_escolhidos"])
print("Valor total: R$", dados_mochila3["valor_total"])
print("Peso total: ", dados_mochila3["peso_total"])
plotar_mochila(valores3, pesos3, dados_mochila3['itens_escolhidos'], "Mochila - Exemplo 3")

# Exemplo 4: Mochila com valores e pesos variados
valores4 = [80, 50, 60, 90, 20]
pesos4 = [10, 5, 7, 12, 3]
capacidade4 = 20

dados_mochila4 = resolver_problema_mochila(valores4, pesos4, capacidade4)

print("\nProblema da Mochila - Exemplo 4:")
print("Status:", dados_mochila4["status"])
print("Itens escolhidos:", dados_mochila4["itens_escolhidos"])
print("Valor total: R$", dados_mochila4["valor_total"])
print("Peso total: ", dados_mochila4["peso_total"])
plotar_mochila(valores4, pesos4, dados_mochila4['itens_escolhidos'], "Mochila - Exemplo 4")
# Arquivo de resolução para Problema 09 Mochila.Py

