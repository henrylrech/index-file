import os
import pandas as pd
from classes.enums import Entry
from classes.jewelry import Jewelry
from classes.entries.order_entry import OrderEntry
from classes.entries.product_entry import ProductEntry
from classes.entries.index_entry import IndexEntry
from file_management import get_entry, insert, search_index, search_sequential_file
from utility.read_bin import read_bin_file
from utility.timer import Timer
from utility.sort import quicksort

#1
def write_unordered_files(chunk_size=50):

    timer = Timer()

    dirname = os.path.dirname(__file__)

    csv_path = os.path.join(dirname, '..', 'dataset', 'jewelry.csv')
    orders_path = os.path.join(dirname, '..', 'bin', 'unordered', 'orders.bin')
    products_path = os.path.join(dirname, '..', 'bin', 'unordered', 'products.bin')
    
    try:

        os.makedirs(os.path.dirname(orders_path), exist_ok=True)
        os.makedirs(os.path.dirname(products_path), exist_ok=True)

        if os.path.exists(orders_path): 
            os.remove(orders_path) 
            print("Arquivo orders.bin removido.")
        if os.path.exists(products_path): 
            os.remove(products_path)
            print("Arquivo products.bin removido.")

        print("Criando arquivos...")

        with open(orders_path, "ab") as orders_file, open(products_path, "ab") as products_file:
            for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
                for ix, row in chunk.iterrows():
                    date = row.iloc[0]
                    order_id = row.iloc[1]
                    product_id = row.iloc[2]
                    quantity = row.iloc[3]
                    category_id = row.iloc[4]
                    jewellery_type = row.iloc[5]
                    brand_id = row.iloc[6]
                    price = row.iloc[7]
                    user_id = row.iloc[8]
                    gender = row.iloc[9]
                    box_colour = row.iloc[10]
                    metal = row.iloc[11]
                    gem = row.iloc[12]
                    
                    jewelry = Jewelry(date, order_id, product_id, quantity, category_id, 
                                    jewellery_type, brand_id, price, user_id, gender, 
                                    box_colour, metal, gem)
                    
                    #print(vars(jewelry))

                    orders_file.write(jewelry.as_order_entry().as_binary())
                    products_file.write(jewelry.as_product_entry().as_binary())

        print(f"Arquivos criados com sucesso. Duração: {timer.seconds()} segundos.")
        return True
        
    except Exception as e:
        print(f"Erro: {e}")
        return False

#2
def order_files():
    timer = Timer()

    dirname = os.path.dirname(__file__)
    bin_path = os.path.join(dirname, '..', 'bin')
    unordered_orders_path = os.path.join(bin_path, 'unordered', 'orders.bin')
    unordered_products_path = os.path.join(bin_path, 'unordered', 'products.bin')

    if not os.path.exists(unordered_orders_path) or not os.path.exists(unordered_products_path):
        print("Arquivos não ordenados não encontrados. Por favor, crie-os primeiro.")
        return False
    
    orders_path = os.path.join(bin_path, 'ordered', 'orders.bin')
    products_path = os.path.join(bin_path, 'ordered', 'products.bin')

    os.makedirs(os.path.dirname(orders_path), exist_ok=True)
    os.makedirs(os.path.dirname(products_path), exist_ok=True)

    if os.path.exists(orders_path): 
        os.remove(orders_path) 
        print("Arquivo orders.bin removido.")
    if os.path.exists(products_path): 
        os.remove(products_path)
        print("Arquivo products.bin removido.")

    order_entries = []
    with open(unordered_orders_path, "rb") as f:
        while True:
            data = f.read(OrderEntry.get_size())
            if not data:
                break

            f.read(1) # newline byte

            order_entry = OrderEntry.from_binary(data)
            order_entries.append(order_entry)
            # print(vars(order_entry))

    print(f"Ordenando {len(order_entries)} entradas de pedidos... (Quicksort)")
    order_entries = quicksort(order_entries, "order_id")
    print("Entradas de pedidos ordenadas.")

    print("Escrvendo arquivo de pedidos ordenados...")
    with open(orders_path, "ab") as orders_file:
        for oe in order_entries:
            orders_file.write(oe.as_binary())
    print("Arquivo ordenado escrito.")

    product_entries = []
    with open(unordered_products_path, "rb") as f:
        while True:
            data = f.read(ProductEntry.get_size())
            if not data:
                break

            f.read(1) # newline byte

            product_entry = ProductEntry.from_binary(data)
            product_entries.append(product_entry)
            #print(vars(product_entry))

    print(f"Ordenando {len(product_entries)} entradas de produtos... (Quicksort)")
    print(product_entries[0].product_id, product_entries[-1].product_id)
    product_entries = quicksort(product_entries, "product_id")
    print(product_entries[0].product_id, product_entries[-1].product_id)
    print("Entradas de produtos ordenadas.")

    print("Escrvendo arquivo de produtos ordenados...")
    with open(products_path, "ab") as products_file:
        for pe in product_entries:
            products_file.write(pe.as_binary())
    print("Arquivo ordenado escrito.")

    print(f"Criação de arquivos ordenados finalizada com sucesso. Duração: {timer.seconds()} segundos.")

