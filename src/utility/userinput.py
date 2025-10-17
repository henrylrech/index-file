from classes.enums import Entry

def choose_entry_type():
    entry_type = input("""
Qual tipo de entrada deseja pesquisar?
1 - Pedido
2 - Produto
(pressione Enter para voltar ao menu)
Escolha uma opção: 
""")
    if entry_type.strip() == '':
        return None
    
    match entry_type:
        case '1':
            return Entry.ORDERENTRY
        case '2':
            return Entry.PRODUCTENTRY
        case _:
            print(f"Opção inválida: {entry_type}")
            return None
