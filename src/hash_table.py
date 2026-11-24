"""Module A, part 2: hash table with separate chaining.


from records import DynamicArray


class _Node:
    __slots__ = ("key", "value", "next")

    def __init__(self, key, value, nxt):
        self.key = key
        self.value = value
        self.next = nxt


def fnv1a(text):
    h = 2166136261
    for ch in text:
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return h


class HashTable:
    def __init__(self, capacity=16, max_load=0.75):
        self._capacity = capacity          # always a power of two
        self._buckets = [None] * capacity
        self._size = 0
        self._max_load = max_load

    def __len__(self):
        return self._size

    def _index(self, key):
        return fnv1a(key) & (self._capacity - 1)

    def put(self, key, value):
        """Insert or overwrite."""
        i = self._index(key)
        node = self._buckets[i]
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next
        self._buckets[i] = _Node(key, value, self._buckets[i])
        self._size += 1
        if self._size > self._max_load * self._capacity:
            self._resize()

    def get(self, key, default=None):
        node = self._buckets[self._index(key)]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        return default

    def contains(self, key):
        return self.get(key) is not None

    def add_to_group(self, key, item):
        """Store several items under one key (many neighborhoods, one code)."""
        group = self.get(key)
        if group is None:
            group = DynamicArray()
            self.put(key, group)
        group.append(item)

    def _resize(self):
        old = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        for head in old:
            node = head
            while node is not None:
                nxt = node.next
                i = self._index(node.key)
                node.next = self._buckets[i]
                self._buckets[i] = node
                node = nxt

    def longest_chain(self):
        """Handy for the report: how bad is our worst collision?"""
        worst = 0
        for head in self._buckets:
            length, node = 0, head
            while node is not None:
                length += 1
                node = node.next
            worst = max(worst, length)
        return worst
