import struct
from classes.entries.index_entry import IndexEntry

class ProductEntry:

    def __init__(self, product_id, jewellery_type, metal, gem, active=True):
        self.product_id = product_id
        self.jewellery_type = jewellery_type
        self.metal = metal
        self.gem = gem
        self.active = active

    def as_binary(self):
        jewellery_bytes = self.jewellery_type.encode('utf-8')[:20].ljust(20, b'\x00')
        metal_bytes = self.metal.encode('utf-8')[:20].ljust(20, b'\x00')
        gem_bytes = self.gem.encode('utf-8')[:20].ljust(20, b'\x00')

        # 'q' = signed 64-bit integer, 'd' = 64-bit float
        data = struct.pack('q20s20s20s?', 
                           self.product_id, 
                           jewellery_bytes, 
                           metal_bytes,
                           gem_bytes,
            			   self.active)
        
        return data + b'\n'  # adiciona o byte de nova linha
    
    def as_index_entry(self, address):
        return IndexEntry(self.product_id, address)
    
    def as_str(self):
        return f"Produto: {self.product_id}, Tipo: {self.jewellery_type}, Metal: {self.metal}, Jóia: {self.gem}, Ativo: {self.active}"
    
    @classmethod
    def from_binary(cls, data):
        product_id, jewellery_bytes, metal_bytes, gem_bytes, active = struct.unpack('q20s20s20s?', data)
        jewellery_type = jewellery_bytes.rstrip(b'\x00').decode('utf-8')
        metal = metal_bytes.rstrip(b'\x00').decode('utf-8')
        gem = gem_bytes.rstrip(b'\x00').decode('utf-8')
        return cls(product_id, jewellery_type, metal, gem, active)
    
    @staticmethod
    def get_size():
        return struct.calcsize('q20s20s20s?')
    