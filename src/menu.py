from classes.enums import Entry
import file_management as fm

def _print_options():
    print("<--------------------------------< Menu >-------------------------------->")
    print("1 - Construir arquivos não ordenados (Leitura do dataset .csv)")
    print("2 - Construir arquivos ordenados")
    print("3 - Construir índices")
    print("4 - Leitura de arquivos binários")
    print("5 - Pesquisa de pedidos por ID (usando índice)")
    print("0 - Sair")
    print("<------------------------------------------------------------------------>")
    print("Escolha uma opção:")

def menu():
    while True:
        _print_options()
        choice = input()

        if choice == '0' or choice == '':
            print("Saindo...")
            break
        elif choice == '1':
            chunk_size = input("Quantas linhas por chunk? (pressione Enter para padrão 50): ")
            if chunk_size.strip() == '':
                chunk_size = 50
            else:
                try:
                    chunk_size = int(chunk_size)
                except ValueError:
                    print("Entrada inválida. Usando tamanho de chunk padrão 50.")
                    chunk_size = 50

            fm.write_unordered_files(chunk_size)

        elif choice == '2':
            fm.order_files()
        elif choice == '3':
            every_n = input("Criar índice a cada quantos registros? (pressione Enter para padrão 10): ")
            if every_n.strip() == '':
                every_n = 10
            else:
                try:
                    every_n = int(every_n)
                except ValueError:
                    print("Entrada inválida. Usando valor padrão 10.")
                    every_n = 10

            fm.build_indexes(every_n)
        elif choice == '4':
            file_id = input("""
Qual arquivo deseja ler? 
1 - arquivo de pedidos não ordenado
2 - arquivo de produtos não ordenado
3 - arquivo de pedidos ordenado
4 - arquivo de produtos ordenado
5 - índice de pedidos
6 - índice de produtos
(pressione Enter para voltar ao menu)
Escolha uma opção: 
""")
            if file_id.strip() == '':
                continue
            fm.read_entire_file(file_id)
        elif choice == '5':
            order_id = input("Digite o ID do pedido a ser pesquisado (pressione Enter para voltar ao menu): ")
            if order_id.strip() == '':
                continue
            try:
                order_id = int(order_id)
            except ValueError:
                print("ID inválido. Deve ser um número inteiro.")
                continue
            fm.search(Entry.ORDERENTRY, order_id)
        else:
            print("Opção inválida. Tente novamente.")
    
