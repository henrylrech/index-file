import math
import pandas as pd
import os
import struct
import numpy as np
from menu import menu

def main():
    menu()

if __name__ == "__main__":
    main()
    '''
    record_size = struct.calcsize('qqqdq')
    
    with open("orders.bin", "rb") as f:
        while True:
            data = f.read(record_size)
            if not data:
                break

            f.read(1)
            
            order_id, product_id, quantity, price, user_id = struct.unpack('qqqdq', data)
            print(order_id, product_id, quantity, price, user_id)
    '''
