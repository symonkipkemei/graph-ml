# Shortest Path Between Rooms — Process Documentation

## What It Does
Computes the shortest traversal path between any two rooms in the building using the circulation graph. `Graph.ShortestPath` returns the exact sequence of rooms an occupant must pass through — connected only by real door and window apertures. No solid walls are crossed.

This directly answers **Goal 1** from the report: how does an occupant move from point A to point B?

---

## Geometry Preparation (Rhino)

| File | Contents |
|------|----------|
| `box-house-rooms.obj` | All room volumes as a single merged surface model |
| `box-house-doors.obj` | Door opening surfaces only |
| `box-house-windows.obj` | Window opening surfaces only |

Same geometry as Assignment 01. No additional files are needed.

---

## Notebook Pipeline

### Step 1 — Load Geometry
```python
objects = Topology.ByOBJPath("box-house-rooms.obj", selfMerge=True)
doors   = Topology.ByOBJPath("box-house-doors.obj",   selfMerge=True)
windows = Topology.ByOBJPath("box-house-windows.obj", selfMerge=True)
```
Aperture clusters are flattened to individual faces and colour-coded (`"brown"` for doors, `"cyan"` for windows).

### Step 2 — Build CellComplex and Add Apertures
```python
cells = Topology.Cells(objects[0])
cc = CellComplex.ByCells(cells)
cc = Topology.RemoveCoplanarFaces(cc)
cc = Topology.RemoveCollinearEdges(cc)
cc = Topology.AddApertures(cc, aperture_faces, subTopologyType="face")
```

### Step 3 — Build Circulation Graph
```python
g_circ = Graph.ByTopology(cc,
                           direct=False,
                           viaSharedApertures=True,
                           toExteriorApertures=False)
```
Rooms connect only through aperture-bearing shared faces. Exterior openings are excluded here — they are handled in A02-03.

### Step 4 — Inspect Vertices
```python
g_verts = Graph.Vertices(g_circ)
for i, v in enumerate(g_verts):
    print(i, v.X(), v.Y(), v.Z())
```
Each vertex is one room centroid. Because `box-house-rooms.obj` has no named groups, rooms are identified by index only. The coordinate table is used to select meaningful start and end rooms.

### Step 5 — Compile Routing Graph and Find Shortest Path
```python
crg = Graph.CompiledRoutingGraph(g_circ, precomputeTurns=False)
shortest_path = Graph.ShortestPath(crg, vertexA=start_v, vertexB=end_v)
```
`CompiledRoutingGraph` pre-processes the graph into a structure optimised for repeated queries. `ShortestPath` returns a `Wire` — a sequence of edges connecting the centroids of the rooms along the route.

Path metrics are derived from the returned wire:
```python
hops   = len(Topology.Edges(shortest_path))   # number of room transitions
length = Wire.Length(shortest_path)            # Euclidean centroid-to-centroid sum
```

### Step 6 — Visualise
```python
# Start node: green, size 20
# End node:   blue,  size 20
# Path edges: yellow, width 6
# Other edges: grey, width 2
Topology.Show(cc, ap_cluster, g_circ, shortest_path, ...)
```

### Step 7 — Batch Query Multiple Pairs
```python
for (a_idx, b_idx) in pairs:
    path = Graph.ShortestPath(crg, vertexA=g_verts[a_idx], vertexB=g_verts[b_idx])
```
The compiled routing graph `crg` is reused across all queries, avoiding the overhead of recompiling for each pair.

---

## Key Lessons Learned

1. **`Graph.CompiledRoutingGraph` is required for `Graph.ShortestPath`** — `ShortestPath` accepts a compiled routing graph object, not the raw `Graph` directly. The compile step pre-builds internal data structures for efficient traversal.

2. **`ShortestPath` returns a `Wire`, not a vertex list** — The path is a topological `Wire` object. Use `Topology.Edges(path)` to count hops and `Wire.Length(path)` for Euclidean distance.

3. **`None` return means no path exists** — If the two rooms are not connected through any chain of apertures (disconnected graph component or isolated room), `ShortestPath` returns `None`. Always check before accessing path properties.

4. **Vertex selection by index, not coordinate** — Room nodes have no names. The inspect step (vertex index + coordinates table) is required before every analysis to map physical rooms to graph indices.

5. **`CompiledRoutingGraph` is reusable** — Compile once, query many times. For the batch multi-pair analysis, the same `crg` is used for all pairs without recompiling.

---

## Shortcomings

### 1. No Room Name Labels
`box-house-rooms.obj` has no `g RoomName` group entries. Path output is `0 → 3 → 7 → 12`, not `bedroom → corridor → living room → kitchen`. A manual index-to-name mapping must be maintained separately.

### 2. Euclidean Length is Not Walking Distance
`Wire.Length` sums the straight-line distances between room centroids. It does not account for the actual door position within the wall or the detour required to reach a door that is offset from the room centre. It is a topological approximation, not an architectural measurement.

### 3. Multi-Floor Paths Are Broken
Stair connections between floors require apertures on horizontal shared faces (floor/ceiling openings). These are not modelled. Rooms on upper floors appear as disconnected nodes or isolated components, and `ShortestPath` returns `None` for any cross-floor query.

### 4. No Edge Weights
All edges are treated as equally traversable. A narrow bathroom door and a wide open archway produce identical edges. Weighted shortest path (e.g. by door width or shared face area) is not implemented.

### 5. Hops Undercount Actual Transitions
Each edge in the path represents a room-to-room connection. If two rooms are connected through multiple stacked apertures (a door and a window on the same wall), only one edge appears in the graph — the hop count does not reflect the number of distinct openings available at each step.
