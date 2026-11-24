"""Unit tests for Module A. Run with:  python -m unittest discover -s tests -v"""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from records import DynamicArray, Record, load_catalog
from hash_table import HashTable
from bst import BST
from trie import Trie, normalize


class TestDynamicArray(unittest.TestCase):
    def test_append_grow_and_pop(self):
        arr = DynamicArray()
        for i in range(100):
            arr.append(i)
        self.assertEqual(len(arr), 100)
        self.assertEqual(arr[99], 99)
        self.assertEqual(arr.pop(), 99)
        self.assertEqual(len(arr), 99)

    def test_out_of_range(self):
        with self.assertRaises(IndexError):
            DynamicArray()[0]


class TestHashTable(unittest.TestCase):
    def test_put_get_overwrite(self):
        t = HashTable()
        t.put("97000", "a")
        t.put("97000", "b")
        self.assertEqual(t.get("97000"), "b")
        self.assertEqual(len(t), 1)
        self.assertIsNone(t.get("00000"))

    def test_many_keys_force_resize(self):
        t = HashTable()
        for i in range(5000):
            t.put(str(i).zfill(5), i)
        self.assertEqual(len(t), 5000)
        self.assertEqual(t.get("04999"), 4999)

    def test_groups(self):
        t = HashTable()
        t.add_to_group("01030", 7)
        t.add_to_group("01030", 8)
        self.assertEqual(len(t.get("01030")), 2)


class TestBST(unittest.TestCase):
    def setUp(self):
        self.tree = BST()
        for rid, key in enumerate([97050, 97000, 97299, 97100, 97300, 96999, 97100]):
            self.tree.insert(key, rid)

    def test_search_with_duplicates(self):
        self.assertEqual(len(self.tree.search(97100)), 2)
        self.assertIsNone(self.tree.search(1))

    def test_range_query_is_inclusive(self):
        found = self.tree.range_query(97000, 97299)
        self.assertEqual(len(found), 5)   # 97050, 97000, 97299, 97100 x2

    def test_sorted_input_makes_a_line(self):
        line = BST()
        for k in range(200):
            line.insert(k, k)
        self.assertEqual(line.height(), 200)


class TestTrie(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize("San Ángel"), "san angel")

    def test_autocomplete_ignores_accents_and_case(self):
        t = Trie()
        for rid, name in enumerate(["San Ángel", "San Pedro", "Santa Rosa", "Itzaes"]):
            t.insert(name, rid)
        self.assertEqual(len(t.autocomplete("SAN ang")), 1)
        self.assertEqual(len(t.autocomplete("san")), 3)
        self.assertEqual(len(t.autocomplete("san", limit=2)), 2)
        self.assertEqual(len(t.autocomplete("zzz")), 0)


class TestLoader(unittest.TestCase):
    def test_load_small_file(self):
        path = os.path.join(os.path.dirname(__file__), "tiny.txt")
        with open(path, "w", encoding="latin-1", newline="") as f:
            f.write("legal notice\r\n")
            f.write("d_codigo|d_asenta|d_tipo_asenta|D_mnpio|d_estado|d_ciudad|d_CP|c_estado|c_oficina|c_CP|c_tipo_asenta|c_mnpio|id_asenta_cpcons|d_zona|c_cve_ciudad\r\n")
            f.write("97000|Mérida Centro|Colonia|Mérida|Yucatán|Mérida|97001|31|97001||09|050|0001|Urbano|01\r\n")
        try:
            recs = load_catalog(path)
            self.assertEqual(len(recs), 1)
            self.assertEqual(recs[0].neighborhood, "Mérida Centro")
            self.assertEqual(recs[0].zone, "Urbano")
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
