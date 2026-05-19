# Centrality Analysis — Process Documentation

## What It Does
Applies two graph centrality metrics to the circulation graph to characterise the spatial role of each room within the building's movement network:

| Metric | Question answered | Space syntax equivalent |
|--------|------------------|------------------------|
| **Closeness centrality** | Which room is easiest to reach from everywhere else? | Global integration |
| **Betweenness centrality** | Which rooms lie on the most shortest paths? | Choice |

A high closeness score identifies rooms that are topologically shallow — reachable quickly from any other room. A high betweenness score identifies structural hub rooms whose removal would most disrupt circulation through the building.

---

## Geometry Preparation (Rhino)

| File | Contents |
|------|----------|
| `box-house-rooms.obj` | All room volumes as a single merged surface model |
| `box-house-doors.obj` | Door opening surfaces only |
| `box-house-windows.obj` | Window opening surfaces only |

Same geometry as Assignment 01.

---

## Notebook Pipeline

### Step 1 — Load Geometry and Build Circulation Graph
Same setup as A02-01: load OBJ files, flatten apertures, build CellComplex, register apertures, and build the circulation graph with `direct=False, viaSharedApertures=True, toExteriorApertures=False`.

### Step 2 — Closeness Centrality
```python
cc_values = Graph.ClosenessCentrality(g_circ, colorScale="thermal")
```
`Graph.ClosenessCentrality` computes the reciprocal of the mean shortest-path distance from each node to all reachable nodes. It writes two keys to each vertex dictionary:
- `"closeness_centrality"` — the numeric score
- `"cc_color"` — a hex colour string mapped from the score on the chosen colour scale

The return value is a list of numeric scores, one per vertex, in the same order as `Graph.Vertices(g_circ)`.

Results are printed with the most and least central rooms flagged:
```python
best_i  = cc_values.index(max(cc_values))   # most central room
worst_i = cc_values.index(min(cc_values))   # least central room
```

### Step 3 — Visualise Closeness
```python
Topology.Show(cc, g_circ,
              vertexSize=18,
              vertexColorKey="cc_color",
              ...)
```
The `cc_color` key written by `ClosenessCentrality` is passed directly as `vertexColorKey`. No manual colour mapping is needed.

### Step 4 — Betweenness Centrality
```python
bc_values = Graph.BetweennessCentrality(g_circ, normalize=True, colorScale="thermal")
```
`normalize=True` scales scores to the range [0, 1], making them comparable across graphs of different sizes. Two keys are written per vertex:
- `"betweenness_centrality"` — the numeric score
- `"bc_color"` — a hex colour string

### Step 5 — Visualise Betweenness
```python
Topology.Show(cc, g_circ,
              vertexSize=18,
              vertexColorKey="bc_color",
              ...)
```

### Step 6 — Side-by-Side Comparison
```python
combined = sorted(
    zip(range(len(cc_values)), cc_values, bc_values),
    key=lambda x: x[1],
    reverse=True
)
```
Rooms are sorted by closeness (descending) and printed alongside their betweenness score. Rooms that rank high on both metrics are the most spatially critical — they are both accessible and heavily used as transit points.

---

## Key Lessons Learned

1. **`ClosenessCentrality` and `BetweennessCentrality` write colour keys directly to vertices** — After calling either function, the `cc_color` or `bc_color` key is available on every vertex dictionary. `Topology.Show` can use these keys directly via `vertexColorKey` without any manual colour assignment.

2. **`normalize=True` in `BetweennessCentrality` is important for small graphs** — Raw betweenness counts can be very small on a 19-node graph (maximum possible paths is limited). Normalising scales the scores to [0, 1], making the relative differences between rooms legible.

3. **Disconnected components affect closeness** — If the graph has isolated rooms (no aperture connections to the rest), closeness centrality returns `0` for those nodes. They are unreachable from the main network and appear as cold nodes on the thermal scale.

4. **Both metrics operate on the unweighted graph** — All edges are treated as having equal cost. This makes the scores reflect topological depth (hop count), not physical walking distance.

5. **High closeness ≠ high betweenness** — A room can be spatially central without being a structural hub (e.g. a well-connected room in a cluster where many alternative paths exist). Cross-referencing both metrics is needed to identify the most architecturally critical spaces.

---

## Shortcomings

### 1. Unweighted Graph Ignores Physical Distance
Both metrics are computed on an unweighted graph. A room one hop away across a long corridor and a room one hop away through a doorway immediately adjacent are treated identically. Adding edge weights (e.g. door-to-door Euclidean distance) would produce architecturally more meaningful centrality scores.

### 2. No Room Labels
All centrality output is by vertex index only. The scores cannot be mapped to room types (corridor, bedroom, kitchen) without a manual index-to-name table, which the current OBJ export does not provide.

### 3. Small Graph — Relative Differences May Be Subtle
With 19 nodes, the range of both metrics may be narrow. Rooms in a regular grid-like layout will cluster tightly in centrality score, making it difficult to draw strong conclusions about individual rooms.

### 4. Disconnected Nodes Skew Closeness
Rooms that have no aperture connections (isolated nodes) receive a closeness score of `0`. This drags the minimum down and compresses the visible range for the thermal colour scale, making differences between connected rooms harder to read visually.

### 5. Betweenness Ignores Flow Direction
Betweenness centrality counts all-pairs shortest paths equally. It does not account for the actual frequency or directionality of movement in the building (e.g. all occupants entering from one direction). A flow-weighted analysis would require observed or modelled movement data.

### 6. Multi-Floor Analysis Not Possible
Without stair apertures, upper-floor rooms form isolated components. Centrality is computed only within each connected component, so cross-floor comparisons are not meaningful.
