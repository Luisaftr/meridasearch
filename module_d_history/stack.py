"""Module D, part 1: a stack (last in, first out) built on our DynamicArray."""

from module_a_storage_indexes.records import DynamicArray


class Stack:
    def __init__(self):
        self._items = DynamicArray()

    def __len__(self):
        return len(self._items)

    def is_empty(self):
        return len(self._items) == 0

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty Stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at empty Stack")
        return self._items[len(self._items) - 1]

    def clear(self):
        self._items = DynamicArray()
