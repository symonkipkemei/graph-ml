# Circulation Graph — Process Documentation

## What It Does
Builds a graph where rooms are nodes and edges exist **only** between rooms that share a physical aperture (door or window). This is distinct from the dual graph, which connects all spatially adjacent rooms regardless of whether a passage exists between them.

---

## Geometry Preparation (Rhino)

Three separate OBJ files must be exported from Rhino:

| File | Contents |
|------|----------|
| `box-house-rooms.obj` | All room volumes as a single merged surface model |
| `box-house-doors.obj` | Door opening surfaces only |
| `box-house-windows.obj` | Window opening surfaces only |

Doors and windows must be modelled as **planar faces** positioned exactly on (or overlapping) the shared wall faces between rooms. The aperture matching is spatial — geometry that does not intersect a shared face will be ignored.

---

## Notebook Pipeline

### Step 1 — Load Rooms
```python
objects = Topology.ByOBJPath("box-house-rooms.obj", selfMerge=True)
```
`selfMerge=True` returns a single `Cluster` containing all room volumes merged. This is the pattern used in all notebooks in this project.

### Step 2 — Load and Flatten Apertures
```python
doors   = Topology.ByOBJPath("box-house-doors.obj",   selfMerge=True)
windows = Topology.ByOBJPath("box-house-windows.obj", selfMerge=True)
```
`selfMerge=True` returns each OBJ as a **Cluster**, not individual faces. `AddApertures` requires individual `Face` objects, so the clusters must be flattened:
```python
aperture_faces = []
for ap in doors:
    for f in (Topology.Faces(ap) or [ap]):
        Topology.SetDictionary(f, Dictionary.ByKeysValues(["color"], ["brown"]))
        aperture_faces.append(f)
for ap in windows:
    for f in (Topology.Faces(ap) or [ap]):
        Topology.SetDictionary(f, Dictionary.ByKeysValues(["color"], ["cyan"]))
        aperture_faces.append(f)
```
Color is stored in each face dictionary at this stage for later visualisation.

### Step 3 — Build CellComplex
```python
cells = Topology.Cells(objects[0])
cc = CellComplex.ByCells(cells)
cc = Topology.RemoveCoplanarFaces(cc)
cc = Topology.RemoveCollinearEdges(cc)
```
Extracts 18 cells from the cluster, assembles them into a `CellComplex`, and cleans up redundant geometry.

### Step 4 — Attach Apertures
```python
cc = Topology.AddApertures(cc, aperture_faces, subTopologyType="face")
```
Each aperture face is spatially matched against the faces of the CellComplex. A match registers the aperture on the shared face so the graph builder can detect it.

### Step 5 — Build Circulation Graph
```python
g_circ = Graph.ByTopology(cc,
                           direct=False,
                           viaSharedApertures=True,
                           toExteriorApertures=False)
```

| Parameter | Value | Reason |
|-----------|-------|--------|
| `direct` | `False` | Disables direct room-to-room edges (would produce the dual graph) |
| `viaSharedApertures` | `True` | Connects rooms only through shared aperture faces |
| `toExteriorApertures` | `False` | Excludes apertures on exterior (boundary) faces |

### Step 6 — Visualise
```python
Topology.Show(cc, ap_cluster, g_circ,
              faceColorKey="color", faceOpacity=0.15, ...)
```
Rooms, apertures, and the graph are overlaid in a single 3D view. Doors appear brown, windows cyan.

---

## Key Lessons Learned

1. **`selfMerge=True` produces Clusters** — `Topology.ByOBJPath` with `selfMerge=True` merges all objects into a single Cluster. Individual faces must be extracted with `Topology.Faces()` before passing to `AddApertures`.

2. **Parameter rename in v0.9.21** — The parameter `useApertures=True` used in earlier versions was replaced by `viaSharedApertures=True`. Code written against older examples will raise a `TypeError`.

3. **`direct=False` is essential** — Setting `direct=True` alongside `viaSharedApertures=True` would produce a supergraph (all adjacencies plus aperture connections), not a pure circulation graph.

4. **Aperture geometry must lie on shared faces** — Apertures placed on exterior walls are excluded by `toExteriorApertures=False`. Apertures that don't spatially intersect any CellComplex face will silently produce no edges.

---

## Shortcomings

### 1. No Room Type Classification
The exported `box-house-rooms.obj` is a single merged surface model with no named groups. Topologicpy reads the `name` key from OBJ group names (`g` prefix), but this OBJ has none. As a result, rooms cannot be automatically colour-coded by type (bedroom, corridor, etc.). A manual index-to-name mapping is required.

**Workaround:** Name each room object in Rhino before exporting so the OBJ contains `g RoomName` entries per object.

### 2. Surface Model — No Closed Room Breps
Walls are individual shared planar surfaces, not separate closed polysurfaces per room. This means rooms cannot be selected or named individually in Rhino via Object Properties. The `Cell.ByFaces()` approach used by classmates who exported per-room breps does not apply here.

### 3. Tolerance Sensitivity in Aperture Matching
`AddApertures` matches apertures to CellComplex faces by spatial proximity. If aperture geometry deviates from the face plane by more than the tolerance threshold (default `0.0001`), the aperture will not be registered and the corresponding edge will be missing from the graph.

### 4. Exterior Entry Points Not Represented
`toExteriorApertures=False` excludes all apertures on boundary faces (exterior walls). Entry doors from outside the building will not appear as graph edges. Set `toExteriorApertures=True` to include them, but note this will add connections to the exterior cell (outside space).

### 5. Multi-Floor Stair Connections
Stair connections between floors require apertures on horizontal shared faces (floor/ceiling openings). These are not modelled as apertures in the current setup. The stair cells appear as disconnected nodes unless floor-level apertures are explicitly exported and included.

### 6. Single-Building Scope
The current pipeline handles one building as a single CellComplex. Separate buildings or apartment units must each be processed independently and then merged if needed, as `CellComplex.ByCells` cannot span disconnected geometries.
