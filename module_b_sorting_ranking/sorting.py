"""Module B, part 2: three sorting algorithms from three families.

  * insertion_sort : quadratic            O(n^2)
  * merge_sort     : divide-and-conquer   O(n log n), stable
  * heap_sort      : heap-based           O(n log n), in place

Every sort works on a DynamicArray of (key, record_id) pairs and returns a
NEW sorted array, so the original stays untouched. Because the record_id is
part of the pair, ties are broken the same way by every algorithm.
"""

import unicodedata
from module_a_storage_indexes.records import DynamicArray


def normalize(text):
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def make_key(*fields):
    """Build a multi-key function, e.g. make_key('municipality', 'neighborhood')."""
    def key(record):
        return tuple(normalize(getattr(record, f)) for f in fields)
    return key


def make_pairs(records, key_func, count=None):
    """Turn records into (key, position) pairs, ready to be sorted."""
    pairs = DynamicArray()
    total = len(records) if count is None else min(count, len(records))
    for i in range(total):
        pairs.append((key_func(records[i]), i))
    return pairs


def _copy(items):
    clone = DynamicArray()
    for item in items:
        clone.append(item)
    return clone


# ---------- quadratic: insertion sort ----------
def insertion_sort(items):
    arr = _copy(items)
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and current < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr


# ---------- divide and conquer: merge sort ----------
def merge_sort(items):
    arr = _copy(items)
    buffer = _copy(items)
    _merge_sort(arr, buffer, 0, len(arr))
    return arr


def _merge_sort(arr, buffer, lo, hi):
    if hi - lo < 2:
        return
    mid = (lo + hi) // 2
    _merge_sort(arr, buffer, lo, mid)
    _merge_sort(arr, buffer, mid, hi)
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if arr[j] < arr[i]:
            buffer[k] = arr[j]
            j += 1
        else:
            buffer[k] = arr[i]
            i += 1
        k += 1
    while i < mid:
        buffer[k] = arr[i]
        i += 1
        k += 1
    while j < hi:
        buffer[k] = arr[j]
        j += 1
        k += 1
    for t in range(lo, hi):
        arr[t] = buffer[t]


# ---------- heap based: heap sort ----------
def heap_sort(items):
    arr = _copy(items)
    n = len(arr)
    # 1) turn the array into a max-heap
    for start in range(n // 2 - 1, -1, -1):
        _sift_down_max(arr, start, n)
    # 2) move the biggest item to the end, shrink the heap, repeat
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down_max(arr, 0, end)
    return arr


def _sift_down_max(arr, i, n):
    item = arr[i]
    while True:
        child = 2 * i + 1
        if child >= n:
            break
        if child + 1 < n and arr[child] < arr[child + 1]:
            child += 1
        if item < arr[child]:
            arr[i] = arr[child]
            i = child
        else:
            break
    arr[i] = item
