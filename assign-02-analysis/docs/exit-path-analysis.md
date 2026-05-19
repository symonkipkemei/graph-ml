# Exit Path Analysis — Process Documentation

## What It Does
Identifies all exit points in the building and computes the shortest evacuation path from every interior room to the building exterior. The circulation graph is rebuilt with `toExteriorApertures=True`, which adds one **exterior node** representing the space outside the building envelope. Every edge connecting to this node is an exterior-facing aperture — a door or window on the building boundary.

This directly answers **Goal 2** from the report: what are all the exit points in the building, and how far is each room from them?

---

## Geometry Preparation (Rhino)

| File | Contents |
|------|----------|
| `box-house-rooms.obj` | All room volumes as a single merged surface model |
| `box-house-doors.obj` | Door opening surfaces only |
| `box-house-windows.obj` | Window opening surfaces only |

Same geometry as Assignment 01. The exterior node is generated automatically by `Graph.ByTopology` — no additional geometry is required.

---

## Notebook Pipeline

### Step 1 — Load Geometry and Add Apertures
Same as A02-01: load OBJ files, flatten and colour-code apertures, build CellComplex, register apertures with `Topology.AddApertures`.

### Step 2 — Build Exit Circulation Graph
```python
g_exit = Graph.ByTopology(cc,
                           direct=False,
                           viaSharedApertures=True,
                           toExteriorApertures=True)
```
The only change from the standard circulation graph is `toExteriorApertures=True`. This adds:
- One extra vertex for the building exterior
- One edge per exterior-facing aperture connecting an interior room to the exterior vertex

| Parameter | A02-01 value | A02-03 value | Effect of change |
|-----------|-------------|-------------|-----------------|
| `toExteriorApertures` | `False` | `True` | Adds exterior node + exit edges |

### Step 3 — Identify the Exterior Node
```python
degrees      = [Graph.VertexDegree(g_exit, v) for v in exit_verts]
exterior_idx = degrees.index(max(degrees))
exterior_v   = exit_verts[exterior_idx]
```
The exterior node is identified as the vertex with the highest degree in the graph. It connects to every interior room that has an exterior-facing aperture, so its degree equals the number of exit openings on the building envelope.

Interior room vertices are all remaining vertices:
```python
interior_verts = [v for i, v in enumerate(exit_verts) if i != exterior_idx]
```

### Step 4 — Visualise Exit Graph
Exit edges (those touching the exterior node) are highlighted in orange; interior edges are grey; the exterior node is shown in yellow.

### Step 5 — Compile Routing Graph and Compute All Exit Paths
```python
crg_exit = Graph.CompiledRoutingGraph(g_exit, precomputeTurns=False)

for rv in interior_verts:
    path = Graph.ShortestPath(crg_exit, vertexA=rv, vertexB=exterior_v)
```
`ShortestPath` is called once per interior room with `exterior_v` as the fixed destination. Rooms that have no aperture path to the exterior return `None`.

### Step 6 — Rank Rooms by Evacuation Distance
```python
connected.sort(key=lambda x: (x[1], x[2]))   # sort by hops, then path length
```
Rooms are ranked first by **hops** (structural depth from exit) and then by **Euclidean path length** as a tiebreaker. Hops are the primary metric because they reflect the number of room transitions required — a direct measure of how many doors must be opened to reach the outside.

### Step 7 — Visualise by Hops to Exit
Room nodes are coloured using the `RdYlGn_r` scale: green (1 hop — room directly adjacent to an exit opening) through red (maximum hops — deepest interior room). The exterior node is shown in yellow.

### Step 8 — Show Worst-Case Evacuation Path
The room with the most hops is highlighted in magenta. Its full evacuation path is drawn in orange over the building geometry.

---

## Key Lessons Learned

1. **`toExteriorApertures=True` adds exactly one exterior node** — All exterior-facing apertures converge on a single node representing the building exterior. It is not per-aperture; it is one shared node for the entire outside.

2. **Exterior node identification by highest degree is a heuristic** — It works reliably when the building has more exterior apertures than any interior hub room has connections. If an interior corridor has more edges than the total number of exterior openings, the heuristic will misidentify the corridor as the exterior node. Verify the identified node's position against the building envelope.

3. **`None` return means no path to exterior** — A room with `None` result has no aperture-connected path to any exterior-facing opening. This can happen for rooms on upper floors (no stair apertures) or rooms that are completely enclosed with no registered apertures.

4. **Hops ≠ doors** — Each hop is a room transition, not a door opening. One hop from room A to the exterior means room A directly shares an exterior-facing aperture. Two hops means room A must first transit through one intermediate room.

5. **The exterior node must be excluded from interior analysis** — When iterating over vertices for room-level queries, the exterior node must be filtered out. It is not a room and its position (typically at the building centroid or origin) is not meaningful architecturally.

---

## Shortcomings

### 1. Exterior Node Heuristic May Misfire
The exterior node is identified by the highest degree. In buildings where an interior corridor or atrium connects to many rooms, that interior hub may have a higher degree than the total number of exterior openings. Manual verification of the identified node's coordinates against the building envelope is required.

### 2. Multi-Floor Exit Paths Are Broken
Stair apertures (horizontal openings between floors) are not modelled. Rooms on upper floors appear disconnected from the ground floor and return `None` for all exit path queries. Vertical evacuation routes cannot be analysed without modelling stair shafts as aperture-bearing horizontal faces.

### 3. No Exit Type Distinction
All exterior-facing apertures are treated as equivalent exits. Exterior doors (primary exits) and exterior windows (emergency egress only) produce identical edges. Filtering by aperture type (`"door"` vs `"window"`) would require querying the aperture dictionary on each exit edge.

### 4. No Edge Weights — Evacuation Distance is Structural Only
Hops and Euclidean centroid distance are both structural approximations. They do not account for corridor width, stair descent time, door swing clearance, or occupant flow capacity. A fire engineering model would require weighted edges and flow simulation.

### 5. Single Exterior Node Cannot Distinguish Exit Locations
All exterior-facing apertures route to one shared exterior node. The analysis reports the shortest path to *any* exit, but cannot directly compare paths to *specific* exits (e.g. north door vs south door). Modelling each exit as a distinct terminal node would require a custom graph build rather than `Graph.ByTopology`.

### 6. No Room Labels
Exit ranking output is by vertex index. Without named OBJ groups, the room at rank 1 (nearest exit) cannot be automatically identified as "main lobby" or "ground floor corridor".
