# 🍑 Module B: Sorting and ranking

| Requirement | Our answer | File |
|---|---|---|
| Three sorting algorithms from different families | ✅ Insertion sort (quadratic), merge sort (divide and conquer), heap sort (heap-based) | `sorting.py` |
| Sort by multiple keys | ✅ `make_key("municipality", "neighborhood")`, accent and case insensitive | `sorting.py` |
| Top-K query using a heap | ✅ Our own `MinHeap` of size K, e.g. municipalities with the most neighborhoods | `heap.py`, `ranking.py` |

## Run it
From the repo root:
```
python -m module_b_sorting_ranking.demo
python -m unittest discover -t . -s . -v
```

## What we measured
- Full catalog: merge sort about 1.2 s, heap sort about 1.2 s.
- Insertion sort already needs 0.19 s for 2,000 rows, so it is only tested on small sizes.
- Top 5 municipalities by neighborhoods: Hermosillo (2,124), Cajeme (1,698), Guachochi (1,496), León (1,277), Juárez (1,158).
- All sorts are checked against Python's built-in `sorted` in the tests (baseline only, never inside our structures).

## Complexity
| Algorithm | Time | Extra space | Stable |
|---|---|---|---|
| Insertion sort | O(n²) | O(1) | yes |
| Merge sort | O(n log n) | O(n) | yes |
| Heap sort | O(n log n) | O(1) | no |
| Top-K with heap | O(n log K) | O(K) | n/a |