#3
def build_indexes(every_n=500):
    timer = Timer()

    dirname = os.path.dirname(__file__)
    bin_path = os.path.join(dirname, '..', 'bin')
    orders_path = os.path.join(bin_path, 'ordered', 'orders.bin')
    products_path = os.path.join(bin_path, 'ordered', 'products.bin')

    orders_index_path = os.path.join(bin_path, 'indexes', 'orders_index.bin')
    products_index_path = os.path.join(bin_path, 'indexes', 'products_index.bin')
    os.makedirs(os.path.dirname(orders_index_path), exist_ok=True)
    os.makedirs(os.path.dirname(products_index_path), exist_ok=True)

    if not os.path.exists(orders_path) or not os.path.exists(products_path):
        print("Arquivos ordenados não encontrados. Por favor, crie-os primeiro.")
        return False

    orders_count = 0
    orders_address = 0
    with open(orders_path, "rb") as f:
        with open(orders_index_path, "wb") as index_file:
            while True:
                data = f.read(OrderEntry.get_size())
                if not data:
                    break

                f.read(1) # newline byte

                record_size = OrderEntry.get_size() + 1
                orders_address += record_size

                orders_count += 1
                if orders_count == 1 or orders_count % every_n != 0:
                    continue

                order_entry = OrderEntry.from_binary(data)
                index_entry = order_entry.as_index_entry(orders_address - record_size).as_binary()
                index_file.write(index_entry)

    products_count = 0
    products_address = 0
    product_entry_size = ProductEntry.get_size()
    with open(products_path, "rb") as f:
        with open(products_index_path, "wb") as index_file:
            while True:
                data = f.read(product_entry_size)
                if not data:
                    break

                f.read(1) # newline byte

                record_size = product_entry_size + 1
                products_address += record_size

                products_count += 1
                if products_count % every_n != 0:
                    continue

                product_entry = ProductEntry.from_binary(data)
                index_entry = product_entry.as_index_entry(products_address - record_size).as_binary()
                index_file.write(index_entry)

    print(f"Criação de índices finalizada com sucesso. Duração: {timer.seconds()} segundos.")
        
#4 
def read_entire_file(file_id):
    dirname = os.path.dirname(__file__)
    bin_path = os.path.join(dirname, '..', 'bin')

    path = ''
    entry = None
    match file_id:
        case '1':
            path = os.path.join(bin_path, 'unordered', 'orders.bin')
            entry = Entry.ORDERENTRY
        case '2':
            path = os.path.join(bin_path, 'unordered', 'products.bin')
            entry = Entry.PRODUCTENTRY
        case '3':
            path = os.path.join(bin_path, 'ordered', 'orders.bin')
            entry = Entry.ORDERENTRY
        case '4':
            path = os.path.join(bin_path, 'ordered', 'products.bin')
            entry = Entry.PRODUCTENTRY
        case '5':
            path = os.path.join(bin_path, 'indexes', 'orders_index.bin')
            entry = Entry.INDEXENTRY
        case '6':
            path = os.path.join(bin_path, 'indexes', 'products_index.bin')
            entry = Entry.INDEXENTRY
        case _:
            print("ID de arquivo inválido.")
            return

    read_bin_file(path, entry)
    
