def main():
    while True:
        print("="*50)
        print("LISTA DE PESQUISA OPERACIONAL E OTIMIZAÇÃO")
        print("EXERCÍCIO 02")
        print("="*50)
        print("\n")
        print("Todos os exercícios resolvidos (problemas 1 até 13) vieram do material (problemas.md.slides.pdf).")
        print("Esse material está disponível para download no site pessoal do professor Rian e foi utilizado em sala de aula")
        print("para a introdução e prática dos conceitos de Pesquisa Operacional e Otimização.")
        print("Cada atividade possui um total de 1 exemplo utilizado do material original e 2 exemplos adicionais desenvolvidos")
        print("para demonstrar o funcionamento prático dos modelos.")
        print("Abaixo estão os problemas resolvidos, organizados e prontos para execução individual.")
        print("\n")
        print("="*50)
        print("MENU DE PROBLEMAS")
        print("="*50)
        print("1. Problema da Ração")
        print("2. Problema da Dieta")
        print("3. Problema do Plantio")
        print("4. Problema das Tintas")
        print("5. Problema do Transporte")
        print("6. Problema do Fluxo Máximo")
        print("7. Problema de Escalonamento de Horários")
        print("8. Problema de Cobertura")
        print("9. Problema da Mochila")
        print("10. Problema dos Padrões")
        print("0. Sair")

        escolha = input("\nDigite o número do problema que deseja executar: ")

        if escolha == "0":
            print("Encerrando o programa.")
            break
        elif escolha == "1":
            import src.problema_01_racao
        elif escolha == "2":
            import src.problema_02_dieta
        elif escolha == "3":
            import src.problema_03_plantio
        elif escolha == "4":
            import src.problema_04_tintas
        elif escolha == "5":
            import src.problema_05_transporte
        elif escolha == "6":
            import src.problema_06_fluxo_maximo
        elif escolha == "7":
            import src.problema_07_escalonamento
        elif escolha == "8":
            import src.problema_08_cobertura
        elif escolha == "9":
            import src.problema_09_mochila
        elif escolha == "10":
            import src.problema_10_padroes
        elif escolha == "11":
            import src.problema_11_facilidades
        elif escolha == "12":
            import src.problema_12_frequencia                        
        elif escolha == "13":
            import src.problema_13_clique_maxima                        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

