# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização linear
import matplotlib.pyplot as plt  # Para criar gráficos

# Função que calcula a quantidade de cada produto (latinhas) a produzir para maximizar o lucro
def resolver_problema_padroes(consumos, lucros, material_disponivel):
    # Cria um problema para maximizar o lucro total
    problema = pulp.LpProblem("Problema_Padroes", pulp.LpMaximize)

    produtos = list(consumos.keys())  # Lista de produtos (ex.: Pequena, Media, Grande)
    # Cria variáveis: quantidade de cada produto a produzir (inteiro, não negativo)
    x = {p: pulp.LpVariable(f"x_{p}", lowBound=0, cat='Integer') for p in produtos}

    # Define o objetivo: maximizar o lucro total (lucro por unidade * quantidade)
    problema += pulp.lpSum(lucros[p] * x[p] for p in produtos), "Maximizar_Lucro"
    # Restrição: o consumo total de material não pode exceder o disponível
    problema += pulp.lpSum(consumos[p] * x[p] for p in produtos) <= material_disponivel, "Restricao_Material"

    # Resolve o problema
    problema.solve()

    # Organiza os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "quantidade_produtos": {p: x[p].varValue for p in produtos},  # Quantidade de cada produto
        "lucro_total": pulp.value(problema.objective)  # Lucro total
    }

    return resultado  # Retorna os resultados

# Função para criar um gráfico de barras mostrando a quantidade produzida de cada produto
def plotar_padroes(quantidade_produtos, titulo):
    produtos = list(quantidade_produtos.keys())  # Nomes dos produtos
    quantidades = [quantidade_produtos[p] for p in produtos]  # Quantidades produzidas

    fig, ax = plt.subplots()  # Cria uma figura
    ax.bar(produtos, quantidades, color='lightgreen')  # Cria o gráfico de barras
    plt.xlabel('Produtos')  # Nome do eixo X
    plt.ylabel('Quantidade Produzida')  # Nome do eixo Y
    plt.title(titulo)  # Título do gráfico
    plt.show()  # Exibe o gráfico

# Exemplo 1: Configuração inicial
consumos1 = {'Pequena': 2, 'Media': 3, 'Grande': 5}  # Consumo de material por unidade
lucros1 = {'Pequena': 1, 'Media': 2, 'Grande': 4}  # Lucro por unidade
material_disponivel1 = 1000  # Material disponível

dados_padroes1 = resolver_problema_padroes(consumos1, lucros1, material_disponivel1)

print("\nProblema de Padroes - Exemplo 1:")
print("Status:", dados_padroes1["status"])  # Status da solução
print("Quantidade produzida:", dados_padroes1["quantidade_produtos"])  # Quantidade de cada produto
print("Lucro total: R$", dados_padroes1["lucro_total"])  # Lucro total
plotar_padroes(dados_padroes1['quantidade_produtos'], "Padroes de Produção - Exemplo 1")  # Mostra o gráfico

# Exemplo 2: Novo conjunto de dados
consumos2 = {'Latinha A': 4, 'Latinha B': 5, 'Latinha C': 7}  # Consumo de material
lucros2 = {'Latinha A': 3, 'Latinha B': 5, 'Latinha C': 8}  # Lucro por unidade
material_disponivel2 = 500  # Material disponível

dados_padroes2 = resolver_problema_padroes(consumos2, lucros2, material_disponivel2)

print("\nProblema de Padroes - Exemplo 2:")
print("Status:", dados_padroes2["status"])
print("Quantidade produzida:", dados_padroes2["quantidade_produtos"])
print("Lucro total: R$", dados_padroes2["lucro_total"])
plotar_padroes(dados_padroes2['quantidade_produtos'], "Padroes de Produção - Exemplo 2")

# Exemplo 3: Conjunto com consumos e lucros mais altos
consumos3 = {'Tipo X': 6, 'Tipo Y': 9, 'Tipo Z': 12}  # Consumo de material
lucros3 = {'Tipo X': 5, 'Tipo Y': 7, 'Tipo Z': 10}  # Lucro por unidade
material_disponivel3 = 720  # Material disponível

dados_padroes3 = resolver_problema_padroes(consumos3, lucros3, material_disponivel3)

print("\nProblema de Padroes - Exemplo 3:")
print("Status:", dados_padroes3["status"])
print("Quantidade produzida:", dados_padroes3["quantidade_produtos"])
print("Lucro total: R$", dados_padroes3["lucro_total"])
plotar_padroes(dados_padroes3['quantidade_produtos'], "Padroes de Produção - Exemplo 3")