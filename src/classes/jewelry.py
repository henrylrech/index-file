import struct

from utility import parse

class Jewelry:
    def __init__(self, date, order_id, product_id, quantity, category_id, 
                 jewellery_type, brand_id, price, user_id, gender, box_colour, metal, gem):
        self.date = parse.to_str(date)
        self.order_id = parse.to_int(order_id)
        self.product_id = parse.to_int(product_id)
        self.quantity = parse.to_int(quantity)
        self.category_id = parse.to_float(category_id)
        self.jewellery_type = parse.to_str(jewellery_type)
        self.brand_id = parse.to_int(brand_id)
        self.price = parse.to_float(price)
        self.user_id = parse.to_int(user_id)
        self.gender = parse.to_str(gender)
        self.box_colour = parse.to_str(box_colour)
        self.metal = parse.to_str(metal)
        self.gem = parse.to_str(gem)

    def as_product_entry(self):
        return ProductEntry(self.product_id, self.category_id, self.metal, self.gem)
    
    def as_order_entry(self):
        return OrderEntry(self.order_id, self.product_id, self.quantity, self.price, self.user_id)

class ProductEntry:

    def __init__(self, product_id, category_id, metal, gem):
        self.product_id = product_id
        self.category_id = category_id
        self.metal = metal
        self.gem = gem

    def as_binary(self):
        metal_bytes = self.metal.encode('utf-8')[:20].ljust(20, b'\x00')
        gem_bytes = self.gem.encode('utf-8')[:20].ljust(20, b'\x00')

        # 'q' = signed 64-bit integer, 'd' = 64-bit float
        data = struct.pack('qd20s20s', 
                           self.product_id, 
                           self.category_id, 
                           metal_bytes,
                           gem_bytes)
        
        return data + b'\n'  # adiciona o byte de nova linha
    
    def as_string(self):
        return f"Produto: {self.product_id}, Categoria: {self.category_id}, Metal: {self.metal}, Jóia: {self.gem}"
    
    @classmethod
    def from_binary(cls, data):
        product_id, category_id, metal_bytes, gem_bytes = struct.unpack('qd20s20s', data)
        metal = metal_bytes.rstrip(b'\x00').decode('utf-8')
        gem = gem_bytes.rstrip(b'\x00').decode('utf-8')
        return cls(product_id, category_id, metal, gem)
    
    @staticmethod
    def get_size():
        return struct.calcsize('qd20s20s')
    
class OrderEntry:
    def __init__(self, order_id, product_id, quantity, price, user_id):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.user_id = user_id

    def as_binary(self):
        # 'q' = signed 64-bit integer, 'd' = 64-bit float
        data = struct.pack('qqqdq', 
                           self.order_id, 
                           self.product_id, 
                           self.quantity, 
                           self.price, 
                           self.user_id)
        
        return data + b'\n'  # adiciona o byte de nova linha
    
    def as_string(self):
        return f"Pedido: {self.order_id}, Produto: {self.product_id}, Qtd: {self.quantity}, Preço: {self.price}, Usuário: {self.user_id}"
    
    @classmethod
    def from_binary(cls, data):
        order_id, product_id, quantity, price, user_id = struct.unpack('qqqdq', data)
        return cls(order_id, product_id, quantity, price, user_id)
    
    @staticmethod
    def get_size():
        return struct.calcsize('qqqdq')
