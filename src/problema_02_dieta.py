# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização linear
import matplotlib.pyplot as plt  # Para criar gráficos

# Função que calcula a combinação de ingredientes mais barata para atender às necessidades de vitaminas
def resolver_problema_dieta(matriz_vitaminas, precos, quantidades_minimas):
    # Conta o número de ingredientes e vitaminas
    num_ingredientes = len(precos)  # Quantos ingredientes existem
    num_vitaminas = len(quantidades_minimas)  # Quantas vitaminas precisam ser atendidas

    # Cria um problema para minimizar o custo
    problema = pulp.LpProblem("Problema_Dieta", pulp.LpMinimize)

    # Define as variáveis: quantidade de cada ingrediente (não negativa)
    ingredientes = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(num_ingredientes)]

    # Define o objetivo: minimizar o custo total (preço de cada ingrediente * quantidade)
    problema += pulp.lpSum(precos[i] * ingredientes[i] for i in range(num_ingredientes)), "Custo_Total"

    # Adiciona restrições: cada vitamina deve atingir pelo menos a quantidade mínima
    for v in range(num_vitaminas):
        problema += pulp.lpSum(matriz_vitaminas[v][i] * ingredientes[i] for i in range(num_ingredientes)) >= quantidades_minimas[v], f"Vitamina_{v+1}"

    # Resolve o problema
    problema.solve()

    # Organiza os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "quantidades": [ingredientes[i].varValue for i in range(num_ingredientes)],  # Quantidade de cada ingrediente
        "custo_total": pulp.value(problema.objective)  # Custo total da dieta
    }

    return resultado  # Retorna os resultados

# Função para criar um gráfico de barras com as quantidades dos ingredientes
def plotar_dieta(dados, titulo):
    labels = [f'Ingrediente {i+1}' for i in range(len(dados['quantidades']))]  # Nomes dos ingredientes
    valores = dados['quantidades']  # Quantidades de cada ingrediente

    fig, ax = plt.subplots()  # Cria uma figura
    ax.bar(labels, valores)  # Cria o gráfico de barras
    ax.set_ylabel('Quantidade utilizada')  # Nome do eixo Y
    ax.set_title(titulo)  # Título do gráfico
    plt.xticks(rotation=45)  # Rotaciona os rótulos do eixo X para melhor leitura
    plt.show()  # Exibe o gráfico

# Dados do problema
matriz_vitaminas = [
    [1, 0, 2, 2, 1, 2],  # Quantidade de vitamina 1 por ingrediente
    [0, 1, 3, 1, 3, 2]   # Quantidade de vitamina 2 por ingrediente
]
precos = [35, 30, 60, 50, 27, 22]  # Preços dos ingredientes
quantidades_minimas = [9, 19]  # Quantidades mínimas de vitaminas 1 e 2

# Exemplo 1: Configuração inicial
dados_dieta1 = resolver_problema_dieta(matriz_vitaminas, precos, quantidades_minimas)

# Mostra os resultados do Exemplo 1
print("Problema da Dieta - Exemplo 1:")
print("Status:", dados_dieta1["status"])  # Status da solução
for idx, qtd in enumerate(dados_dieta1["quantidades"]):
    print(f"Quantidade do Ingrediente {idx+1}: {qtd:.2f}")  # Quantidade de cada ingrediente
print("Custo Total: R$", dados_dieta1["custo_total"])  # Custo total
plotar_dieta(dados_dieta1, "Composição da Dieta - Exemplo 1")  # Mostra o gráfico
print("\n" + "="*50 + "\n")  # Separador

# Exemplo 2: Aumentando as necessidades de vitaminas
quantidades_minimas2 = [15, 30]  # Maiores quantidades mínimas de vitaminas
dados_dieta2 = resolver_problema_dieta(matriz_vitaminas, precos, quantidades_minimas2)

# Mostra os resultados do Exemplo 2
print("\nProblema da Dieta - Exemplo 2:")
print("Status:", dados_dieta2["status"])
for idx, qtd in enumerate(dados_dieta2["quantidades"]):
    print(f"Quantidade do Ingrediente {idx+1}: {qtd:.2f}")
print("Custo Total: R$", dados_dieta2["custo_total"])
plotar_dieta(dados_dieta2, "Composição da Dieta - Exemplo 2")
print("\n" + "="*50 + "\n")

# Exemplo 3: Alterando preços e exigências de vitaminas
precos3 = [45, 25, 65, 55, 25, 18]  # Novos preços dos ingredientes
quantidades_minimas3 = [10, 22]  # Novas quantidades mínimas de vitaminas
dados_dieta3 = resolver_problema_dieta(matriz_vitaminas, precos3, quantidades_minimas3)

# Mostra os resultados do Exemplo 3
print("\nProblema da Dieta - Exemplo 3:")
print("Status:", dados_dieta3["status"])
for idx, qtd in enumerate(dados_dieta3["quantidades"]):
    print(f"Quantidade do Ingrediente {idx+1}: {qtd:.2f}")
print("Custo Total: R$", dados_dieta3["custo_total"])
plotar_dieta(dados_dieta3, "Composição da Dieta - Exemplo 3")
print("\n" + "="*50 + "\n")