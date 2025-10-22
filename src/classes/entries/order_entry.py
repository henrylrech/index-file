import struct
from classes.entries.index_entry import IndexEntry

class OrderEntry:
    def __init__(self, order_id, product_id, quantity, price, user_id, active=True):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.user_id = user_id
        self.active = active

    def as_binary(self):
        # 'q' = signed 64-bit integer, 'd' = 64-bit float, '?' = boolean
        data = struct.pack('qqqdq?', 
                           self.order_id, 
                           self.product_id, 
                           self.quantity, 
                           self.price, 
                           self.user_id,
                           self.active)
        
        return data + b'\n'  # adiciona o byte de nova linha
    
    def as_index_entry(self, address):
        return IndexEntry(self.order_id, address)

    def as_str(self):
        return f"Pedido: {self.order_id}, Produto: {self.product_id}, Qtd: {self.quantity}, Preço: {self.price}, Usuário: {self.user_id}, Ativo: {self.active}"
    
    @classmethod
    def from_binary(cls, data):
        order_id, product_id, quantity, price, user_id, active = struct.unpack('qqqdq?', data)
        return cls(order_id, product_id, quantity, price, user_id, active)
    
    @staticmethod
    def get_size():
        return struct.calcsize('qqqdq?')
