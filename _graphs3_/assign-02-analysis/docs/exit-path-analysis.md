# Exit Path Analysis

## The Problem

Every room in the Box House is a potential starting point for an occupant who needs to leave the building. The design question is: how many rooms must that occupant pass through before reaching the outside, and are there rooms so deep in the layout that evacuation becomes structurally difficult?

This is an egress problem. It is not answered by counting doors on the exterior walls — it requires tracing the actual path through the aperture network from each room to an exit. A room might be physically near an exterior wall but have no door leading to it, forcing the occupant to walk back through the interior and out through a different part of the building entirely.

---

## Why This Approach

The circulation graph already encodes the movement network of the building — rooms as nodes, apertures as edges. Adding the exterior as a single connected node transforms this wayfinding model into an egress model. Every exterior-facing door or window becomes an edge to the outside. The exterior node is not a room; it is the destination.

Shortest path from every room to this exterior node measures **topological evacuation distance** — the minimum number of room transitions required to reach the building's boundary. Ranking rooms by this distance surfaces the building's egress hierarchy: which rooms can exit directly, which require one intermediate space, and which are buried deep enough in the layout that evacuation requires traversing several rooms in sequence.

This framing also identifies the **worst-case room** — the room with the longest evacuation path. In building safety terms, this is the space most exposed to risk: the one that places the most transitions between the occupant and the outside.

---

## Findings

The exit path analysis on the Box House maps the egress structure of the building — the relationship between each room's position in the layout and its distance from safety.

**Exit-adjacent rooms (1 hop)** — Rooms with a path length of one hop share an exterior-facing aperture directly with the outside. Their occupants can exit without passing through any other room. These rooms are the building's primary egress points.

**Intermediate rooms (2–3 hops)** — Most interior rooms require one or two transit spaces before reaching an exit. These rooms depend on their neighbours' connections to the exterior. The path quality depends on whether those intermediate spaces are corridors (purpose-built for movement) or functional rooms (bedrooms, kitchens) that occupants are passing through incidentally.

**Deep interior rooms** — The rooms with the highest hop count are the most isolated from the exterior. The worst-case room highlights a potential egress weakness in the layout: an occupant in that room must traverse the maximum number of spaces before reaching safety. Whether this is acceptable depends on the function of the room and the intended occupancy.

**Exit distribution** — The number of edges connecting the exterior node reveals how many distinct exit openings the building has. A high count means exits are distributed across the envelope; a low count means most evacuation routes converge on the same opening, creating a bottleneck. The visualisation of exit edges (the orange edges radiating from the exterior node) makes this distribution spatially readable.

**Evacuation ranking** — The full room ranking from nearest to furthest exit gives the building's egress profile. A well-distributed layout produces a shallow ranking — most rooms are 1–2 hops away. A poorly distributed layout produces a long tail, with several rooms requiring 3 or more transitions.

---

## Limitations

The exterior is modelled as a single node — all exits are treated as equivalent. The analysis finds the shortest path to *any* exit, but cannot distinguish between a path to the front door versus a path to a small window on a back wall. A more granular model would assign separate terminal nodes to each distinct exit opening.

Rooms on upper floors return no evacuation path because stair apertures are not modelled. The analysis is currently limited to ground-floor horizontal circulation. Vertical egress — descending stairs to exit the building — is outside the scope of the current geometry.

Hop count is a structural proxy for evacuation difficulty, not a time-based measure. It does not account for corridor width, occupant density, door swing clearance, or the time required to traverse a large room versus a small one.
