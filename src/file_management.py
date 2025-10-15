import os
import time
import pandas as pd
from classes.jewelry import Jewelry, OrderEntry, ProductEntry
from utility.timer import Timer

def write_unordered_files(chunk_size=50):

    timer = Timer()

    dirname = os.path.dirname(__file__)

    csv_path = os.path.join(dirname, '..', 'dataset', 'jewelry.csv')
    orders_path = os.path.join(dirname, '..', 'bin', 'unordered', 'orders.bin')
    products_path = os.path.join(dirname, '..', 'bin', 'unordered', 'products.bin')
    
    #try:

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
        
    #except Exception as e:
     #   print(f"Erro: {e}")
    #    return False

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

    if os.path.exists(orders_path): 
        os.remove(orders_path) 
        print("Arquivo orders.bin removido.")
    if os.path.exists(products_path): 
        os.remove(products_path)
        print("Arquivo products.bin removido.")

    with open(unordered_orders_path, "rb") as f:
        while True:
            data = f.read(OrderEntry.get_size())
            if not data:
                break

            f.read(1) # newline byte

            order_entry = OrderEntry.from_binary(data)
            print(vars(order_entry))

    with open(unordered_products_path, "rb") as f:
        while True:
            data = f.read(ProductEntry.get_size())
            if not data:
                break

            f.read(1) # newline byte

            product_entry = ProductEntry.from_binary(data)
            print(vars(product_entry))

    print(f"Arquivos ordenados com sucesso. Duração: {timer.seconds()} segundos.")

