# 🌸 MéridaSearch

A small, sweet search engine for Mexico's postal code catalog (about 160,000 rows from Correos de México).
Built by Group 11 to show that the right data structure beats brute force. 🍓

## 🌿 What is inside (so far)

| Module | What it does | File |
|---|---|---|
| A · Storage | Our own growable array holds every record | `src/records.py` |
| A · Hash table | Exact lookup by postal code (separate chaining, hand-written FNV-1a hash) | `src/hash_table.py` |
| A · BST | Range queries such as 97000 to 97299 | `src/bst.py` |
| A · Trie | Autocomplete by neighborhood name (accent and case insensitive) | `src/trie.py` |

| B · Heap | Our own min-heap | `src/heap.py` |
| B · Sorting | Insertion sort (quadratic), merge sort (divide and conquer), heap sort (heap-based), plus multi-key sorting | `src/sorting.py` |
| B · Ranking | Top-K with a size-K heap, e.g. the municipalities with the most neighborhoods | `src/ranking.py` |

Coming next: graph (C), undo/redo and queue (D), benchmark, and the LRU cache booster. ✨

## 🍑 How to run

1. Download the catalog from Correos de México and put `CPdescarga.txt` inside the `data/` folder (it is git-ignored on purpose: the catalog's license does not allow redistribution).
2. Take the tours: `cd src && python demo_module_a.py` and `python demo_module_b.py`
3. Run the tests: `python -m unittest discover -s tests -v`

Only the Python standard library is used, and never inside our own structures.

## 🌷 Fun facts we found

- The file is already sorted by postal code, so a plain BST fed in file order becomes a straight line (height 31,860). We insert in a seeded random order instead, which gives a height of 33.
- 159,527 rows, 31,860 distinct postal codes, 32 states and 2,478 municipalities.
- Longest collision chain in our hash table: 5.
