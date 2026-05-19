# Dual Graph — Process Documentation

## What It Does
Builds a graph where each room cell becomes a single node, and an edge is drawn between any two rooms that share a face. This is the spatial adjacency graph of the building — it answers the question "which rooms are physically next to each other?" without requiring any door or window to exist between them.

It is the topological dual of the primal graph: where the primal encodes geometry, the dual encodes spatial relationships between volumes.

---

## Geometry Preparation (Rhino)

| File | Contents |
|------|----------|
| `box-house-rooms.obj` | All room volumes as a single merged surface model |

No aperture files are needed.

---

## Notebook Pipeline

### Step 1 — Load OBJ
```python
objects = Topology.ByOBJPath("box-house-rooms.obj", selfMerge=True)
```
Returns a single `Cluster` containing all merged room surfaces.

### Step 2 — Show Raw Geometry
```python
Topology.Show(objects, faceOpacity=0.1, ...)
```
Visualises the imported cluster before graph processing.

### Step 3 — Extract Cells and Build CellComplex
```python
cells = Topology.Cells(objects[0])
cc = CellComplex.ByCells(cells)
cc = Topology.RemoveCoplanarFaces(cc)
cc = Topology.RemoveCollinearEdges(cc)
```
Extracts 18 cells and assembles a clean `CellComplex`. The cleanup steps reduce redundant faces and edges that would otherwise produce spurious graph connections.

### Step 4 — Derive Dual Graph
```python
g2 = Graph.ByTopology(cc, direct=True)
```
`Graph.ByTopology` with `direct=True` places one node at the internal vertex of each cell and draws an edge between any two cells that share a face. No apertures are considered — pure geometric adjacency.

### Step 5 — Style and Visualise
```python
# Vertices: red, size 18
# Edges: black, width 4
Topology.Show(g2, ...)
Topology.Show(cc, g2, ...)  # overlaid
```

---

## Key Concept: `direct=True`

The `direct` parameter in `Graph.ByTopology` controls the connection rule:

| `direct` | Meaning |
|----------|---------|
| `True` | Connect cells that share a face (regardless of apertures) |
| `False` | Do not use direct face-sharing as a connection criterion |

Setting `direct=True` alone produces the full adjacency graph. The circulation graph uses `direct=False` combined with `viaSharedApertures=True` to restrict connections to aperture-bearing faces only.

---

## Comparison with Other Graphs

| | Primal | Dual | Circulation | Fenestration |
|--|--------|------|-------------|--------------|
| Nodes | Geometric vertices | Rooms | Rooms | Rooms + apertures |
| Edges | Geometric edges | All shared faces | Aperture-bearing faces only | Room–aperture connections |
| Requires apertures | No | No | Yes | Yes |

---

## Shortcomings

### 1. Connects Rooms Without Physical Access
The dual graph edges represent shared wall faces, not passages. Two rooms sharing a wall will be connected even if that wall has no door. This overstates connectivity and cannot be used to answer circulation questions without combining it with aperture data.

### 2. Exterior Cell Included
The space outside the building boundary is also a `Cell` in the `CellComplex`. It will appear as a node in the dual graph connected to all rooms on the building perimeter. This exterior node must be filtered out manually if only interior connections are desired.

### 3. No Semantic Differentiation
All nodes are visually identical (red, size 18). There is no distinction between a corridor node, a stair node, or a classroom node. Room type information cannot be derived from `box-house-rooms.obj` because it has no named groups.

### 4. Sensitive to Coplanar Face Cleanup
If `RemoveCoplanarFaces` is not applied before building the dual graph, a single conceptual wall shared between two rooms may register as multiple coincident faces, producing multiple edges between the same pair of rooms.

### 5. No Edge Weights
All edges have equal weight. The dual graph does not encode the size of the shared face (a large open archway and a narrow structural gap produce identical edges).