#5
def search(entry, key):

    dirname = os.path.dirname(__file__)
    bin_path = os.path.join(dirname, '..', 'bin')

    file_path = ''
    match entry:
        case Entry.ORDERENTRY:
            file_path = os.path.join(bin_path, 'ordered', 'orders.bin')
        case Entry.PRODUCTENTRY:
            file_path = os.path.join(bin_path, 'ordered', 'products.bin')
        case _:
            print("Tipo de entrada inválido para busca.")
            return None, None

    found_address, last_address = search_index(entry, key)
    if found_address:
        print(f"Index hit. Registro encontrado no endereço {found_address}")
            
        entry = get_entry(file_path, entry, found_address)
        if entry:
            print(entry.as_str())
            return entry, found_address

    else:
        print("Registro não encontrado no índice.")
        print(f"Último endereço verificado no índice: {last_address}. Fazendo pesquisa sequencial no arquivo de dados...")

        entry, address = search_sequential_file(file_path, entry, key, last_address)
        if entry:
            print(entry.as_str())
            return entry, address
        
    return None, None

def remove_logical(entry_type, key):

    dirname = os.path.dirname(__file__)
    bin_path = os.path.join(dirname, '..', 'bin')

    file_path = ''
    match entry_type:
        case Entry.ORDERENTRY:
            file_path = os.path.join(bin_path, 'ordered', 'orders.bin')
        case Entry.PRODUCTENTRY:
            file_path = os.path.join(bin_path, 'ordered', 'products.bin')
        case _:
            print("Tipo de entrada inválido para remoção.")
            return

    entry, address = search(entry_type, key)
    if entry is None:
        print("Registro não encontrado. Não é possível remover.")
        return False
    if not entry.active:
        print("Registro já está marcado como inativo.")
        return False
    
    entry.active = False
    
    with open(file_path, "r+b") as f:  # modo leitura+escrita binária
        f.seek(address)
        f.write(entry.as_binary())
        f.write(b'\n')  # mantém consistência se você usa newline entre registros
    
    
    print(f"Registro com chave {key}, endereço {address} marcado como inativo com sucesso.")

def insert_order():

    order_id = 0
    product_id = 0
    quantity = 0
    price = 0
    user_id = 0

    try:
        order_id = int(input("Digite o ID do pedido: "))
        product_id = int(input("Digite o ID do produto: "))
        quantity = int(input("Digite a quantidade: "))
        price = float(input("Digite o preço: "))
        user_id = int(input("Digite o ID do usuário: "))
    except ValueError:
        print("Entrada inválida. IDs devem ser inteiros e preço deve ser um número.")
        return False
    
    entry = OrderEntry(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price=price,
        user_id=user_id,
        active=True
    )

    insert(Entry.ORDERENTRY, entry)
    
def insert_product():
    
    product_id = 0
    jewellery_type = ''
    metal = ''
    gem = ''

    try:
        product_id = int(input("Digite o ID do produto: "))
        jewellery_type = input("Digite o tipo de joia: ")
        metal = input("Digite o metal: ")
        gem = input("Digite a jóia: ")
    except ValueError:
        print("Entrada inválida. IDs devem ser inteiros.")
        return False
    
    entry = ProductEntry(
        product_id=product_id,
        jewellery_type=jewellery_type,
        metal=metal,
        gem=gem
    )

    insert(Entry.PRODUCTENTRY, entry)


        
