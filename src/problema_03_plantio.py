import pulp
import matplotlib.pyplot as plt

def resolver_problema_plantio(area_fazendas, agua_fazendas, area_maxima_cultura, agua_por_area, lucro_por_area):
    problema = pulp.LpProblem("Problema_Plantio", pulp.LpMaximize)

    milho = pulp.LpVariable('Milho', lowBound=0)
    arroz = pulp.LpVariable('Arroz', lowBound=0)
    feijao = pulp.LpVariable('Feijao', lowBound=0)

    culturas = [milho, arroz, feijao]

    lucro_total = sum(
        sum(lucro_por_area[i] * culturas[i] * (area / sum(area_fazendas)) for i in range(3))
        for area in area_fazendas
    )
    problema += lucro_total, "Lucro_Total"

    for idx, (area, agua) in enumerate(zip(area_fazendas, agua_fazendas)):
        fator = area / sum(area_fazendas)
        problema += pulp.lpSum(culturas[i] * fator for i in range(3)) <= area, f"Area_Fazenda_{idx+1}"
        problema += pulp.lpSum(culturas[i] * agua_por_area[i] * fator for i in range(3)) <= agua, f"Agua_Fazenda_{idx+1}"

    for i in range(3):
        problema += culturas[i] * sum(area_fazendas) <= area_maxima_cultura[i], f"Area_Maxima_Cultura_{i+1}"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "milho": milho.varValue,
        "arroz": arroz.varValue,
        "feijao": feijao.varValue,
        "lucro_total": pulp.value(problema.objective)
    }

    return resultado

def plotar_plantio(dados, titulo):
    labels = ['Milho', 'Arroz', 'Feijao']
    valores = [dados['milho'], dados['arroz'], dados['feijao']]

    fig, ax = plt.subplots()
    ax.bar(labels, valores)
    ax.set_ylabel('Proporção da área plantada')
    ax.set_title(titulo)
    plt.show()

# Exemplo 1: Dados originais
area_fazendas = [400, 650, 350]
agua_fazendas = [1800, 2200, 950]
area_maxima_cultura = [660, 880, 400]
agua_por_area = [5.5, 4, 3.5]
lucro_por_area = [5000, 4000, 1800]

dados_plantio1 = resolver_problema_plantio(area_fazendas, agua_fazendas, area_maxima_cultura, agua_por_area, lucro_por_area)

print("Problema do Plantio - Exemplo 1:")
print("Status:", dados_plantio1["status"])
print(f"Proporção da área para Milho: {dados_plantio1['milho']:.4f}")
print(f"Proporção da área para Arroz: {dados_plantio1['arroz']:.4f}")
print(f"Proporção da área para Feijão: {dados_plantio1['feijao']:.4f}")
print("Lucro Total: R$", dados_plantio1["lucro_total"])
plotar_plantio(dados_plantio1, "Distribuição de Plantio - Exemplo 1")

# Exemplo 2: Mudando mais drasticamente as áreas e água das fazendas
data2_area_fazendas = [500, 400, 300]
data2_agua_fazendas = [1500, 1400, 1000]
area_maxima_cultura2 = [800, 700, 500]
dados_plantio2 = resolver_problema_plantio(data2_area_fazendas, data2_agua_fazendas, area_maxima_cultura2, agua_por_area, lucro_por_area)

print("\nProblema do Plantio - Exemplo 2:")
print("Status:", dados_plantio2["status"])
print(f"Proporção da área para Milho: {dados_plantio2['milho']:.4f}")
print(f"Proporção da área para Arroz: {dados_plantio2['arroz']:.4f}")
print(f"Proporção da área para Feijão: {dados_plantio2['feijao']:.4f}")
print("Lucro Total: R$", dados_plantio2["lucro_total"])
plotar_plantio(dados_plantio2, "Distribuição de Plantio - Exemplo 2")

# Exemplo 3: Mudando água e lucro das culturas
data3_agua_fazendas = [1300, 1800, 900]
lucro_por_area3 = [4000, 5500, 2500]
dados_plantio3 = resolver_problema_plantio(area_fazendas, data3_agua_fazendas, area_maxima_cultura, agua_por_area, lucro_por_area3)

print("\nProblema do Plantio - Exemplo 3:")
print("Status:", dados_plantio3["status"])
print(f"Proporção da área para Milho: {dados_plantio3['milho']:.4f}")
print(f"Proporção da área para Arroz: {dados_plantio3['arroz']:.4f}")
print(f"Proporção da área para Feijão: {dados_plantio3['feijao']:.4f}")
print("Lucro Total: R$", dados_plantio3["lucro_total"])
plotar_plantio(dados_plantio3, "Distribuição de Plantio - Exemplo 3")
