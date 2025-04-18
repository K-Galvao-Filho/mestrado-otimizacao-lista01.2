import pulp
import matplotlib.pyplot as plt

# Função para resolver o problema de padrões (latinhas)
def resolver_problema_padroes(consumos, lucros, material_disponivel):
    problema = pulp.LpProblem("Problema_Padroes", pulp.LpMaximize)

    produtos = list(consumos.keys())
    x = {p: pulp.LpVariable(f"x_{p}", lowBound=0, cat='Integer') for p in produtos}

    problema += pulp.lpSum(lucros[p] * x[p] for p in produtos), "Maximizar_Lucro"
    problema += pulp.lpSum(consumos[p] * x[p] for p in produtos) <= material_disponivel, "Restricao_Material"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "quantidade_produtos": {p: x[p].varValue for p in produtos},
        "lucro_total": pulp.value(problema.objective)
    }

    return resultado

# Função para plotar os produtos produzidos
def plotar_padroes(quantidade_produtos, titulo):
    produtos = list(quantidade_produtos.keys())
    quantidades = [quantidade_produtos[p] for p in produtos]

    fig, ax = plt.subplots()
    ax.bar(produtos, quantidades, color='lightgreen')
    plt.xlabel('Produtos')
    plt.ylabel('Quantidade Produzida')
    plt.title(titulo)
    plt.show()

# Exemplo 1: Dados do problema
consumos1 = {'Pequena': 2, 'Media': 3, 'Grande': 5}
lucros1 = {'Pequena': 1, 'Media': 2, 'Grande': 4}
material_disponivel1 = 1000

dados_padroes1 = resolver_problema_padroes(consumos1, lucros1, material_disponivel1)

print("\nProblema de Padroes - Exemplo 1:")
print("Status:", dados_padroes1["status"])
print("Quantidade produzida:", dados_padroes1["quantidade_produtos"])
print("Lucro total: R$", dados_padroes1["lucro_total"])
plotar_padroes(dados_padroes1['quantidade_produtos'], "Padroes de Produção - Exemplo 1")

# Exemplo 2: Novo conjunto de dados
consumos2 = {'Latinha A': 4, 'Latinha B': 5, 'Latinha C': 7}
lucros2 = {'Latinha A': 3, 'Latinha B': 5, 'Latinha C': 8}
material_disponivel2 = 500

dados_padroes2 = resolver_problema_padroes(consumos2, lucros2, material_disponivel2)

print("\nProblema de Padroes - Exemplo 2:")
print("Status:", dados_padroes2["status"])
print("Quantidade produzida:", dados_padroes2["quantidade_produtos"])
print("Lucro total: R$", dados_padroes2["lucro_total"])
plotar_padroes(dados_padroes2['quantidade_produtos'], "Padroes de Produção - Exemplo 2")

# Exemplo 3: Outro conjunto variado
consumos3 = {'Tipo X': 6, 'Tipo Y': 9, 'Tipo Z': 12}
lucros3 = {'Tipo X': 5, 'Tipo Y': 7, 'Tipo Z': 10}
material_disponivel3 = 720

dados_padroes3 = resolver_problema_padroes(consumos3, lucros3, material_disponivel3)

print("\nProblema de Padroes - Exemplo 3:")
print("Status:", dados_padroes3["status"])
print("Quantidade produzida:", dados_padroes3["quantidade_produtos"])
print("Lucro total: R$", dados_padroes3["lucro_total"])
plotar_padroes(dados_padroes3['quantidade_produtos'], "Padroes de Produção - Exemplo 3")