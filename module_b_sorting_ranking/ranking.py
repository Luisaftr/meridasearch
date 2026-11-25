"""Module B, part 3: counting and Top-K ranking with our own heap.

Top-K idea: keep a min-heap with at most K candidates. When a better one
arrives, it replaces the weakest. Cost: O(n log K) instead of O(n log n).
"""

from module_a_storage_indexes.records import DynamicArray
from module_a_storage_indexes.hash_table import HashTable
from .heap import MinHeap


def count_neighborhoods_by_municipality(records):
    """HashTable: 'Municipality, State' -> number of neighborhoods."""
    counts = HashTable()
    for r in records:
        label = r.municipality + ", " + r.state
        counts.put(label, (counts.get(label) or 0) + 1)
    return counts


def collect_counts(table):
    """Flatten the hash table into a DynamicArray of (count, label)."""
    pairs = DynamicArray()
    for head in table._buckets:          # same package, so we peek at the buckets
        node = head
        while node is not None:
            pairs.append((node.value, node.key))
            node = node.next
    return pairs


def top_k(pairs, k):
    """Return the K biggest (count, label) pairs, biggest first."""
    heap = MinHeap()
    for pair in pairs:
        if len(heap) < k:
            heap.push(pair)
        elif pair > heap.peek():
            heap.replace_top(pair)
    best = DynamicArray()
    while len(heap) > 0:
        best.append(heap.pop())          # smallest first...
    result = DynamicArray()
    for i in range(len(best) - 1, -1, -1):
        result.append(best[i])           # ...so we flip it
    return result
