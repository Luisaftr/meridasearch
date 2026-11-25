# 🌷 Module C: Graph

| Requirement | Our answer | File |
|---|---|---|
| Model neighborhoods or municipalities as a graph, defining and justifying the edge | ✅ Nodes are the 2,478 municipalities; edges come from postal-code zones (see below) | `graph.py` |
| BFS for "everything reachable within N hops" | ✅ `bfs_within(graph, start, max_hops)` with a hop limit, plus `hops_profile` for the chart | `algorithms.py` |
| Shortest path with weights we define | ✅ Dijkstra on our own `MinHeap` (lazy deletion) | `algorithms.py` |

## What an edge means (and why)
Correos assigns postal codes by geographic zone, so the codes tell us who sits next to whom. The catalog has no coordinates, so this is a **proxy for geography**.

| Edge type | Rule | Weight |
|---|---|---|
| Same zone | Two municipalities share the first 3 digits of a postal code | 1 |
| Next zone | A postal code is followed, in numeric order, by a code of a different municipality | 2 + gap // 100 |

The weight is the cost of moving between two municipalities through the postal system: 1 inside a zone, 2 or more across a zone border (far-apart codes cost more). The "next zone" edges also join every zone into **one connected graph**.

**Ideas we tried and dropped (good for the report):**
- "Share a delivery office (`c_oficina`)": the country split into 724 separate islands, so BFS could not travel.
- "Only consecutive codes": a single long chain, so BFS and shortest path were meaningless (Mérida to Tizimín passed through 60 municipalities).

## Run it
From the repo root:
```
python -m module_c_graph.demo
python -m module_c_graph.make_figures     # redraws the charts (needs matplotlib, drawing only)
python -m unittest discover -t . -s . -v
```

## Results (full catalog)
- Graph: 2,478 nodes and 10,437 edges, built in about 2.7 s.
- New municipalities per hop from Mérida: 1, 16, 5, 15, 9, 15, 6, 15, 5.
- Cheapest route Mérida to Tizimín: cost 12, 8 hops (Mérida, Umán, Telchac Pueblo, Tahmek, Dzidzantún, Huhí, Dzilam González, Sotuta, Tizimín).

## Charts
| `figures/bfs_reach.png` | `figures/bfs_rings.png` | `figures/shortest_path.png` |
|---|---|---|
| New municipalities reached at each hop | Mérida's network within 2 hops | Accumulated cost along the Dijkstra route |

## Complexity
(V = municipalities, E = edges)
| Algorithm | Time | Space |
|---|---|---|
| Build graph | O(N log N + E) for N catalog rows | O(V + E) |
| BFS within N hops | O(V + E) | O(V) |
| Dijkstra with a binary heap | O((V + E) log V) | O(V) |

## Limitations
- Code space is not real geography: Mérida appears next to Uxpanapa, Veracruz, simply because Veracruz's last codes (96xxx) come right before Yucatán's first (97xxx), while real neighbors such as Campeche are not linked. Real coordinates would fix this.
- Dijkstra needs non-negative weights; ours are always at least 1.
