"""Module C, part 2: BFS (within N hops) and Dijkstra (weighted shortest path)."""

from module_a_storage_indexes.records import DynamicArray
from module_b_sorting_ranking.heap import MinHeap

INFINITY = float("inf")


def bfs_within(graph, start, max_hops):
    """Everything reachable from `start` in at most `max_hops` steps.

    Returns a DynamicArray of (node id, hops), nearest first.
    The queue is a DynamicArray plus a moving head index.
    """
    n = graph.node_count()
    hops = DynamicArray()
    for _ in range(n):
        hops.append(-1)                      # -1 = not visited yet
    hops[start] = 0
    queue = DynamicArray()
    queue.append(start)
    head = 0
    reached = DynamicArray()
    while head < len(queue):
        node = queue[head]
        head += 1
        reached.append((node, hops[node]))
        if hops[node] == max_hops:
            continue                         # do not expand past the limit
        for neighbor, _weight in graph.neighbors(node):
            if hops[neighbor] == -1:
                hops[neighbor] = hops[node] + 1
                queue.append(neighbor)
    return reached


def hops_profile(graph, start, max_hops):
    """How many NEW nodes appear at each hop: [(hop, count), ...]."""
    counts = DynamicArray()
    for _ in range(max_hops + 1):
        counts.append(0)
    for _node, h in bfs_within(graph, start, max_hops):
        counts[h] += 1
    return counts


def dijkstra(graph, start, goal):
    """Cheapest path by edge weight. Returns (total weight, DynamicArray of node ids).

    Uses our own MinHeap with "lazy deletion": outdated entries are skipped.
    Returns (None, None) when there is no route.
    """
    n = graph.node_count()
    best = DynamicArray()
    came_from = DynamicArray()
    for _ in range(n):
        best.append(INFINITY)
        came_from.append(-1)
    best[start] = 0
    heap = MinHeap()
    heap.push((0, start))
    while len(heap) > 0:
        dist, node = heap.pop()
        if dist > best[node]:
            continue                         # a cheaper route was already found
        if node == goal:
            break
        for neighbor, weight in graph.neighbors(node):
            candidate = dist + weight
            if candidate < best[neighbor]:
                best[neighbor] = candidate
                came_from[neighbor] = node
                heap.push((candidate, neighbor))
    if best[goal] == INFINITY:
        return None, None
    backwards = DynamicArray()
    node = goal
    while node != -1:
        backwards.append(node)
        node = came_from[node]
    path = DynamicArray()
    while len(backwards) > 0:
        path.append(backwards.pop())
    return best[goal], path
