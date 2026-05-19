# Building Graph Analysis Report
## Wayfinding and Exit Point Analysis

**Project:** Box House — Graph-ML Assignment 01
**Author:** Symon Kipkemei
**Date:** 2026-04-29

---

## Objective

This project investigates how the spatial and topological structure of a building can be represented as a graph, with two primary analytical goals:

1. **Wayfinding** — understanding how an occupant can move from one room (point A) to another (point B), constrained by the actual doors and windows in the building.
2. **Exit Point Mapping** — identifying all openings on the building envelope that allow passage between interior space and the exterior.

Four graph representations were built progressively, each answering a different layer of the question. They are presented below in order from geometric foundation to circulation model.

---

## Graph 1 — Primal Graph: The Geometric Skeleton

### What it answers
"What is the exact geometric structure of this building?"

### How it works
Every vertex and edge in the `CellComplex` (the 3D volumetric model of all rooms) becomes a node and edge in the graph. A building with 18 rooms produces 90+ nodes and 160+ edges — one for every physical corner and wall intersection.

```python
vertices = [Topology.Copy(v) for v in Topology.Vertices(cc)]
edges    = [Topology.Copy(e) for e in Topology.Edges(cc)]
g1 = Graph.ByVerticesEdges(vertices, edges)
```

### Contribution to wayfinding goals
The primal graph is not directly useful for answering "how do I get from A to B?" — it encodes geometry, not spatial relationships between spaces. It is the **foundational layer** that all other graphs are derived from. It confirms the building model is topologically sound before higher-level analysis begins.

### Limitation
Nodes carry no semantic information. A corridor corner and a bedroom corner are indistinguishable.

---

## Graph 2 — Dual Graph: Room Adjacency

### What it answers
"Which rooms are physically next to each other?" (regardless of whether a door or window exists between them)

### How it works
Each room cell collapses to a single node placed at the room's internal centroid. An edge is drawn between any two rooms that share a wall face.

```python
g2 = Graph.ByTopology(cc, direct=True)
```

| Parameter | Effect |
|-----------|--------|
| `direct=True` | Connect rooms that share any face — pure geometric adjacency |

### Contribution to wayfinding goals
The dual graph gives the **theoretical maximum connectivity** of the building — the upper bound on where an occupant could go if every wall were passable. It is useful for:

- Identifying spatial clusters of rooms (zones, wings)
- Detecting isolated or poorly connected spaces
- Providing the baseline against which circulation restrictions (doors only) can be compared

### Critical limitation for wayfinding
Two rooms connected in the dual graph may share only a structural wall with no opening. A path found on the dual graph may require walking through a solid wall. **It cannot be used alone to answer movement questions.**

---

## Graph 3 — Circulation Graph: Movement Paths

### What it answers
"How can an occupant actually move through the building, using only real doors and windows?"

### How it works
This graph uses the same room-level nodes as the dual graph, but edges are only drawn where an aperture (door or window) exists on the shared face between two rooms.

```python
g_circ = Graph.ByTopology(cc,
                           direct=False,
                           viaSharedApertures=True,
                           toExteriorApertures=False)
```

| Parameter | Value | Reason |
|-----------|-------|--------|
| `direct` | `False` | Prevents edges from forming on shared walls without openings |
| `viaSharedApertures` | `True` | Draws an edge only where a door or window aperture is registered |
| `toExteriorApertures` | `False` | Excludes openings on exterior walls (entry doors are omitted here) |

### Answering "Point A to Point B"
The circulation graph is the **core wayfinding tool**. A shortest-path query on this graph (e.g. Dijkstra or BFS) directly returns the sequence of rooms an occupant must traverse to get from one room to another using real building openings.

For example: to move from a bedroom (node A) to a kitchen (node B), the graph path `A → corridor → living room → B` reflects only traversals through actual doors — no solid walls are crossed.

### Setup requirement
Apertures must be loaded and registered before the graph is built:

```python
# Load and flatten door and window faces
aperture_faces = [...]  # from Topology.ByOBJPath with selfMerge=True

# Register apertures on the CellComplex
cc = Topology.AddApertures(cc, aperture_faces, subTopologyType="face")

# Then build the graph
g_circ = Graph.ByTopology(cc, direct=False, viaSharedApertures=True, ...)
```

### Limitation for exit analysis
With `toExteriorApertures=False`, entry doors from outside the building are excluded. The circulation graph shows internal movement only. To model entry/exit from outside, this parameter must be set to `True` — but doing so adds an exterior cell node representing the outside.

