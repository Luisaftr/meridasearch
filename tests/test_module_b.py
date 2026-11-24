"""Unit tests for Module B. Run with:  python -m unittest discover -s tests -v"""
import os, random, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from records import DynamicArray, Record
from heap import MinHeap
from sorting import insertion_sort, merge_sort, heap_sort, make_key, make_pairs
from ranking import top_k, count_neighborhoods_by_municipality, collect_counts


def to_list(arr):
    return [x for x in arr]


def random_pairs(n, seed=1):
    rng = random.Random(seed)
    arr = DynamicArray()
    for i in range(n):
        arr.append(((rng.randint(0, 50), rng.randint(0, 50)), i))
    return arr


class TestMinHeap(unittest.TestCase):
    def test_pops_in_order(self):
        heap = MinHeap()
        values = [5, 3, 9, 1, 7, 1, 8]
        for v in values:
            heap.push(v)
        self.assertEqual([heap.pop() for _ in range(len(values))], sorted(values))

    def test_replace_top(self):
        heap = MinHeap()
        for v in (4, 6, 8):
            heap.push(v)
        heap.replace_top(7)
        self.assertEqual(heap.pop(), 6)


class TestSorting(unittest.TestCase):
    def check(self, sort_fn, n):
        pairs = random_pairs(n)
        self.assertEqual(to_list(sort_fn(pairs)), sorted(to_list(pairs)))

    def test_all_sorts_match_python_baseline(self):
        for sort_fn in (insertion_sort, merge_sort, heap_sort):
            for n in (0, 1, 2, 50, 300):
                with self.subTest(sort=sort_fn.__name__, n=n):
                    self.check(sort_fn, n)

    def test_original_is_untouched(self):
        pairs = random_pairs(40)
        before = to_list(pairs)
        merge_sort(pairs)
        heap_sort(pairs)
        insertion_sort(pairs)
        self.assertEqual(to_list(pairs), before)

    def test_multi_key_municipality_then_neighborhood(self):
        rows = [("Zeta", "Mérida", "Yucatán"), ("Álamo", "Mérida", "Yucatán"),
                ("Beta", "Abalá", "Yucatán")]
        records = DynamicArray()
        for name, muni, state in rows:
            records.append(Record("97000", name, "Colonia", muni, state, "", "Urbano"))
        pairs = make_pairs(records, make_key("municipality", "neighborhood"))
        names = [records[i].neighborhood for _, i in merge_sort(pairs)]
        self.assertEqual(names, ["Beta", "Álamo", "Zeta"])   # Abalá first, then Mérida


class TestTopK(unittest.TestCase):
    def test_top_k_matches_baseline(self):
        rng = random.Random(7)
        pairs = DynamicArray()
        for i in range(500):
            pairs.append((rng.randint(0, 100), "town" + str(i)))
        expected = sorted(to_list(pairs), reverse=True)[:5]
        self.assertEqual(to_list(top_k(pairs, 5)), expected)

    def test_k_bigger_than_n(self):
        pairs = DynamicArray()
        pairs.append((2, "a"))
        pairs.append((9, "b"))
        self.assertEqual(to_list(top_k(pairs, 10)), [(9, "b"), (2, "a")])

    def test_count_by_municipality(self):
        records = DynamicArray()
        for name, muni in (("a", "Mérida"), ("b", "Mérida"), ("c", "Progreso")):
            records.append(Record("97000", name, "Colonia", muni, "Yucatán", "", "Urbano"))
        counts = count_neighborhoods_by_municipality(records)
        self.assertEqual(counts.get("Mérida, Yucatán"), 2)
        self.assertEqual(to_list(top_k(collect_counts(counts), 1)), [(2, "Mérida, Yucatán")])


if __name__ == "__main__":
    unittest.main()
