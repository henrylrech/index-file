class HashIndex:
    def __init__(self, size=1024):
        self.size = size
        self.table = [[] for _ in range(size)]  # buckets

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, offset):
        bucket = self._hash(key)
        bucket_list = self.table[bucket]

        # substitui se já existe
        for i, (k, _) in enumerate(bucket_list):
            if k == key:
                bucket_list[i] = (key, offset)
                return
        
        # senão, adiciona
        bucket_list.append((key, offset))

    def search(self, key):
        bucket = self._hash(key)
        bucket_list = self.table[bucket]

        for k, offset in bucket_list:
            if k == key:
                return True, offset
        
        return False, None

    def remove(self, key):
        bucket = self._hash(key)
        bucket_list = self.table[bucket]

        for i, (k, _) in enumerate(bucket_list):
            if k == key:
                del bucket_list[i]
                return True
        
        return False