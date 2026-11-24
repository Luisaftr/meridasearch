"""Quick tour of Module B on the real catalog."""
import sys, time
from records import load_catalog
from sorting import make_key, make_pairs, insertion_sort, merge_sort, heap_sort
from ranking import count_neighborhoods_by_municipality, collect_counts, top_k

path = sys.argv[1] if len(sys.argv) > 1 else "../data_source/CPdescarga.txt"
records = load_catalog(path)
key = make_key("municipality", "neighborhood")


def clock(label, fn):
    t = time.perf_counter()
    out = fn()
    print(f"  {label:<26}{time.perf_counter() - t:8.3f}s")
    return out


print("Sorting by municipality, then neighborhood")
for n in (1000, 2000):
    pairs = make_pairs(records, key, n)
    print(f" n = {n:,}")
    clock("insertion sort (O(n^2))", lambda: insertion_sort(pairs))
    clock("merge sort", lambda: merge_sort(pairs))
    clock("heap sort", lambda: heap_sort(pairs))
for n in (10000, 50000, len(records)):
    pairs = make_pairs(records, key, n)
    print(f" n = {n:,}")
    clock("merge sort", lambda: merge_sort(pairs))
    clock("heap sort", lambda: heap_sort(pairs))

ordered = merge_sort(make_pairs(records, key, 5))
print("\nFirst rows:", [(records[i].municipality, records[i].neighborhood) for _, i in ordered])

print("\nTop 5 municipalities by number of neighborhoods")
pairs = collect_counts(count_neighborhoods_by_municipality(records))
print(f"  {len(pairs):,} municipalities counted")
for count, label in clock("heap Top-K (K=5)", lambda: top_k(pairs, 5)):
    print(f"   {count:>5}  {label}")
clock("full merge sort instead", lambda: merge_sort(pairs))
