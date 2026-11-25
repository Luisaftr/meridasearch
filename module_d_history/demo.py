"""Quick tour of Module D. Run from the repo root:  python -m module_d_history.demo"""
import sys
from module_a_storage_indexes.records import load_catalog
from module_a_storage_indexes.hash_table import HashTable
from module_a_storage_indexes.bst import BST
from module_a_storage_indexes.trie import Trie
from module_d_history.history import Query, QueryHistory

path = sys.argv[1] if len(sys.argv) > 1 else "data_source/CPdescarga.txt"
records = load_catalog(path, limit=20000)       # a small slice keeps the demo instant
table, tree, trie = HashTable(), BST(), Trie()
for i, r in enumerate(records):
    table.add_to_group(r.postal_code, i)
    tree.insert(int(r.postal_code), i)
    trie.insert(r.neighborhood, i)


def executor(query):
    """Connects a Query to the right index (a tiny preview of the full engine)."""
    if query.kind == "code":
        ids = table.get(query.argument)
    elif query.kind == "range":
        low, high = query.argument.split("-")
        ids = tree.range_query(int(low), int(high))
    else:
        ids = trie.autocomplete(query.argument, 5)
    return 0 if ids is None else len(ids)


history = QueryHistory(executor)
print("Batch of pending queries:")
for q in (Query("code", "01030"), Query("range", "01000-01999"), Query("prefix", "san")):
    history.add_pending(q)
print(f"  {history.pending_count()} waiting")
for query, result in history.run_pending():
    print(f"  ran {query!r:<26} -> {result} results")

print("\nUndo, undo, redo:")
print("  undo ->", history.undo())
print("  undo ->", history.undo())
print("  redo ->", history.redo())
print("\nA new query clears the redo stack:")
history.run(Query("code", "01000"))
print("  can redo?", history.can_redo())
