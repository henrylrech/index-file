import struct

from utility import parse

class Jewelry:
    def __init__(self, date, order_id, product_id, quantity, category_id, 
                 jewellery_type, brand_id, price, user_id, gender, box_colour, metal, gem):
        self.date = date
        self.order_id = parse.to_int(order_id)
        self.product_id = parse.to_int(product_id)
        self.quantity = parse.to_int(quantity)
        self.category_id = parse.to_float(category_id)
        self.jewellery_type = jewellery_type
        self.brand_id = parse.to_int(brand_id)
        self.price = parse.to_float(price)
        self.user_id = parse.to_int(user_id)
        self.gender = gender
        self.box_colour = box_colour
        self.metal = metal
        self.gem = gem

    def as_product_entry(self):
        return ProductEntry(self.product_id, self.brand_id, self.category_id, self.jewellery_type)
    
    def as_order_entry(self):
        return OrderEntry(self.order_id, self.product_id, self.quantity, self.price, self.user_id)

class ProductEntry:
    def __init__(self, product_id, brand_id, category_id, jewellery_type):
        self.product_id = product_id
        self.brand_id = parse.to_float(brand_id)
        self.category_id = category_id
        self.jewellery_type = parse.to_float(jewellery_type)

    def as_binary(self):
        # 'q' = signed 64-bit integer, 'd' = 64-bit float
        data = struct.pack('qdqd', 
                           int(self.product_id), 
                           float(self.brand_id), 
                           int(self.category_id),
                           float(self.jewellery_type))
        
        return data + b'\n'  # adiciona o byte de nova linha
    
    def from_binary(data):
        product_id, brand_id, category_id, jewellery_type = struct.unpack('qdqd', data)
        return ProductEntry(product_id, brand_id, category_id, jewellery_type)
    
    def get_size():
        return struct.calcsize('qdqd')
    
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
                           int(self.order_id), 
                           int(self.product_id), 
                           int(self.quantity), 
                           float(self.price), 
                           int(self.user_id))
        
        return data + b'\n'  # adiciona o byte de nova linha
    
    def from_binary(data):
        order_id, product_id, quantity, price, user_id = struct.unpack('qqqdq', data)
        return OrderEntry(order_id, product_id, quantity, price, user_id)
    
    def get_size():
        return struct.calcsize('qqqdq')
