"""Quick tour of Module C. Run from the repo root:  python -m module_c_graph.demo"""
import sys, time
from module_a_storage_indexes.records import load_catalog
from module_c_graph.graph import build_municipality_graph
from module_c_graph.algorithms import bfs_within, hops_profile, dijkstra

path = sys.argv[1] if len(sys.argv) > 1 else "data_source/CPdescarga.txt"
records = load_catalog(path)
t = time.perf_counter()
g = build_municipality_graph(records)
print(f"Graph: {g.node_count():,} municipalities, {g.edge_count:,} edges, built in {time.perf_counter()-t:.2f}s")

start = g.id_of("Mérida, Yucatán")
print("\nMunicipalities within 2 hops of Mérida:")
for node, h in bfs_within(g, start, 2):
    print(f"  {h} hop(s)  {g.names[node]}")

print("\nNew municipalities per hop from Mérida:", [c for c in hops_profile(g, start, 8)])

goal = g.id_of("Tizimín, Yucatán")
total, route = dijkstra(g, start, goal)
print(f"\nCheapest route Mérida -> Tizimín (cost {total}):")
print("  " + " -> ".join(g.names[i] for i in route))
