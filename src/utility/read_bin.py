import os
from classes.entries.order_entry import OrderEntry
from classes.entries.product_entry import ProductEntry
from classes.entries.index_entry import IndexEntry
from classes.enums import Entry

def read_bin_file(file_path, entry_type):

    if not os.path.exists(file_path):
        print(f"Arquivo {file_path} não encontrado.")
        return

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