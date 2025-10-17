import os
from classes.entries.order_entry import OrderEntry
from classes.entries.product_entry import ProductEntry
from classes.entries.index_entry import IndexEntry
from classes.enums import Entry

def read_bin_file(file_path, entry_type):

    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado.")
        return
    entry_class = None
    match entry_type:
        case Entry.ORDERENTRY:
            entry_class = OrderEntry
        case Entry.PRODUCTENTRY:
            entry_class = ProductEntry
        case Entry.INDEXENTRY:
            entry_class = IndexEntry
        case _:
            print(f"Tipo de entrada desconhecido: {entry_type}")
            return

    with open(file_path, "rb") as f:
        while True:
            data = f.read(entry_class.get_size())
            if not data:
                break

            f.read(1)  # newline byte

            entry = entry_class.from_binary(data)
            print(entry.as_str())

def search_index(entry, key):
    dirname = os.path.dirname(__file__)
    bin_path = os.path.join(dirname, '..', 'bin')

    file_path = ''
    index_path = ''
    match entry:
        case Entry.ORDERENTRY:
            file_path = os.path.join(bin_path, 'ordered', 'orders.bin')
            index_path = os.path.join(bin_path, 'indexes', 'orders_index.bin')
        case Entry.PRODUCTENTRY:
            file_path = os.path.join(bin_path, 'ordered', 'products.bin')
            index_path = os.path.join(bin_path, 'indexes', 'products_index.bin')
        case _:
            print("Tipo de entrada inválido para busca.")
            return
        
    if not os.path.exists(file_path) or not os.path.exists(index_path):
        print("Arquivos necessários para busca não encontrados.")
        return
    
    with open(index_path, "rb") as index_file:
        left = 0
        right = 0
        data = index_file.read(IndexEntry.get_size()) # read first entry
        while data:
            right += 1
            data = index_file.read(IndexEntry.get_size()) # read next entries 
        
        index_file.seek(0) # reset pointer to start

        #print(f"Total de entradas no índice: {right}")

        #print(left, right)
        found_address = None
        last_address = None

        while left <= right:
            mid = (left + right) // 2
            #print(mid)
            index_file.seek(mid * IndexEntry.get_size() + mid)
            data = index_file.read(IndexEntry.get_size())
            if not data:
                break

            index_entry = IndexEntry.from_binary(data)

            #print(index_entry.as_str())
            if key > index_entry.primary_id:
                last_address = index_entry.address

            if index_entry.primary_id == key:
                found_address = index_entry.address
                last_address = index_entry.address
                break
            elif index_entry.primary_id < key:
                left = mid + 1
            else:
                right = mid - 1         
        
    return found_address, last_address

def get_entry(file_path, entry_type, address):
    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado.")
        return None

    entry_class = None
    match entry_type:
        case Entry.ORDERENTRY:
            entry_class = OrderEntry
        case Entry.PRODUCTENTRY:
            entry_class = ProductEntry
        case Entry.INDEXENTRY:
            entry_class = IndexEntry
        case _:
            print(f"Tipo de entrada desconhecido: {entry_type}")
            return None

    with open(file_path, "rb") as f:
        f.seek(address)  # + address for newline bytes
        data = f.read(entry_class.get_size())
        if not data:
            return None

        entry = entry_class.from_binary(data)
        return entry

def search_sequential_file(file_path, entry_type, key, last_address):
    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado.")
        return None

    entry_class = None
    match entry_type:
        case Entry.ORDERENTRY:
            entry_class = OrderEntry
        case Entry.PRODUCTENTRY:
            entry_class = ProductEntry
        case Entry.INDEXENTRY:
            entry_class = IndexEntry
        case _:
            print(f"Tipo de entrada desconhecido: {entry_type}")
            return None
        
    entry_class_size = entry_class.get_size()

    with open(file_path, "rb") as f:

        if last_address:
            f.seek(last_address)

        address = 0
        while True:
            data = f.read(entry_class_size)
            if not data:
                break

            f.read(1)  # newline byte

            entry = entry_class.from_binary(data)
            
            match entry_type:
                case Entry.ORDERENTRY:
                    if key == entry.order_id:
                        print(f"Registro encontrado no endereço {address}")
                        return entry, address
                    elif key > entry.order_id:
                        address = f.tell()  # current position
                        #print(address)
                    else:
                        print("Registro não encontrado no arquivo de dados.")
                        return None, None
                    
                case Entry.PRODUCTENTRY:
                    if key == entry.product_id:
                        print(f"Registro encontrado no endereço {address}")
                        return entry, address
                    elif key > entry.product_id:
                        address = f.tell()  # current position
                        #print(address)
                    else:
                        print("Registro não encontrado no arquivo de dados.")
                        return None, None

                case _:
                    print(f"Tipo de entrada inválido para busca sequencial: {entry_type}")
                    return None, None
                    
    return None, None

def insert(entry_type, entry):
    dirname = os.path.dirname(__file__)
    bin_path = os.path.join(dirname, '..', 'bin')

    file_path = ''
    entry_class = None
    match entry_type:
        case Entry.ORDERENTRY:
            file_path = os.path.join(bin_path, 'ordered', 'orders.bin')
            entry_class = OrderEntry
        case Entry.PRODUCTENTRY:
            file_path = os.path.join(bin_path, 'ordered', 'products.bin')
            entry_class = ProductEntry
        case _:
            print("Tipo de entrada inválido para inserção.")
            return

    tmp_path = file_path + ".tmp"

    entry_class_size = entry_class.get_size()

    last_entry = None
    inserted = False

    with open(file_path, "rb") as original_file, open(tmp_path, "wb") as temp_file:
        while True:
            data = original_file.read(entry_class_size)
            if not data:
                break

            original_file.read(1)  # newline byte

            last_entry = entry_class.from_binary(data)
            if entry_type == Entry.ORDERENTRY:
                if entry.order_id > last_entry.order_id or inserted:
                    temp_file.write(last_entry.as_binary())
                else:
                    temp_file.write(entry.as_binary())
                    inserted = True  # to avoid multiple insertions
                    temp_file.write(last_entry.as_binary())
                
            elif entry_type == Entry.PRODUCTENTRY:
                if entry.product_id > last_entry.product_id  or inserted:
                    temp_file.write(last_entry.as_binary())
                else:
                    temp_file.write(entry.as_binary())
                    inserted = True  # to avoid multiple insertions
                    temp_file.write(last_entry.as_binary())

    if inserted:
        os.replace(tmp_path, file_path)
        print("Registro inserido com sucesso.")
