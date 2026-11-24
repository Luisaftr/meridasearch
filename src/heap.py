#Module B, part 1: a binary min-heap built on our DynamicArray.


from records import DynamicArray


class MinHeap:
    def __init__(self):
        self._data = DynamicArray()

    def __len__(self):
        return len(self._data)

    def peek(self):
        return self._data[0]

    def push(self, item):
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self):
        """Remove and return the smallest item."""
        top = self._data[0]
        last = self._data.pop()
        if len(self._data) > 0:
            self._data[0] = last
            self._sift_down(0)
        return top

    def replace_top(self, item):
        """Swap the smallest item for a new one (one sift instead of two)."""
        self._data[0] = item
        self._sift_down(0)

    def _sift_up(self, i):
        data = self._data
        item = data[i]
        while i > 0:
            parent = (i - 1) // 2
            if item < data[parent]:
                data[i] = data[parent]
                i = parent
            else:
                break
        data[i] = item

    def _sift_down(self, i):
        data = self._data
        n = len(data)
        item = data[i]
        while True:
            child = 2 * i + 1
            if child >= n:
                break
            if child + 1 < n and data[child + 1] < data[child]:
                child += 1
            if data[child] < item:
                data[i] = data[child]
                i = child
            else:
                break
        data[i] = item
