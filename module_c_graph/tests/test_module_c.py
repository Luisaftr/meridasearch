"""Unit tests for Module C. Run from the repo root:  python -m unittest discover -t . -s . -v"""
import unittest

from module_a_storage_indexes.records import DynamicArray, Record
from module_c_graph.graph import Graph, build_municipality_graph
from module_c_graph.algorithms import bfs_within, hops_profile, dijkstra


def make_records(rows):
    records = DynamicArray()
    for code, muni in rows:
        records.append(Record(code, "colonia", "Colonia", muni, "Yucatán", "", "Urbano"))
    return records


def weight_between(graph, a, b):
    for neighbor, weight in graph.neighbors(a):
        if neighbor == b:
            return weight
    return None


class TestBuild(unittest.TestCase):
    def setUp(self):
        # 970xx: A and B share a zone. 971xx: C. 975xx: D (far away).
        self.graph = build_municipality_graph(make_records([
            ("97010", "A"), ("97020", "B"), ("97110", "C"), ("97510", "D"),
        ]))
        self.ids = {n: self.graph.id_of(n + ", Yucatán") for n in "ABCD"}

    def test_same_zone_edge_costs_one(self):
        self.assertEqual(weight_between(self.graph, self.ids["A"], self.ids["B"]), 1)

    def test_next_zone_edge_costs_two_plus_gap(self):
        # B (97020) -> C (97110): gap 90 -> 2 + 0 = 2.   C (97110) -> D (97510): gap 400 -> 2 + 4 = 6
        self.assertEqual(weight_between(self.graph, self.ids["B"], self.ids["C"]), 2)
        self.assertEqual(weight_between(self.graph, self.ids["C"], self.ids["D"]), 6)

    def test_graph_is_undirected_and_connected(self):
        self.assertEqual(weight_between(self.graph, self.ids["D"], self.ids["C"]), 6)
        self.assertEqual(len(bfs_within(self.graph, self.ids["A"], 10)), 4)

    def test_works_with_unsorted_input(self):
        scrambled = build_municipality_graph(make_records([
            ("97510", "D"), ("97010", "A"), ("97110", "C"), ("97020", "B"),
        ]))
        a, d = scrambled.id_of("A, Yucatán"), scrambled.id_of("D, Yucatán")
        self.assertEqual(dijkstra(scrambled, a, d)[0], 9)    # A-B 1, B-C 2, C-D 6


class TestBFS(unittest.TestCase):
    def setUp(self):
        # A line: 0 - 1 - 2 - 3 - 4
        self.line = Graph()
        for name in "01234":
            self.line.add_node(name)
        for i in range(4):
            self.line.add_edge(i, i + 1, 1)

    def test_respects_hop_limit(self):
        reached = [(n, h) for n, h in bfs_within(self.line, 0, 2)]
        self.assertEqual(reached, [(0, 0), (1, 1), (2, 2)])

    def test_zero_hops_is_just_the_start(self):
        self.assertEqual(len(bfs_within(self.line, 2, 0)), 1)

    def test_profile_counts_new_nodes_per_hop(self):
        self.assertEqual([c for c in hops_profile(self.line, 2, 3)], [1, 2, 2, 0])


class TestDijkstra(unittest.TestCase):
    def test_prefers_cheaper_longer_route(self):
        g = Graph()
        for name in "SABT":
            g.add_node(name)
        s, a, b, t = 0, 1, 2, 3
        g.add_edge(s, t, 10)          # direct but expensive
        g.add_edge(s, a, 2)
        g.add_edge(a, b, 2)
        g.add_edge(b, t, 2)           # 3 hops, total 6
        total, path = dijkstra(g, s, t)
        self.assertEqual(total, 6)
        self.assertEqual([n for n in path], [s, a, b, t])

    def test_no_route_returns_none(self):
        g = Graph()
        g.add_node("X")
        g.add_node("Y")
        self.assertEqual(dijkstra(g, 0, 1), (None, None))

    def test_start_equals_goal(self):
        g = Graph()
        g.add_node("X")
        total, path = dijkstra(g, 0, 0)
        self.assertEqual((total, len(path)), (0, 1))

    def test_duplicate_edge_keeps_lighter_weight(self):
        g = Graph()
        g.add_node("X")
        g.add_node("Y")
        g.add_edge(0, 1, 9)
        g.add_edge(0, 1, 4)
        self.assertEqual(g.edge_count, 1)
        self.assertEqual(weight_between(g, 1, 0), 4)


if __name__ == "__main__":
    unittest.main()
