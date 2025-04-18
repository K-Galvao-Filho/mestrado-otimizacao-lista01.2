import pulp
import matplotlib.pyplot as plt

def resolver_problema_tintas(custos, composicao_sec, composicao_cor, demanda_sr, demanda_sn, exigencias=None):
    problema = pulp.LpProblem("Problema_Tintas", pulp.LpMinimize)

    variaveis = {}
    produtos = ['SolA', 'SolB', 'SEC', 'COR']
    tintas = ['SR', 'SN']

    for produto in produtos:
        for tinta in tintas:
            variaveis[(produto, tinta)] = pulp.LpVariable(f"{produto}_{tinta}", lowBound=0)

    problema += pulp.lpSum(custos[produto] * variaveis[(produto, tinta)] for produto in produtos for tinta in tintas), "Custo_Total"

    problema += pulp.lpSum(variaveis[(produto, 'SR')] for produto in produtos) == demanda_sr, "Demanda_SR"
    problema += pulp.lpSum(variaveis[(produto, 'SN')] for produto in produtos) == demanda_sn, "Demanda_SN"

    exigencias = exigencias or {'SR': (0.25, 0.50), 'SN': (0.20, 0.50)}

    problema += pulp.lpSum(composicao_sec[produto] * variaveis[(produto, 'SR')] for produto in produtos) >= exigencias['SR'][0] * demanda_sr, "SEC_minima_SR"
    problema += pulp.lpSum(composicao_cor[produto] * variaveis[(produto, 'SR')] for produto in produtos) >= exigencias['SR'][1] * demanda_sr, "COR_minima_SR"

    problema += pulp.lpSum(composicao_sec[produto] * variaveis[(produto, 'SN')] for produto in produtos) >= exigencias['SN'][0] * demanda_sn, "SEC_minima_SN"
    problema += pulp.lpSum(composicao_cor[produto] * variaveis[(produto, 'SN')] for produto in produtos) >= exigencias['SN'][1] * demanda_sn, "COR_minima_SN"

    problema.solve()

    resultado = {
        "status": pulp.LpStatus[problema.status],
        "quantidades": {(produto, tinta): variaveis[(produto, tinta)].varValue for produto in produtos for tinta in tintas},
        "custo_total": pulp.value(problema.objective)
    }

    return resultado

def plotar_tintas(dados, titulo):
    produtos_tinta = ['SolA_SR', 'SolB_SR', 'SEC_SR', 'COR_SR', 'SolA_SN', 'SolB_SN', 'SEC_SN', 'COR_SN']
    valores = [dados['quantidades'][tuple(p.split('_'))] for p in produtos_tinta]

    fig, ax = plt.subplots()
    ax.bar(produtos_tinta, valores)
    ax.set_ylabel('Litros utilizados')
    ax.set_title(titulo)
    plt.xticks(rotation=45)
    plt.show()

# Exemplo 1: Dados originais
custos1 = {'SolA': 1.5, 'SolB': 1.0, 'SEC': 4.0, 'COR': 6.0}
composicao_sec1 = {'SolA': 0.3, 'SolB': 0.6, 'SEC': 1.0, 'COR': 0.0}
composicao_cor1 = {'SolA': 0.7, 'SolB': 0.4, 'SEC': 0.0, 'COR': 1.0}

demanda_sr1 = 1000
demanda_sn1 = 250

# Resolver Exemplo 1
dados_tintas1 = resolver_problema_tintas(custos1, composicao_sec1, composicao_cor1, demanda_sr1, demanda_sn1)

print("Problema das Tintas - Exemplo 1:")
print("Status:", dados_tintas1["status"])
for chave, valor in dados_tintas1["quantidades"].items():
    print(f"Quantidade de {chave[0]} para {chave[1]}: {valor:.2f} litros")
print("Custo Total: R$", dados_tintas1["custo_total"])
plotar_tintas(dados_tintas1, "Composição das Tintas - Exemplo 1")

# Exemplo 2: Custos modificados
custos2 = {'SolA': 2.5, 'SolB': 1.8, 'SEC': 6.0, 'COR': 7.5}
composicao_sec2 = {'SolA': 0.25, 'SolB': 0.55, 'SEC': 1.0, 'COR': 0.0}
composicao_cor2 = {'SolA': 0.75, 'SolB': 0.45, 'SEC': 0.0, 'COR': 1.0}

demanda_sr2 = 900
demanda_sn2 = 300

# Resolver Exemplo 2
dados_tintas2 = resolver_problema_tintas(custos2, composicao_sec2, composicao_cor2, demanda_sr2, demanda_sn2)

print("\nProblema das Tintas - Exemplo 2:")
print("Status:", dados_tintas2["status"])
for chave, valor in dados_tintas2["quantidades"].items():
    print(f"Quantidade de {chave[0]} para {chave[1]}: {valor:.2f} litros")
print("Custo Total: R$", dados_tintas2["custo_total"])
plotar_tintas(dados_tintas2, "Composição das Tintas - Exemplo 2")

# Exemplo 3: Exigências mais rigorosas
custos3 = {'SolA': 1.5, 'SolB': 1.0, 'SEC': 4.0, 'COR': 6.0}
composicao_sec3 = {'SolA': 0.4, 'SolB': 0.5, 'SEC': 1.0, 'COR': 0.0}
composicao_cor3 = {'SolA': 0.6, 'SolB': 0.5, 'SEC': 0.0, 'COR': 1.0}

demanda_sr3 = 1000
demanda_sn3 = 250
exigencias3 = {'SR': (0.30, 0.60), 'SN': (0.25, 0.55)}

# Resolver Exemplo 3
dados_tintas3 = resolver_problema_tintas(custos3, composicao_sec3, composicao_cor3, demanda_sr3, demanda_sn3, exigencias3)

print("\nProblema das Tintas - Exemplo 3:")
print("Status:", dados_tintas3["status"])
for chave, valor in dados_tintas3["quantidades"].items():
    print(f"Quantidade de {chave[0]} para {chave[1]}: {valor:.2f} litros")
print("Custo Total: R$", dados_tintas3["custo_total"])
plotar_tintas(dados_tintas3, "Composição das Tintas - Exemplo 3")

# Exemplo 4 ajustado: Forçando uso de SEC e COR puros (agora viável)
custos4 = {'SolA': 2.0, 'SolB': 2.5, 'SEC': 3.5, 'COR': 4.0}
composicao_sec4 = {'SolA': 0.2, 'SolB': 0.3, 'SEC': 1.0, 'COR': 0.0}
composicao_cor4 = {'SolA': 0.8, 'SolB': 0.7, 'SEC': 0.0, 'COR': 1.0}

demanda_sr4 = 1000
demanda_sn4 = 250
exigencias4 = {'SR': (0.35, 0.65), 'SN': (0.30, 0.55)}

# Resolver Exemplo 4
dados_tintas4 = resolver_problema_tintas(custos4, composicao_sec4, composicao_cor4, demanda_sr4, demanda_sn4, exigencias4)

print("\nProblema das Tintas - Exemplo 4:")
print("Status:", dados_tintas4["status"])
for chave, valor in dados_tintas4["quantidades"].items():
    print(f"Quantidade de {chave[0]} para {chave[1]}: {valor:.2f} litros")
print("Custo Total: R$", dados_tintas4["custo_total"])
plotar_tintas(dados_tintas4, "Composição das Tintas - Exemplo 4")
