# Fenestration Graph — Process Documentation

## What It Does
Extends the dual graph by making every door and window an explicit node. Rather than drawing a direct room-to-room edge, the graph branches through the aperture: each door or window becomes an intermediate node connected to the rooms on either side of it.

This allows the graph to answer not just "which rooms are connected?" but also "through what opening?" — and to compare the number, type, and position of openings per room.

---

## Geometry Preparation (Rhino)

| File | Contents |
|------|----------|
| `box-house-rooms.obj` | All room volumes as a single merged surface model |
| `box-house-doors.obj` | Door opening surfaces only |
| `box-house-windows.obj` | Window opening surfaces only |

Aperture faces must be planar and positioned on (or overlapping) the shared wall faces of the room model.

---

## Notebook Pipeline

### Step 1 — Load OBJ Files
```python
objects = Topology.ByOBJPath("box-house-rooms.obj", selfMerge=True)
doors   = Topology.ByOBJPath("box-house-doors.obj",   selfMerge=True)
windows = Topology.ByOBJPath("box-house-windows.obj", selfMerge=True)
```
All three return `Cluster` objects. Doors and windows must be flattened to individual faces.

### Step 2 — Flatten and Colour-Code Apertures
```python
door_faces, window_faces = [], []
for ap in doors:
    for f in (Topology.Faces(ap) or [ap]):
        Topology.SetDictionary(f, Dictionary.ByKeysValues(["color", "type"], ["brown", "door"]))
        door_faces.append(f)
for ap in windows:
    for f in (Topology.Faces(ap) or [ap]):
        Topology.SetDictionary(f, Dictionary.ByKeysValues(["color", "type"], ["cyan", "window"]))
        window_faces.append(f)
aperture_faces = door_faces + window_faces
```
`selfMerge=True` returns a `Cluster` for doors and windows. `Topology.Faces()` extracts individual `Face` objects. Each face receives a `color` and `type` dictionary entry at this stage, which flows through to the final graph node colour.

### Step 3 — Build CellComplex and Add Apertures
```python
cells = Topology.Cells(objects[0])
cc = CellComplex.ByCells(cells)
cc = Topology.RemoveCoplanarFaces(cc)
cc = Topology.RemoveCollinearEdges(cc)
cc = Topology.AddApertures(cc, aperture_faces, subTopologyType="face")
```
`AddApertures` spatially matches each aperture face against the CellComplex faces. A matched face stores the aperture object so it can be retrieved later via `Topology.Apertures(face)`.

### Step 4 — Build the Graph (Custom)
Unlike the dual and circulation graphs, the fenestration graph is built manually using `Graph.ByVerticesEdges`:

```python
# Room nodes — one per cell at its internal vertex
room_vertices = []
for c in Topology.Cells(cc):
    v = Topology.InternalVertex(c)
    Topology.SetDictionary(v, {"type": "room", "color": "red", "size": 18})
    room_vertices.append(v)

# Aperture nodes + edges
aperture_vertices, graph_edges = [], []
for face in Topology.Faces(cc):
    apers = Topology.Apertures(face)
    if not apers:
        continue
    adj_cells = Topology.SuperTopologies(face, cc, topologyType="cell")
    for ap in apers:
        av = Topology.Centroid(ap)          # one node per aperture at its own centroid
        Topology.SetDictionary(av, {"type": ap_type, "color": color, "size": 12})
        aperture_vertices.append(av)
        for adj_cell in adj_cells:          # connect to each room on either side
            best_room_vertex = ...          # matched by centroid proximity
            graph_edges.append(Edge.ByVertices([av, best_room_vertex]))

g_fen = Graph.ByVerticesEdges(room_vertices + aperture_vertices, graph_edges)
```

**Key decisions:**
- Aperture node position: `Topology.Centroid(ap)` — the centroid of the aperture face itself, not the wall face. This ensures two windows on the same wall produce two distinct nodes at different positions.
- Room matching: nearest room vertex by Euclidean distance from `Topology.Centroid(adj_cell)`. Used because `adj_cells` returns CellComplex cells, which cannot be directly compared to the manually-created `room_vertices` by object identity.

### Step 5 — Style and Visualise
```python
# Room nodes:    red,   size 18
# Door nodes:    brown, size 12
# Window nodes:  cyan,  size 12
# Edges:         black, width 3
Topology.Show(g_fen, ...)
Topology.Show(cc, ap_cluster, g_fen, ...)  # overlaid with geometry and aperture faces
```

---

## Node Legend

| Node colour | Represents |
|-------------|------------|
| Red | Room cell |
| Brown | Door aperture |
| Cyan | Window aperture |

---

## Comparison with Circulation Graph

| | Circulation | Fenestration |
|--|-------------|--------------|
| Apertures as nodes | No — used only as edge condition | Yes — explicit nodes |
| Room-to-room edges | Direct (room A — room B) | Via aperture (room A — door — room B) |
| Graph builder | `Graph.ByTopology` | `Graph.ByVerticesEdges` (custom) |
| Two windows same wall | Indistinguishable | Two separate nodes |

---

## Shortcomings

### 1. Room Matching by Proximity May Fail for Complex Layouts
Adjacent cells are matched to room vertices by finding the nearest centroid. In very dense or irregular layouts where room centroids are close together, a cell may be matched to the wrong room vertex.

### 2. Aperture Nodes Have No Room Identity
An aperture node knows its own type (door/window) and colour but not which rooms it connects. The room-aperture relationship is encoded only in the graph edges, not in the node dictionary.

### 3. Exterior Apertures Not Distinguished
Windows on exterior walls are matched to only one adjacent cell (the interior room). The exterior is not represented as a node, so exterior-facing windows appear as dangling edges connected to one room only. This is correct topologically but loses the distinction between interior and exterior fenestration.

### 4. No Aperture Size or Orientation Data
All aperture nodes are treated equally regardless of the physical size of the opening. A floor-to-ceiling glazed wall and a small bathroom window produce identical nodes.

### 5. Depends on Aperture Geometry Alignment
If an aperture face does not spatially intersect a CellComplex face within the matching tolerance, `Topology.Apertures(face)` returns nothing for that face and the aperture is silently dropped from the graph.

### 6. No Room Type Classification
Same limitation as all other graphs in this project — `box-house-rooms.obj` has no named groups, so room types cannot be inferred automatically.