---

## Graph 4 — Fenestration Graph: Opening-Level Detail

### What it answers
"Through exactly which opening does a person pass between two rooms, and what type of opening is it?"

### How it works
Every door and window becomes an **explicit node** in the graph (not just an edge condition). Edges connect rooms to apertures, and apertures to rooms — creating a tripartite structure: Room → Opening → Room.

```python
g_fen = Graph.ByVerticesEdges(room_vertices + aperture_vertices, graph_edges)
```

| Node colour | Represents |
|-------------|------------|
| Red | Room |
| Brown | Door |
| Cyan | Window |

### Contribution to exit point mapping
The fenestration graph makes every opening an addressable entity. By inspecting aperture nodes that connect to only **one** room node (instead of two), all exterior-facing openings can be identified — these are the building's exit points.

An exterior door connects: `Interior Room → Door node` (no second room on the other side — the exterior is not represented as a node by default).

An interior door connects: `Room A → Door node → Room B`.

This distinction lets the graph answer:
- How many exits does Room X have to the outside?
- Which openings are interior-only vs. exterior-facing?
- What type is each exit (door vs. window)?

---

## Combined Analysis: Answering the Two Goals

### Goal 1 — How does a user move from Point A to Point B?

| Step | Graph used | Question answered |
|------|------------|-------------------|
| 1 | Dual | Which rooms are spatially reachable at all? |
| 2 | Circulation | What is the valid path using real doors and windows? |
| 3 | Fenestration | Through which specific opening does each transition occur? |

The **circulation graph** is the primary tool. Run a shortest-path algorithm on it to return the room sequence. The **fenestration graph** augments this by identifying the exact door or window at each step along the path.

To include building entry and exit in the path (e.g. entering from outside), the circulation graph must be rebuilt with `toExteriorApertures=True`.

### Goal 2 — What are all the exit points in the building?

Exit points are openings on the building envelope — exterior-facing apertures. Two methods surface them:

**Method A — Fenestration graph (structural):**
Traverse all aperture nodes and select those connected to only one room node. These are the exterior apertures. Filter by type key `"door"` to find walkable exits; `"window"` for emergency or ventilation openings.

**Method B — Circulation graph with exterior enabled:**
Rebuild the graph with `toExteriorApertures=True`. All edges that connect to the exterior cell node represent exit-capable openings.

| Opening type | Role |
|--------------|------|
| Interior doors | Enable movement between rooms |
| Interior windows | Secondary connections (if modelled as apertures) |
| Exterior doors | Primary exits / entry points |
| Exterior windows | Emergency egress candidates |

---

## Shortcomings Relevant to These Goals

| Issue | Impact on wayfinding | Impact on exit analysis |
|-------|----------------------|------------------------|
| No room type classification (no named OBJ groups) | Cannot label path nodes as "corridor", "stair", etc. | Cannot automatically flag fire exits or emergency routes |
| `toExteriorApertures=False` by default | Entry/exit from outside excluded from paths | Exterior exits must be found via fenestration graph instead |
| Aperture geometry must intersect CellComplex face | A misplaced door in the model = missing edge = path blocked | A misplaced exterior door = exit not counted |
| No stair apertures modelled | Multi-floor paths are broken — stair cells appear disconnected | Stair shafts not counted as vertical exit routes |
| Exterior cell present in dual/circulation | Exterior appears as a node when `toExteriorApertures=True` — must be filtered | The exterior cell itself is not a room and should be excluded from room counts |
| No edge weights | All door transitions are treated as equally traversable | Cannot prioritise nearest or widest exit |

---

## Recommended Next Steps

1. **Name room objects in Rhino** before exporting so the OBJ contains `g RoomName` entries. This enables automatic room labelling on all graph nodes.
2. **Model stair apertures** as horizontal face openings between floors. Add them to the aperture export so multi-floor paths are connected.
3. **Set `toExteriorApertures=True`** in the circulation graph and filter the exterior node out of shortest-path results to enable true entry-to-room path analysis.
4. **Add edge weights** (shared face area, door width) to the circulation graph to support weighted shortest-path queries — e.g. find the widest exit rather than the geographically nearest.
5. **Apply graph path query** (BFS or Dijkstra via `Graph.ShortestPath`) on the circulation graph to produce a formal A→B traversal report for any room pair.
