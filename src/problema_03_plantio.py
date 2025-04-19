# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização linear
import matplotlib.pyplot as plt  # Para criar gráficos

# Função que calcula a melhor distribuição de culturas (milho, arroz, feijão) para maximizar o lucro
def resolver_problema_plantio(area_fazendas, agua_fazendas, area_maxima_cultura, agua_por_area, lucro_por_area):
    # Cria um problema para maximizar o lucro
    problema = pulp.LpProblem("Problema_Plantio", pulp.LpMaximize)

    # Define as variáveis: proporção da área para cada cultura (não negativa)
    milho = pulp.LpVariable('Milho', lowBound=0)  # Proporção para milho
    arroz = pulp.LpVariable('Arroz', lowBound=0)  # Proporção para arroz
    feijao = pulp.LpVariable('Feijao', lowBound=0)  # Proporção para feijão

    culturas = [milho, arroz, feijao]  # Lista das culturas

    # Calcula o lucro total, ponderado pela área de cada fazenda
    lucro_total = sum(
        sum(lucro_por_area[i] * culturas[i] * (area / sum(area_fazendas)) for i in range(3))
        for area in area_fazendas
    )
    problema += lucro_total, "Lucro_Total"  # Define o objetivo: maximizar o lucro

    # Adiciona restrições para cada fazenda
    for idx, (area, agua) in enumerate(zip(area_fazendas, agua_fazendas)):
        fator = area / sum(area_fazendas)  # Proporção da área da fazenda
        # Restrição de área: soma das áreas plantadas não pode exceder a área disponível
        problema += pulp.lpSum(culturas[i] * fator for i in range(3)) <= area, f"Area_Fazenda_{idx+1}"
        # Restrição de água: consumo de água pelas culturas não pode exceder a água disponível
        problema += pulp.lpSum(culturas[i] * agua_por_area[i] * fator for i in range(3)) <= agua, f"Agua_Fazenda_{idx+1}"

    # Restrições de área máxima para cada cultura
    for i in range(3):
        problema += culturas[i] * sum(area_fazendas) <= area_maxima_cultura[i], f"Area_Maxima_Cultura_{i+1}"

    # Resolve o problema
    problema.solve()

    # Organiza os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "milho": milho.varValue,  # Proporção da área para milho
        "arroz": arroz.varValue,  # Proporção da área para arroz
        "feijao": feijao.varValue,  # Proporção da área para feijão
        "lucro_total": pulp.value(problema.objective)  # Lucro total
    }

    return resultado  # Retorna os resultados

# Função para criar um gráfico de barras com a distribuição das culturas
def plotar_plantio(dados, titulo):
    labels = ['Milho', 'Arroz', 'Feijao']  # Nomes das culturas
    valores = [dados['milho'], dados['arroz'], dados['feijao']]  # Proporções de área

    fig, ax = plt.subplots()  # Cria uma figura
    ax.bar(labels, valores)  # Cria o gráfico de barras
    ax.set_ylabel('Proporção da área plantada')  # Nome do eixo Y
    ax.set_title(titulo)  # Título do gráfico
    plt.show()  # Exibe o gráfico

# Exemplo 1: Configuração inicial
area_fazendas = [400, 650, 350]  # Áreas disponíveis em cada fazenda
agua_fazendas = [1800, 2200, 950]  # Água disponível em cada fazenda
area_maxima_cultura = [660, 880, 400]  # Área máxima para milho, arroz e feijão
agua_por_area = [5.5, 4, 3.5]  # Consumo de água por unidade de área para cada cultura
lucro_por_area = [5000, 4000, 1800]  # Lucro por unidade de área para cada cultura

dados_plantio1 = resolver_problema_plantio(area_fazendas, agua_fazendas, area_maxima_cultura, agua_por_area, lucro_por_area)

# Mostra os resultados do Exemplo 1
print("Problema do Plantio - Exemplo 1:")
print("Status:", dados_plantio1["status"])  # Status da solução
print(f"Proporção da área para Milho: {dados_plantio1['milho']:.4f}")  # Área para milho
print(f"Proporção da área para Arroz: {dados_plantio1['arroz']:.4f}")  # Área para arroz
print(f"Proporção da área para Feijão: {dados_plantio1['feijao']:.4f}")  # Área para feijão
print("Lucro Total: R$", dados_plantio1["lucro_total"])  # Lucro total
plotar_plantio(dados_plantio1, "Distribuição de Plantio - Exemplo 1")  # Mostra o gráfico

# Exemplo 2: Mudança nas áreas e água das fazendas
data2_area_fazendas = [500, 400, 300]  # Novas áreas das fazendas
data2_agua_fazendas = [1500, 1400, 1000]  # Nova disponibilidade de água
area_maxima_cultura2 = [800, 700, 500]  # Novas áreas máximas para as culturas
dados_plantio2 = resolver_problema_plantio(data2_area_fazendas, data2_agua_fazendas, area_maxima_cultura2, agua_por_area, lucro_por_area)

# Mostra os resultados do Exemplo 2
print("\nProblema do Plantio - Exemplo 2:")
print("Status:", dados_plantio2["status"])
print(f"Proporção da área para Milho: {dados_plantio2['milho']:.4f}")
print(f"Proporção da área para Arroz: {dados_plantio2['arroz']:.4f}")
print(f"Proporção da área para Feijão: {dados_plantio2['feijao']:.4f}")
print("Lucro Total: R$", dados_plantio2["lucro_total"])
plotar_plantio(dados_plantio2, "Distribuição de Plantio - Exemplo 2")

# Exemplo 3: Mudança na água e nos lucros das culturas
data3_agua_fazendas = [1300, 1800, 900]  # Nova disponibilidade de água
lucro_por_area3 = [4000, 5500, 2500]  # Novos lucros por cultura
dados_plantio3 = resolver_problema_plantio(area_fazendas, data3_agua_fazendas, area_maxima_cultura, agua_por_area, lucro_por_area3)

# Mostra os resultados do Exemplo 3
print("\nProblema do Plantio - Exemplo 3:")
print("Status:", dados_plantio3["status"])
print(f"Proporção da área para Milho: {dados_plantio3['milho']:.4f}")
print(f"Proporção da área para Arroz: {dados_plantio3['arroz']:.4f}")
print(f"Proporção da área para Feijão: {dados_plantio3['feijao']:.4f}")
print("Lucro Total: R$", dados_plantio3["lucro_total"])
plotar_plantio(dados_plantio3, "Distribuição de Plantio - Exemplo 3")