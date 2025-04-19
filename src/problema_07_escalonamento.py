# Importa bibliotecas necessárias
import pulp  # Para resolver problemas de otimização linear
import matplotlib.pyplot as plt  # Para criar gráficos

# Função que calcula o menor número de enfermeiras necessário para atender à demanda semanal
def resolver_problema_escalonamento(demanda):
    dias = len(demanda)  # Número de dias na semana (7)
    # Cria um problema para minimizar o total de enfermeiras
    problema = pulp.LpProblem("Problema_Escalonamento", pulp.LpMinimize)

    # Cria variáveis: número de enfermeiras que começam a trabalhar em cada dia (inteiro, não negativo)
    x = {i: pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(dias)}

    # Define o objetivo: minimizar o total de enfermeiras (soma de todas que começam)
    problema += pulp.lpSum(x[i] for i in range(dias)), "Minimizar_total_enfermeiras"

    # Restrições: garantir que a demanda diária seja atendida
    # Cada enfermeira trabalha 5 dias consecutivos, começando em um dos últimos 5 dias
    for d in range(dias):
        problema += pulp.lpSum(x[(d - i) % dias] for i in range(5)) >= demanda[d], f"Demanda_dia_{d}"

    # Resolve o problema
    problema.solve()

    # Organiza os resultados em um dicionário
    resultado = {
        "status": pulp.LpStatus[problema.status],  # Status da solução (ex.: "Optimal")
        "inicio_enfermeiras": {i: x[i].varValue for i in range(dias)},  # Enfermeiras que começam em cada dia
        "total_enfermeiras": pulp.value(problema.objective)  # Total de enfermeiras
    }

    return resultado  # Retorna os resultados

# Função para criar um gráfico de barras mostrando as enfermeiras que começam em cada dia
def plotar_escalonamento(dados, titulo):
    dias = sorted(dados['inicio_enfermeiras'].keys())  # Lista de dias (0 a 6)
    valores = [dados['inicio_enfermeiras'][d] for d in dias]  # Número de enfermeiras por dia

    fig, ax = plt.subplots()  # Cria uma figura
    ax.bar(dias, valores, color='lightblue')  # Cria o gráfico de barras
    ax.set_xlabel('Dia da semana')  # Nome do eixo X
    ax.set_ylabel('Enfermeiras iniciando')  # Nome do eixo Y
    ax.set_title(titulo)  # Título do gráfico
    ax.set_xticks(dias)  # Define os ticks do eixo X
    ax.set_xticklabels(['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'])  # Rótulos dos dias
    plt.show()  # Exibe o gráfico

# Exemplo 1: Configuração inicial (demanda da apostila)
demanda1 = [17, 13, 15, 19, 14, 16, 11]  # Demanda de enfermeiras por dia (Domingo a Sábado)

print("\nProblema de Escalonamento de Horários - Exemplo 1:")
dados_escalonamento1 = resolver_problema_escalonamento(demanda1)
print("Status:", dados_escalonamento1["status"])  # Status da solução
for dia, valor in dados_escalonamento1["inicio_enfermeiras"].items():
    print(f"Dia {dia} - Enfermeiras iniciando: {valor:.0f}")  # Enfermeiras que começam em cada dia
print("Total de enfermeiras: ", dados_escalonamento1["total_enfermeiras"])  # Total de enfermeiras
plotar_escalonamento(dados_escalonamento1, "Escalonamento de Enfermeiras - Exemplo 1")  # Mostra o gráfico

# Exemplo 2: Demanda mais alta no meio da semana
demanda2 = [10, 12, 20, 25, 23, 18, 14]  # Nova demanda com pico na quarta e quinta

print("\nProblema de Escalonamento de Horários - Exemplo 2:")
dados_escalonamento2 = resolver_problema_escalonamento(demanda2)
print("Status:", dados_escalonamento2["status"])
for dia, valor in dados_escalonamento2["inicio_enfermeiras"].items():
    print(f"Dia {dia} - Enfermeiras iniciando: {valor:.0f}")
print("Total de enfermeiras: ", dados_escalonamento2["total_enfermeiras"])
plotar_escalonamento(dados_escalonamento2, "Escalonamento de Enfermeiras - Exemplo 2")

# Exemplo 3: Demanda alta no fim de semana
demanda3 = [8, 9, 11, 10, 12, 20, 22]  # Nova demanda com pico na sexta e sábado

print("\nProblema de Escalonamento de Horários - Exemplo 3:")
dados_escalonamento3 = resolver_problema_escalonamento(demanda3)
print("Status:", dados_escalonamento3["status"])
for dia, valor in dados_escalonamento3["inicio_enfermeiras"].items():
    print(f"Dia {dia} - Enfermeiras iniciando: {valor:.0f}")
print("Total de enfermeiras: ", dados_escalonamento3["total_enfermeiras"])
plotar_escalonamento(dados_escalonamento3, "Escalonamento de Enfermeiras - Exemplo 3")