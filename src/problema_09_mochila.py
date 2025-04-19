# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização linear
import matplotlib.pyplot as plt  # Para criar gráficos

# Função que seleciona os itens mais valiosos para colocar na mochila sem exceder a capacidade
def resolver_problema_mochila(valores, pesos, capacidade):
    # Cria um problema para maximizar o valor total dos itens escolhidos
    problema = pulp.LpProblem("Problema_Mochila", pulp.LpMaximize)

    n = len(valores)  # Número de itens disponíveis
    # Cria variáveis binárias: 1 se o item é escolhido, 0 caso contrário
    x = [pulp.LpVariable(f"x_{i}", cat='Binary') for i in range(n)]

    # Define o objetivo: maximizar o valor total (soma do valor de cada item escolhido)
    problema += pulp.lpSum(valores[i] * x[i] for i in range(n)), "Maximizar_valor"
    # Restrição: o peso total dos itens escolhidos não pode exceder a capacidade da mochila
    problema += pulp.lpSum(pesos[i] * x[i] for i in range(n)) <= capacidade, "Restricao_capacidade"

    # Resolve o problema
    problema.solve()

    # Organiza os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "itens_escolhidos": [i for i in range(n) if x[i].varValue == 1],  # Índices dos itens escolhidos
        "valor_total": pulp.value(problema.objective),  # Valor total dos itens
        "peso_total": sum(pesos[i] for i in range(n) if x[i].varValue == 1)  # Peso total dos itens
    }

    return resultado  # Retorna os resultados

# Função para criar um gráfico de barras mostrando os itens selecionados
def plotar_mochila(valores, pesos, itens_escolhidos, titulo):
    fig, ax = plt.subplots()  # Cria uma figura
    indices = list(range(len(valores)))  # Índices dos itens
    # Destaca itens escolhidos em verde e os não escolhidos em azul
    cores = ['lightgreen' if i in itens_escolhidos else 'lightblue' for i in indices]
    ax.bar(indices, [valores[i] for i in indices], color=cores)  # Cria o gráfico de barras
    ax.set_xlabel('Itens')  # Nome do eixo X
    ax.set_ylabel('Valor')  # Nome do eixo Y
    ax.set_title(titulo)  # Título do gráfico
    plt.xticks(indices)  # Define os ticks do eixo X
    plt.show()  # Exibe o gráfico

# Exemplo 1: Configuração inicial
valores1 = [60, 100, 120]  # Valores dos itens
pesos1 = [10, 20, 30]  # Pesos dos itens
capacidade1 = 50  # Capacidade da mochila

dados_mochila1 = resolver_problema_mochila(valores1, pesos1, capacidade1)

print("\nProblema da Mochila - Exemplo 1:")
print("Status:", dados_mochila1["status"])  # Status da solução
print("Itens escolhidos:", dados_mochila1["itens_escolhidos"])  # Itens selecionados
print("Valor total: R$", dados_mochila1["valor_total"])  # Valor total
print("Peso total: ", dados_mochila1["peso_total"])  # Peso total
plotar_mochila(valores1, pesos1, dados_mochila1['itens_escolhidos'], "Mochila - Exemplo 1")  # Mostra o gráfico

# Exemplo 2: Mais itens com capacidade limitada
valores2 = [90, 20, 60, 40, 30]  # Valores dos itens
pesos2 = [15, 5, 10, 8, 6]  # Pesos dos itens
capacidade2 = 25  # Capacidade da mochila

dados_mochila2 = resolver_problema_mochila(valores2, pesos2, capacidade2)

print("\nProblema da Mochila - Exemplo 2:")
print("Status:", dados_mochila2["status"])
print("Itens escolhidos:", dados_mochila2["itens_escolhidos"])
print("Valor total: R$", dados_mochila2["valor_total"])
print("Peso total: ", dados_mochila2["peso_total"])
plotar_mochila(valores2, pesos2, dados_mochila2['itens_escolhidos'], "Mochila - Exemplo 2")

# Exemplo 3: Mochila com mais itens e pesos variados
valores3 = [45, 60, 75, 40, 30, 20]  # Valores dos itens
pesos3 = [3, 8, 7, 4, 2, 1]  # Pesos dos itens
capacidade3 = 15  # Capacidade da mochila

dados_mochila3 = resolver_problema_mochila(valores3, pesos3, capacidade3)

print("\nProblema da Mochila - Exemplo 3:")
print("Status:", dados_mochila3["status"])
print("Itens escolhidos:", dados_mochila3["itens_escolhidos"])
print("Valor total: R$", dados_mochila3["valor_total"])
print("Peso total: ", dados_mochila3["peso_total"])
plotar_mochila(valores3, pesos3, dados_mochila3['itens_escolhidos'], "Mochila - Exemplo 3")

# Exemplo 4: Valores e pesos variados
valores4 = [80, 50, 60, 90, 20]  # Valores dos itens
pesos4 = [10, 5, 7, 12, 3]  # Pesos dos itens
capacidade4 = 20  # Capacidade da mochila

dados_mochila4 = resolver_problema_mochila(valores4, pesos4, capacidade4)

print("\nProblema da Mochila - Exemplo 4:")
print("Status:", dados_mochila4["status"])
print("Itens escolhidos:", dados_mochila4["itens_escolhidos"])
print("Valor total: R$", dados_mochila4["valor_total"])
print("Peso total: ", dados_mochila4["peso_total"])
plotar_mochila(valores4, pesos4, dados_mochila4['itens_escolhidos'], "Mochila - Exemplo 4")