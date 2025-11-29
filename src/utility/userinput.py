from classes.enums import Entry

def choose_entry_type(question: str = None) -> Entry | None:
    entry_type = input(f"""
{question if question else 'Escolha o tipo de entrada:'}
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
