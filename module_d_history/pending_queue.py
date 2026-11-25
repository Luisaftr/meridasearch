"""Module D, part 2: a circular queue (first in, first out).

Items live in a ring of slots. `head` is the next item to leave and
`size` says how many are inside, so enqueue and dequeue never shift anything.
When the ring is full it doubles.
"""


class Queue:
    def __init__(self, capacity=8):
        self._slots = [None] * capacity
        self._head = 0
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def enqueue(self, item):
        if self._size == len(self._slots):
            self._grow()
        tail = (self._head + self._size) % len(self._slots)
        self._slots[tail] = item
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty Queue")
        item = self._slots[self._head]
        self._slots[self._head] = None
        self._head = (self._head + 1) % len(self._slots)
        self._size -= 1
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at empty Queue")
        return self._slots[self._head]

    def _grow(self):
        bigger = [None] * (len(self._slots) * 2)
        for i in range(self._size):
            bigger[i] = self._slots[(self._head + i) % len(self._slots)]
        self._slots = bigger
        self._head = 0
