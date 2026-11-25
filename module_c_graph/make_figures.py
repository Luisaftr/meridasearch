"""Draws the Module C charts. Run from the repo root:  python -m module_c_graph.make_figures

matplotlib is used ONLY to draw pictures. The graph, BFS and Dijkstra are all our own code.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from module_a_storage_indexes.records import load_catalog
from module_c_graph.graph import build_municipality_graph
from module_c_graph.algorithms import bfs_within, hops_profile, dijkstra

TERRACOTTA, MINT, PEACH, CREAM, BROWN = "#D9826B", "#A8D8C0", "#F6C9B6", "#FFF8F2", "#5A3E36"
OUT = "module_c_graph/figures/"

records = load_catalog("data_source/CPdescarga.txt")
graph = build_municipality_graph(records)
start = graph.id_of("Mérida, Yucatán")
goal = graph.id_of("Tizimín, Yucatán")


def short(label):
    return label.split(",")[0]


def in_yucatan(node):
    return graph.names[node].endswith("Yucatán")


def style(ax):
    ax.set_facecolor(CREAM)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(BROWN)
    ax.tick_params(colors=BROWN)


# ---------- 1) BFS reach: new municipalities per hop ----------
profile = [c for c in hops_profile(graph, start, 8)]
fig, ax = plt.subplots(figsize=(8, 4.6), facecolor=CREAM)
style(ax)
bars = ax.bar(range(len(profile)), profile, color=[TERRACOTTA] + [MINT] * (len(profile) - 1), edgecolor=BROWN, linewidth=0.8)
for rect, value in zip(bars, profile):
    ax.text(rect.get_x() + rect.get_width() / 2, value + 0.3, str(value), ha="center", color=BROWN, fontsize=11)
ax.set_xlabel("Hops from Mérida", color=BROWN)
ax.set_ylabel("New municipalities reached", color=BROWN)
ax.set_title("How far can you go from Mérida? (BFS)", color=BROWN, fontsize=14, pad=12)
fig.tight_layout()
fig.savefig(OUT + "bfs_reach.png", dpi=160, facecolor=CREAM)
plt.close(fig)

# ---------- 2) BFS rings: Mérida in the middle, one ring per hop ----------
reached = [(n, h) for n, h in bfs_within(graph, start, 2)]
layers = {0: [], 1: [], 2: []}
for node, h in reached:
    layers[h].append(node)
RADIUS = {1: 3.0, 2: 5.2}
pos, angle_of = {start: (0.0, 0.0)}, {start: 0.0}
for h in (1, 2):
    members = layers[h]
    for k, node in enumerate(members):
        angle = 2 * math.pi * k / len(members) + (0.2 if h == 2 else math.pi / 2)
        angle_of[node] = angle
        pos[node] = (RADIUS[h] * math.cos(angle), RADIUS[h] * math.sin(angle))
hop_of = {n: h for n, h in reached}
parent = {}
for node, h in reached:
    if h == 0:
        continue
    for neighbor, _w in graph.neighbors(node):
        if hop_of.get(neighbor) == h - 1:
            parent[node] = neighbor
            break
fig, ax = plt.subplots(figsize=(11, 9), facecolor=CREAM)
ax.set_facecolor(CREAM)
for ring in RADIUS.values():
    ax.add_patch(plt.Circle((0, 0), ring, fill=False, color=BROWN, alpha=0.12, linestyle="--"))
for child, par in parent.items():
    ax.plot([pos[par][0], pos[child][0]], [pos[par][1], pos[child][1]], color=BROWN, alpha=0.30, linewidth=1.2, zorder=1)
for node, (x, y) in pos.items():
    color = TERRACOTTA if node == start else (MINT if in_yucatan(node) else PEACH)
    ax.scatter([x], [y], s=1300 if node == start else 330, color=color, edgecolor=BROWN, linewidth=0.9, zorder=2)
    if node == start:
        ax.text(x, y, "Mérida", ha="center", va="center", fontsize=11, color="white", fontweight="bold", zorder=3)
    else:
        ang = angle_of[node]
        lx, ly = (RADIUS[hop_of[node]] + 0.45) * math.cos(ang), (RADIUS[hop_of[node]] + 0.45) * math.sin(ang)
        ax.text(lx, ly, short(graph.names[node]), ha="left" if math.cos(ang) > 0.15 else ("right" if math.cos(ang) < -0.15 else "center"),
                va="center", fontsize=9, color=BROWN, zorder=3)
ax.scatter([], [], s=200, color=MINT, edgecolor=BROWN, label="Yucatán")
ax.scatter([], [], s=200, color=PEACH, edgecolor=BROWN, label="Other state (neighbor in code space)")
ax.legend(loc="lower center", ncol=2, frameon=False, labelcolor=BROWN, bbox_to_anchor=(0.5, -0.02))
ax.set_title("Mérida's network within 2 hops (BFS)\ninner ring = 1 hop, outer ring = 2 hops", color=BROWN, fontsize=14, pad=10)
ax.set_xlim(-8.2, 8.2)
ax.set_ylim(-6.6, 6.6)
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT + "bfs_rings.png", dpi=160, facecolor=CREAM)
plt.close(fig)

# ---------- 3) Dijkstra: cumulative cost along the cheapest route ----------
total, route = dijkstra(graph, start, goal)
route = [n for n in route]
cost, running = [0], 0
for a, b in zip(route, route[1:]):
    running += min(w for nb, w in graph.neighbors(a) if nb == b)
    cost.append(running)
fig, ax = plt.subplots(figsize=(9.5, 5), facecolor=CREAM)
style(ax)
ax.step(range(len(route)), cost, where="post", color=TERRACOTTA, linewidth=2.4)
ax.scatter(range(len(route)), cost, s=110, color=MINT, edgecolor=BROWN, zorder=3)
for i, node in enumerate(route):
    ax.annotate(short(graph.names[node]), (i, cost[i]), textcoords="offset points", xytext=(-6, 9),
                ha="right", fontsize=8.5, color=BROWN)
ax.set_xticks(range(len(route)))
ax.set_xlabel("Step along the route", color=BROWN)
ax.set_ylabel("Accumulated cost", color=BROWN)
ax.set_ylim(-1.5, total + 3)
ax.set_title(f"Cheapest route Mérida to Tizimín (Dijkstra, total cost {total})", color=BROWN, fontsize=14, pad=12)
fig.tight_layout()
fig.savefig(OUT + "shortest_path.png", dpi=160, facecolor=CREAM)
plt.close(fig)
print("figures saved; route cost", total, "hops", len(route) - 1)
