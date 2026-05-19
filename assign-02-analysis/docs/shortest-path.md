# Shortest Path Between Rooms

## The Problem

A building is only useful if its occupants can move through it. The design question is not just whether rooms exist, but whether they are reachable — and at what cost. Given any two rooms in the Box House, what is the minimum sequence of spaces an occupant must pass through to travel from one to the other, using only actual doors and windows?

This is a wayfinding problem. It cannot be answered by looking at the floor plan alone, because floor plan adjacency does not guarantee passage. Two rooms can share a wall with no opening between them. The question requires a model of movement, not just a model of space.

---

## Why This Approach

The circulation graph encodes the building's movement network exactly. Each node is a room. Each edge exists only where a registered aperture — a door or window — sits on the shared wall between two rooms. There are no hypothetical shortcuts; the graph reflects the actual openings modelled in Rhino.

Shortest path on this graph finds the minimum-hop route through the aperture network. It answers the wayfinding question structurally: not the shortest straight-line distance through walls, but the fewest room transitions through real openings. The result is a sequence of rooms that mirrors what an occupant would actually experience walking through the building.

The batch analysis — querying multiple room pairs in one pass — builds a picture of travel distances across the whole building. Some pairs of rooms are one or two transitions apart; others may require traversing several intermediate spaces. This variation is not visible from the floor plan.

---

## Findings

The shortest path analysis on the Box House reveals the depth structure of the building — how many spaces separate any two rooms when movement is constrained to real openings.

**Connectivity** — Not every room can reach every other room. Rooms on separate floors appear as isolated nodes in the graph because stair connections are not modelled as apertures. Any pair involving an upper-floor room returns no path, confirming that the graph currently models only horizontal circulation within each floor.

**Travel depth** — Within a connected floor, the maximum path between any two rooms is a measure of how labyrinthine the layout is. A shallow building (low maximum hops) means all rooms are close to each other through the aperture network. A deep building means some rooms are effectively remote even if they appear spatially adjacent on the floor plan.

**Disconnected rooms** — Any room that returns `None` for all path queries has no aperture-connected route to the rest of the building. This is a modelling flag: either the room genuinely has no door (an enclosed space), or an aperture was not registered correctly during geometry preparation.

---

## Limitations

The path length reported is Euclidean centroid-to-centroid distance — a topological approximation, not a measured walking distance. It does not account for where within a wall a door is placed, or the detour required to reach a door offset from the room centre.

All transitions are treated as equal regardless of opening type or width. The path does not distinguish between a wide corridor opening and a narrow bathroom door.

Room nodes carry no names. Path output is expressed as vertex indices (`0 → 3 → 7 → 12`), not room labels. Interpretation requires cross-referencing the vertex coordinate table with the building model.
