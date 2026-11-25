"""Module A, part 4: trie for neighborhood-name autocomplete.

Question it answers: "Which neighborhoods start with 'san'?"
Each node keeps its children in a small linear list (no dict, no set).
"""

import unicodedata
from .records import DynamicArray


def normalize(text):
    """lowercase + no accents, so 'San Angel' finds 'San Ángel'."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


class _TrieNode:
    __slots__ = ("char", "kids", "ids")

    def __init__(self, char):
        self.char = char
        self.kids = DynamicArray()   # child nodes
        self.ids = None              # record positions if a name ends here

    def child(self, char):
        for k in self.kids:
            if k.char == char:
                return k
        return None


class Trie:
    def __init__(self):
        self.root = _TrieNode("")
        self.node_count = 1

    def insert(self, name, record_id):
        node = self.root
        for ch in normalize(name):
            nxt = node.child(ch)
            if nxt is None:
                nxt = _TrieNode(ch)
                node.kids.append(nxt)
                self.node_count += 1
            node = nxt
        if node.ids is None:
            node.ids = DynamicArray()
        node.ids.append(record_id)

    def autocomplete(self, prefix, limit=10):
        """Return up to `limit` record positions whose name starts with prefix."""
        node = self.root
        for ch in normalize(prefix):
            node = node.child(ch)
            if node is None:
                return DynamicArray()
        found = DynamicArray()
        stack = DynamicArray()
        stack.append(node)
        while len(stack) > 0 and len(found) < limit:
            current = stack.pop()
            if current.ids is not None:
                for rid in current.ids:
                    if len(found) < limit:
                        found.append(rid)
            for k in current.kids:
                stack.append(k)
        return found
