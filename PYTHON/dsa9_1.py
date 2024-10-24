class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def delete(self, key):
        index = self._hash(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                return

    def display(self):
        for index, pairs in enumerate(self.table):
            if pairs:
                print(f"table[{index}] --> ", end='')
                for pair in pairs:
                    print(f"({pair[0]}, {pair[1]})", end=' ')
                print()

hash_table = HashTable(7)
hash_table.insert(231, 123)
hash_table.insert(326, 432)
hash_table.insert(212, 523)
hash_table.insert(321, 43)
hash_table.insert(433, 423)
hash_table.insert(262, 111)
hash_table.display()
hash_table.delete(212)
hash_table.display()