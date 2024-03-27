# Defines HashTable class
class HashTable:
    def __init__(self, size=20, load_factor=0.75):
        self.size = size  # Initial size
        self.count = 0  # Number of elements in the hash map
        self.load_factor = load_factor
        self.table = [[] for _ in range(self.size)]  # Creates an empty table with lists

    # Hash function to get the index
    def _hash_function(self, key):
        return hash(key) % self.size

    # Inserts items into the hash table
    def insert(self, key, item):
        if self.count / self.size >= self.load_factor:
            self.resize()

        index = self._hash_function(key)
        self.table[index].append((key, item))
        self.count += 1

    # Lookup items in the hash table
    def lookup(self, key):
        index = self._hash_function(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    # Removes items from the hash table
    def hash_remove(self, key):
        index = self._hash_function(key)
        for i, (k, _) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                self.count -= 1
                return

    # Resize the hash table if the load factor is exceeded
    def resize(self):
        self.size *= 2
        new_table = [[] for _ in range(self.size)]

        for bucket in self.table:
            for key, value in bucket:
                index = hash(key) % self.size
                new_table[index].append((key, value))

        self.table = new_table


