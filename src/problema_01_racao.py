import pulp
import matplotlib.pyplot as plt

def resolver_problema_racao(custo_cereal, custo_carne, preco_amgs, preco_re, 
                             consumo_amgs_cereal, consumo_amgs_carne, 
                             consumo_re_cereal, consumo_re_carne,
                             disponibilidade_cereal, disponibilidade_carne):
    # Criar o problema de maximização
    problema = pulp.LpProblem("Problema_Generico_Racao", pulp.LpMaximize)

    # Variáveis de decisão
    amgs = pulp.LpVariable('AMGS', lowBound=0, cat='Integer')  # Quantidade de All Mega Giga Suprema
    re = pulp.LpVariable('RE', lowBound=0, cat='Integer')      # Quantidade de Ração das Estrelas

    # Função objetivo: maximizar o lucro
    custo_amgs = consumo_amgs_cereal * custo_cereal + consumo_amgs_carne * custo_carne
    custo_re = consumo_re_cereal * custo_cereal + consumo_re_carne * custo_carne

    lucro_amgs = preco_amgs - custo_amgs
    lucro_re = preco_re - custo_re

    problema += lucro_amgs * amgs + lucro_re * re, "Lucro_Total"

    # Restrições de recursos
    problema += consumo_amgs_cereal * amgs + consumo_re_cereal * re <= disponibilidade_cereal, "Restricao_Cereais"
    problema += consumo_amgs_carne * amgs + consumo_re_carne * re <= disponibilidade_carne, "Restricao_Carne"

    # Resolver o problema
    problema.solve()

    # Resultados
    resultado = {
        "status": pulp.LpStatus[problema.status],
        "quantidade_amgs": amgs.varValue,
        "quantidade_re": re.varValue,
        "lucro_total": pulp.value(problema.objective)
    }

    return resultado

def plotar_resultado(dados, titulo):
    labels = ['AMGS', 'RE']
    valores = [dados['quantidade_amgs'], dados['quantidade_re']]

    fig, ax = plt.subplots()
    ax.bar(labels, valores)
    ax.set_ylabel('Quantidade Produzida')
    ax.set_title(titulo)
    plt.show()

# Exemplo 1: Dados originais
dados_exemplo1 = resolver_problema_racao(
    custo_cereal=1, custo_carne=4,
    preco_amgs=20, preco_re=30,
    consumo_amgs_cereal=5, consumo_amgs_carne=1,
    consumo_re_cereal=2, consumo_re_carne=4,
    disponibilidade_cereal=30000, disponibilidade_carne=10000
)

print("Exemplo 1:")
print("Status:", dados_exemplo1["status"])
print("Quantidade de AMGS a produzir:", dados_exemplo1["quantidade_amgs"])
print("Quantidade de RE a produzir:", dados_exemplo1["quantidade_re"])
print("Lucro Total: R$", dados_exemplo1["lucro_total"])
plotar_resultado(dados_exemplo1, "Produção - Exemplo 1")
print("\n" + "="*50 + "\n")

# Exemplo 2: Cenário com aumento do preço do AMGS
dados_exemplo2 = resolver_problema_racao(
    custo_cereal=1, custo_carne=4,
    preco_amgs=25, preco_re=30,
    consumo_amgs_cereal=5, consumo_amgs_carne=1,
    consumo_re_cereal=2, consumo_re_carne=4,
    disponibilidade_cereal=30000, disponibilidade_carne=10000
)

print("\nExemplo 2:")
print("Status:", dados_exemplo2["status"])
print("Quantidade de AMGS a produzir:", dados_exemplo2["quantidade_amgs"])
print("Quantidade de RE a produzir:", dados_exemplo2["quantidade_re"])
print("Lucro Total: R$", dados_exemplo2["lucro_total"])
plotar_resultado(dados_exemplo2, "Produção - Exemplo 2")
print("\n" + "="*50 + "\n")

# Exemplo 3: Cenário com redução na disponibilidade de carne
dados_exemplo3 = resolver_problema_racao(
    custo_cereal=1, custo_carne=4,
    preco_amgs=20, preco_re=30,
    consumo_amgs_cereal=5, consumo_amgs_carne=1,
    consumo_re_cereal=2, consumo_re_carne=4,
    disponibilidade_cereal=30000, disponibilidade_carne=7000
)

print("\nExemplo 3:")
print("Status:", dados_exemplo3["status"])
print("Quantidade de AMGS a produzir:", dados_exemplo3["quantidade_amgs"])
print("Quantidade de RE a produzir:", dados_exemplo3["quantidade_re"])
print("Lucro Total: R$", dados_exemplo3["lucro_total"])
plotar_resultado(dados_exemplo3, "Produção - Exemplo 3")
print("\n" + "="*50 + "\n")