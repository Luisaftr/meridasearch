"""Quick tour of Module A on the real catalog."""
import random, sys, time
from records import load_catalog
from hash_table import HashTable
from bst import BST
from trie import Trie

path = sys.argv[1] if len(sys.argv) > 1 else "../data/CPdescarga.txt"
t = time.perf_counter()
records = load_catalog(path)
print(f"Loaded {len(records):,} records in {time.perf_counter()-t:.2f}s")

table, tree, trie = HashTable(), BST(), Trie()
t = time.perf_counter()
for i, r in enumerate(records):
    table.add_to_group(r.postal_code, i)
print(f"hash: {len(table):,} codes, longest chain {table.longest_chain()}, {time.perf_counter()-t:.2f}s")

# The catalog arrives sorted by postal code. Feeding a plain BST sorted keys
# makes it a straight line, so we insert in a seeded random order instead.
order = list(range(len(records)))
random.Random(42).shuffle(order)
t = time.perf_counter()
for i in order:
    tree.insert(int(records[i].postal_code), i)
print(f"BST (shuffled order): {len(tree):,} keys, height {tree.height():,}, {time.perf_counter()-t:.2f}s")

# Worst case for the report: the same idea with sorted keys, only 3,000 of them.
worst = BST()
t = time.perf_counter()
for i in range(3000):
    worst.insert(int(records[i].postal_code), i)
print(f"BST (sorted order, 3,000 rows): height {worst.height():,}, {time.perf_counter()-t:.2f}s")

t = time.perf_counter()
for i, r in enumerate(records):
    trie.insert(r.neighborhood, i)
print(f"trie: {trie.node_count:,} nodes, {time.perf_counter()-t:.2f}s")

print("\nCode 97000:", [records[i].neighborhood for i in table.get("97000")][:5])
rng = tree.range_query(97000, 97299)
print("Range 97000-97299:", len(rng), "neighborhoods")
print("'san ang':", [records[i].neighborhood for i in trie.autocomplete("san ang", 5)])
