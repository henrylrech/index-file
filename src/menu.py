import file_management as fm

def _print_options():
    print("<----------------< Menu >---------------->")
    print("1 - Construir arquivos não ordenados")
    print("2 - Construir arquivos ordenados")
    print("0 - Sair")
    print("<---------------------------------------->")
    print("Escolha uma opção:")

def menu():
    while True:
        _print_options()
        choice = input()

        if choice == '0':
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
        else:
            print("Opção inválida. Tente novamente.")
    
