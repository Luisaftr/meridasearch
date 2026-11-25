# 🌿 Module A: Storage and indexes

| Requirement | Our answer | File |
|---|---|---|
| Load the dataset into a linear structure of our own design | ✅ `DynamicArray`, a growable array that doubles when full, holds every `Record` | `records.py` |
| Hash table with our own collision strategy: exact lookup by postal code | ✅ Separate chaining (linked lists per bucket), hand-written FNV-1a hash, auto-resize at load 0.75 | `hash_table.py` |
| BST for range queries, e.g. 97000 to 97299 | ✅ Plain BST, iterative insert/search/range query (no recursion limit problems) | `bst.py` |
| Trie for autocomplete by neighborhood name | ✅ Accent and case insensitive; children kept in small linear lists (no `dict`) | `trie.py` |

## Run it
From the repo root:
```
python -m module_a_storage_indexes.demo
python -m unittest discover -t . -s . -v
```

## What we measured (full catalog, 159,527 rows)
- Loading: about 0.3 s. Distinct postal codes: 31,860.
- Hash table: longest collision chain is 5.
- BST: the file is already sorted by postal code, so inserting in file order gives a straight line (height 31,860). Inserting in a seeded random order gives height 33.
- Trie: about 690k nodes. `97000-97299` returns 496 neighborhoods.

## Complexity
| Structure | Operation | Average | Worst |
|---|---|---|---|
| DynamicArray | append | O(1) amortized | O(n) on a resize |
| Hash table | put / get | O(1) | O(n) |
| BST | insert / search | O(log n) | O(n) on sorted input |
| BST | range query | O(log n + k) | O(n) |
| Trie | insert / autocomplete | O(L) / O(L + k) | same |

(n = items, k = results returned, L = length of the word.)
