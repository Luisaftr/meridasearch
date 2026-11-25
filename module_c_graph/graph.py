"""Module C, part 1: municipality graph.

NODES   Every municipality (named 'Municipality, State', because names repeat
        across states).

EDGES   Postal codes are assigned by geographic zone, so the codes tell us who
        lives next to whom. The catalog has no coordinates, so this is a proxy
        for geography. We use two kinds of edge:

        1. SAME ZONE    Two municipalities that share the first 3 digits of a
                        postal code belong to the same delivery zone.
                        Weight = 1 (the closest relationship).
        2. NEXT ZONE    When a postal code is followed (in numeric order) by a
                        code of a different municipality, those two municipalities
                        are neighbors across a zone border.
                        Weight = 2 + gap // 100, where gap is the numeric distance
                        between the two codes. Far-apart codes cost more.
                        These edges also join every zone into ONE connected graph.

        (Two ideas we tried and dropped: "share a delivery office" split the
        country into 724 islands, and "only consecutive codes" produced a
        single long chain where BFS was meaningless.)

WEIGHT  Think of it as the cost of moving from one municipality to the other
        through the postal system: 1 inside a zone, 2 or more across zones.

The graph is undirected and stored as adjacency lists.
"""

from module_a_storage_indexes.records import DynamicArray
from module_a_storage_indexes.hash_table import HashTable
from module_b_sorting_ranking.sorting import merge_sort


def label_of(record):
    return record.municipality + ", " + record.state


class Graph:
    def __init__(self):
        self.names = DynamicArray()          # node id -> label
        self._ids = HashTable()              # label -> node id
        self.adjacent = DynamicArray()       # node id -> DynamicArray of (neighbor id, weight)
        self.edge_count = 0

    def node_count(self):
        return len(self.names)

    def add_node(self, label):
        known = self._ids.get(label)
        if known is not None:
            return known
        new_id = len(self.names)
        self.names.append(label)
        self._ids.put(label, new_id)
        self.adjacent.append(DynamicArray())
        return new_id

    def id_of(self, label):
        return self._ids.get(label)

    def add_edge(self, a, b, weight):
        """Undirected edge; if it already exists we keep the lighter weight."""
        if a == b:
            return
        if self._update_if_present(a, b, weight):
            self._update_if_present(b, a, weight)
            return
        self.adjacent[a].append((b, weight))
        self.adjacent[b].append((a, weight))
        self.edge_count += 1

    def _update_if_present(self, a, b, weight):
        row = self.adjacent[a]
        for i in range(len(row)):
            neighbor, old = row[i]
            if neighbor == b:
                if weight < old:
                    row[i] = (b, weight)
                return True
        return False

    def neighbors(self, node):
        return self.adjacent[node]


def build_municipality_graph(records):
    """Create the graph described above from the catalog."""
    graph = Graph()
    for r in records:
        graph.add_node(label_of(r))

    # --- 1) SAME ZONE: group municipalities by the first 3 digits of the code ---
    zones = HashTable()                      # '973' -> DynamicArray of node ids
    for r in records:
        node = graph.id_of(label_of(r))
        members = zones.get(r.postal_code[:3])
        if members is None:
            members = DynamicArray()
            zones.put(r.postal_code[:3], members)
        already_there = False
        for m in members:
            if m == node:
                already_there = True
                break
        if not already_there:
            members.append(node)
    for head in zones._buckets:
        entry = head
        while entry is not None:
            members = entry.value
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    graph.add_edge(members[i], members[j], 1)
            entry = entry.next

    # --- 2) NEXT ZONE: consecutive codes that belong to different municipalities ---
    # We sort ourselves, so it still works if a future file is not pre-sorted.
    pairs = DynamicArray()
    for i in range(len(records)):
        pairs.append((records[i].postal_code, i))
    ordered = merge_sort(pairs)
    previous_code, previous_node = None, None
    for code, i in ordered:
        node = graph.id_of(label_of(records[i]))
        if previous_node is not None and node != previous_node:
            gap = int(code) - int(previous_code)
            graph.add_edge(previous_node, node, 2 + gap // 100)
        previous_code, previous_node = code, node
    return graph
