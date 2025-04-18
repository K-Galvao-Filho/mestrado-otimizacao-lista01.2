import pulp
import matplotlib.pyplot as plt

def resolver_problema_dieta(matriz_vitaminas, precos, quantidades_minimas):
    num_ingredientes = len(precos)
    num_vitaminas = len(quantidades_minimas)

    problema = pulp.LpProblem("Problema_Dieta", pulp.LpMinimize)

    ingredientes = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(num_ingredientes)]

    problema += pulp.lpSum(precos[i] * ingredientes[i] for i in range(num_ingredientes)), "Custo_Total"

    for v in range(num_vitaminas):
        problema += pulp.lpSum(matriz_vitaminas[v][i] * ingredientes[i] for i in range(num_ingredientes)) >= quantidades_minimas[v], f"Vitamina_{v+1}"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "quantidades": [ingredientes[i].varValue for i in range(num_ingredientes)],
        "custo_total": pulp.value(problema.objective)
    }

    return resultado

def plotar_dieta(dados, titulo):
    labels = [f'Ingrediente {i+1}' for i in range(len(dados['quantidades']))]
    valores = dados['quantidades']

    fig, ax = plt.subplots()
    ax.bar(labels, valores)
    ax.set_ylabel('Quantidade utilizada')
    ax.set_title(titulo)
    plt.xticks(rotation=45)
    plt.show()

# Dados do problema
matriz_vitaminas = [
    [1, 0, 2, 2, 1, 2],
    [0, 1, 3, 1, 3, 2]
]

precos = [35, 30, 60, 50, 27, 22]
quantidades_minimas = [9, 19]

# Exemplo 1: Dados originais
dados_dieta1 = resolver_problema_dieta(matriz_vitaminas, precos, quantidades_minimas)

print("Problema da Dieta - Exemplo 1:")
print("Status:", dados_dieta1["status"])
for idx, qtd in enumerate(dados_dieta1["quantidades"]):
    print(f"Quantidade do Ingrediente {idx+1}: {qtd:.2f}")
print("Custo Total: R$", dados_dieta1["custo_total"])
plotar_dieta(dados_dieta1, "Composição da Dieta - Exemplo 1")
print("\n" + "="*50 + "\n")

# Exemplo 2: Aumentando as necessidades de vitaminas
quantidades_minimas2 = [15, 30]
dados_dieta2 = resolver_problema_dieta(matriz_vitaminas, precos, quantidades_minimas2)

print("\nProblema da Dieta - Exemplo 2:")
print("Status:", dados_dieta2["status"])
for idx, qtd in enumerate(dados_dieta2["quantidades"]):
    print(f"Quantidade do Ingrediente {idx+1}: {qtd:.2f}")
print("Custo Total: R$", dados_dieta2["custo_total"])
plotar_dieta(dados_dieta2, "Composição da Dieta - Exemplo 2")
print("\n" + "="*50 + "\n")

# Exemplo 3: Alterando os preços e exigências
precos3 = [45, 25, 65, 55, 25, 18]
quantidades_minimas3 = [10, 22]
dados_dieta3 = resolver_problema_dieta(matriz_vitaminas, precos3, quantidades_minimas3)

print("\nProblema da Dieta - Exemplo 3:")
print("Status:", dados_dieta3["status"])
for idx, qtd in enumerate(dados_dieta3["quantidades"]):
    print(f"Quantidade do Ingrediente {idx+1}: {qtd:.2f}")
print("Custo Total: R$", dados_dieta3["custo_total"])
plotar_dieta(dados_dieta3, "Composição da Dieta - Exemplo 3")
print("\n" + "="*50 + "\n")