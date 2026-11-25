"""Module A, part 3: plain binary search tree for range queries.

Question it answers: "Give me every code between 97000 and 97299."
Everything is iterative on purpose, so a lopsided tree can never hit
Python's recursion limit.
"""

from .records import DynamicArray


class _TreeNode:
    __slots__ = ("key", "ids", "left", "right")

    def __init__(self, key, first_id):
        self.key = key
        self.ids = DynamicArray()   # positions of every record with this code
        self.ids.append(first_id)
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self._count = 0

    def __len__(self):
        return self._count          # number of distinct keys

    def insert(self, key, record_id):
        if self.root is None:
            self.root = _TreeNode(key, record_id)
            self._count = 1
            return
        node = self.root
        while True:
            if key == node.key:
                node.ids.append(record_id)
                return
            if key < node.key:
                if node.left is None:
                    node.left = _TreeNode(key, record_id)
                    self._count += 1
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = _TreeNode(key, record_id)
                    self._count += 1
                    return
                node = node.right

    def search(self, key):
        node = self.root
        while node is not None:
            if key == node.key:
                return node.ids
            node = node.left if key < node.key else node.right
        return None

    def range_query(self, low, high):
        """In-order walk that skips whole branches outside [low, high]."""
        found = DynamicArray()
        stack = DynamicArray()
        node = self.root
        while node is not None or len(stack) > 0:
            while node is not None:
                stack.append(node)
                # No point going left if this key is already <= low.
                node = node.left if node.key > low else None
            node = stack.pop()
            if low <= node.key <= high:
                for rid in node.ids:
                    found.append(rid)
            # No point going right if this key is already >= high.
            node = node.right if node.key < high else None
        return found

    def height(self):
        if self.root is None:
            return 0
        best = 0
        todo = DynamicArray()
        todo.append((self.root, 1))
        while len(todo) > 0:
            node, depth = todo.pop()
            best = max(best, depth)
            if node.left is not None:
                todo.append((node.left, depth + 1))
            if node.right is not None:
                todo.append((node.right, depth + 1))
        return best
