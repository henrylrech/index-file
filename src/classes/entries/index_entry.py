import struct

class IndexEntry:
    def __init__(self, primary_id, address):
        self.primary_id = primary_id
        self.address = address

    def as_binary(self):
        data = struct.pack('qq', 
                           self.primary_id, 
                           self.address)
        
        return data + b'\n'  # adiciona o byte de nova linha
    
    def as_str(self):
        return f"ID: {self.primary_id}, Endereço: {self.address}"
    
    @classmethod
    def from_binary(cls, data):
        primary_id, address = struct.unpack('qq', data)
        return cls(primary_id, address)
    
    @staticmethod
    def get_size():
        return struct.calcsize('qq')