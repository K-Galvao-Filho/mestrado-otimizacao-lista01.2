# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização
import matplotlib.pyplot as plt  # Para criar gráficos

# Função que calcula a melhor quantidade de rações a produzir
def resolver_problema_racao(custo_cereal, custo_carne, preco_amgs, preco_re, 
                             consumo_amgs_cereal, consumo_amgs_carne, 
                             consumo_re_cereal, consumo_re_carne,
                             disponibilidade_cereal, disponibilidade_carne):
    # Cria um problema para maximizar o lucro
    problema = pulp.LpProblem("Problema_Generico_Racao", pulp.LpMaximize)

    # Define as variáveis: quantas unidades de AMGS e RE produzir
    amgs = pulp.LpVariable('AMGS', lowBound=0, cat='Integer')  # Quantidade de All Mega Giga Suprema (inteiro ≥ 0)
    re = pulp.LpVariable('RE', lowBound=0, cat='Integer')      # Quantidade de Ração das Estrelas (inteiro ≥ 0)

    # Calcula o custo de produção de cada ração
    custo_amgs = consumo_amgs_cereal * custo_cereal + consumo_amgs_carne * custo_carne  # Custo de 1 AMGS
    custo_re = consumo_re_cereal * custo_cereal + consumo_re_carne * custo_carne       # Custo de 1 RE

    # Calcula o lucro por unidade (preço de venda - custo)
    lucro_amgs = preco_amgs - custo_amgs  # Lucro de 1 AMGS
    lucro_re = preco_re - custo_re        # Lucro de 1 RE

    # Define o objetivo: maximizar o lucro total
    problema += lucro_amgs * amgs + lucro_re * re, "Lucro_Total"

    # Define as restrições: não usar mais ingredientes do que o disponível
    problema += consumo_amgs_cereal * amgs + consumo_re_cereal * re <= disponibilidade_cereal, "Restricao_Cereais"
    problema += consumo_amgs_carne * amgs + consumo_re_carne * re <= disponibilidade_carne, "Restricao_Carne"

    # Resolve o problema
    problema.solve()

    # Salva os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "quantidade_amgs": amgs.varValue,          # Quantidade de AMGS a  # Quantidade ideal de AMGS
        "quantidade_re": re.varValue,              # Quantidade ideal de RE
        "lucro_total": pulp.value(problema.objective)  # Lucro total
    }

    return resultado  # Retorna os resultados

# Função para criar um gráfico com os resultados
def plotar_resultado(dados, titulo):
    labels = ['AMGS', 'RE']  # Nomes das rações
    valores = [dados['quantidade_amgs'], dados['quantidade_re']]  # Quantidades produzidas

    fig, ax = plt.subplots()  # Cria uma figura
    ax.bar(labels, valores)   # Cria barras com as quantidades
    ax.set_ylabel('Quantidade Produzida')  # Nome do eixo Y
    ax.set_title(titulo)      # Título do gráfico
    plt.show()                # Mostra o gráfico

# Exemplo 1: Configuração inicial
dados_exemplo1 = resolver_problema_racao(
    custo_cereal=1, custo_carne=4,  # Custos dos ingredientes
    preco_amgs=20, preco_re=30,     # Preços de venda
    consumo_amgs_cereal=5, consumo_amgs_carne=1,  # Ingredientes por AMGS
    consumo_re_cereal=2, consumo_re_carne=4,      # Ingredientes por RE
    disponibilidade_cereal=30000, disponibilidade_carne=10000  # Estoque de ingredientes
)

# Mostra os resultados do Exemplo 1
print("Exemplo 1:")
print("Status:", dados_exemplo1["status"])  # Status da solução
print("Quantidade de AMGS a produzir:", dados_exemplo1["quantidade_amgs"])  # Unidades de AMGS
print("Quantidade de RE a produzir:", dados_exemplo1["quantidade_re"])      # Unidades de RE
print("Lucro Total: R$", dados_exemplo1["lucro_total"])  # Lucro obtido
plotar_resultado(dados_exemplo1, "Produção - Exemplo 1")  # Mostra o gráfico
print("\n" + "="*50 + "\n")  # Separador

# Exemplo 2: Mesmo cenário, mas com preço do AMGS maior
dados_exemplo2 = resolver_problema_racao(
    custo_cereal=1, custo_carne=4,
    preco_amgs=25, preco_re=30,  # AMGS mais caro
    consumo_amgs_cereal=5, consumo_amgs_carne=1,
    consumo_re_cereal=2, consumo_re_carne=4,
    disponibilidade_cereal=30000, disponibilidade_carne=10000
)

# Mostra os resultados do Exemplo 2
print("\nExemplo 2:")
print("Status:", dados_exemplo2["status"])
print("Quantidade de AMGS a produzir:", dados_exemplo2["quantidade_amgs"])
print("Quantidade de RE a produzir:", dados_exemplo2["quantidade_re"])
print("Lucro Total: R$", dados_exemplo2["lucro_total"])
plotar_resultado(dados_exemplo2, "Produção - Exemplo 2")
print("\n" + "="*50 + "\n")

# Exemplo 3: Mesmo cenário do Exemplo 1, mas com menos carne disponível
dados_exemplo3 = resolver_problema_racao(
    custo_cereal=1, custo_carne=4,
    preco_amgs=20, preco_re=30,
    consumo_amgs_cereal=5, consumo_amgs_carne=1,
    consumo_re_cereal=2, consumo_re_carne=4,
    disponibilidade_cereal=30000, disponibilidade_carne=7000  # Menos carne
)

# Mostra os resultados do Exemplo 3
print("\nExemplo 3:")
print("Status:", dados_exemplo3["status"])
print("Quantidade de AMGS a produzir:", dados_exemplo3["quantidade_amgs"])
print("Quantidade de RE a produzir:", dados_exemplo3["quantidade_re"])
print("Lucro Total: R$", dados_exemplo3["lucro_total"])
plotar_resultado(dados_exemplo3, "Produção - Exemplo 3")
print("\n" + "="*50 + "\n")