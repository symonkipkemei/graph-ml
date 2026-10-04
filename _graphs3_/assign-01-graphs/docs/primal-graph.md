# Primal Graph — Process Documentation

## What It Does
Builds a graph directly from the geometric topology of the CellComplex — every physical vertex becomes a graph node and every physical edge becomes a graph edge. The result is a dense wire-frame representation of the building geometry as a graph, preserving the exact spatial structure of all surfaces and volumes.

This is distinct from the dual graph, where one node represents an entire room. In the primal graph, a single room may contribute dozens of nodes and edges.

---

## Geometry Preparation (Rhino)

| File | Contents |
|------|----------|
| `box-house-rooms.obj` | All room volumes as a single merged surface model |

No aperture files are needed — the primal graph uses only the structural geometry.

---

## Notebook Pipeline

### Step 1 — Load OBJ
```python
objects = Topology.ByOBJPath("box-house-rooms.obj", selfMerge=True)
```
Returns a single-item list containing one `Cluster` of all merged room surfaces.

### Step 2 — Remove Coplanar Faces on Raw Objects
```python
for o in objects:
    Topology.RemoveCoplanarFaces(o, 0.01)
```
Applied directly to the raw cluster before building the CellComplex. Cleans up faces that are coplanar within a tolerance of `0.01`.

### Step 3 — Show Raw Geometry
```python
Topology.Show(objects, faceOpacity=0.1, ...)
```
Visualises the raw imported cluster before any graph processing.

### Step 4 — Extract Cells and Build CellComplex
```python
cells = Topology.Cells(objects[0])
cc = CellComplex.ByCells(cells)
cc = Topology.RemoveCoplanarFaces(cc)
cc = Topology.RemoveCollinearEdges(cc)
```
Extracts 18 room cells from the cluster, assembles a clean `CellComplex`.

### Step 5 — Derive Primal Graph
```python
vertices = Topology.Vertices(cc)
vertices = [Topology.Copy(v) for v in vertices]
edges = Topology.Edges(cc)
edges = [Topology.Copy(e) for e in edges]
g1 = Graph.ByVerticesEdges(vertices, edges)
```
Every geometric vertex and edge of the CellComplex is copied and assembled into a graph using `Graph.ByVerticesEdges`. The copy step is required because topologicpy graph vertices must be independent objects — referencing the CellComplex vertices directly causes identity conflicts.

### Step 6 — Style and Visualise
```python
# Vertices: red, size 18
# Edges: black, width 4
Topology.Show(g1, ...)
Topology.Show(cc, g1, ...)  # overlaid
```

---

## Key Concept

| Graph type | Nodes | Edges |
|------------|-------|-------|
| Primal | Geometric vertices of the CellComplex | Geometric edges of the CellComplex |
| Dual | One node per room cell | Rooms sharing a face |
| Circulation | One node per room cell | Rooms sharing an aperture |
| Fenestration | Rooms + apertures | Room–aperture connections |

---

## Shortcomings

### 1. Dense and Hard to Read
A building with 18 rooms produces 90+ nodes and 160+ edges. The graph reflects all geometric vertices, including those introduced by surface subdivisions, making it visually complex and difficult to interpret spatially.

### 2. No Semantic Information
Nodes carry no room type, name, or function. Every vertex looks identical — there is no way to distinguish a corner of a corridor from a corner of a classroom without external mapping.

### 3. Redundant Geometry After Cleanup
`RemoveCollinearEdges` reduces some redundancy but collinear edges on curved or subdivided surfaces may persist, adding nodes that carry no topological meaning.

### 4. Sensitive to Modelling Precision
If the Rhino model has slightly misaligned vertices (within tolerance), `CellComplex.ByCells` may produce duplicate or near-duplicate vertices that appear as separate graph nodes very close together.

### 5. No Room-Level Abstraction
The primal graph cannot answer questions like "which rooms are adjacent?" without post-processing. It encodes geometry, not spatial relationships between spaces.
