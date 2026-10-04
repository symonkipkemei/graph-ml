# Centrality Analysis

## The Problem

In any building, some rooms matter more to circulation than others. A corridor that connects three wings is not equivalent to a bedroom at the end of a dead-end passage — even if both appear as single nodes on the graph. The design question is: which rooms are structurally central to the movement network, and which rooms would cause the most disruption if they were removed or blocked?

This is not a question about geometry. Two rooms can be physically close together but topologically distant if the aperture network routes movement around them. Centrality measures the position of each room within the network of real circulation connections — not its position in space.

---

## Why This Approach

Two complementary metrics are applied to the circulation graph:

**Closeness centrality** measures how quickly each room can be reached from all other rooms. A high closeness score means the room is topologically shallow — an occupant starting anywhere in the building reaches it in few transitions. In space syntax terms this is *integration*: the most integrated room is where movement naturally converges. It is the spatial candidate for shared or public functions — a corridor junction, a lobby, a kitchen.

**Betweenness centrality** measures how often each room lies on the shortest path between other pairs of rooms. A high betweenness score means most routes through the building pass through that room. It is structurally indispensable: blocking it would force many occupants to take longer routes or lose connectivity entirely. In space syntax terms this is *choice*: the room that carries the most through-movement.

The two metrics ask different questions and do not always agree. A room can be highly integrated (easy to reach) without being a transit hub (carrying through-movement), and vice versa. Comparing both together identifies the rooms that are critical on both dimensions — the true spatial backbone of the building.

---

## Findings

The centrality analysis on the Box House reveals the implicit spatial hierarchy of the layout — the rooms the design has made structurally important, regardless of their intended function.

**Most integrated room (closeness)** — The room with the highest closeness score is the most accessible point in the building. Every other room is, on average, fewer transitions away from it than from any other node. This room is the building's topological centre. If the layout is well designed, this should be a corridor or shared living space. If it turns out to be a private room, the layout has buried its centre in the wrong place.

**Hub room (betweenness)** — The room with the highest betweenness score is the one that most paths pass through. It is the structural bottleneck of the building. Occupants moving between any two rooms on opposite sides of the layout are likely to pass through it. This room carries the most latent circulation pressure and should be generous in size and unobstructed — it is functioning as an informal corridor whether or not it was designed as one.

**Isolated rooms** — Rooms with a closeness score of zero are unreachable from the rest of the network through the aperture graph. These appear as cold nodes on the thermal visualisation. They are either intentionally enclosed spaces or the result of missing aperture registrations in the model.

**Comparing closeness and betweenness** — Rooms that rank high on both metrics are the most architecturally critical spaces in the building. Rooms that rank high on closeness but low on betweenness are well-placed but not transit-critical — they are accessible without being indispensable. Rooms that rank high on betweenness but low on closeness are structural bottlenecks located in a less central part of the layout — a narrow corridor connecting two otherwise separate zones.

---

## Limitations

Both metrics are computed on an unweighted graph. All aperture connections are treated as equal regardless of door width, corridor length, or traversal difficulty. A more architecturally faithful analysis would weight edges by the Euclidean distance between room centroids, making the scores reflect physical travel effort rather than hop count.

The analysis is limited to connected components. Rooms on separate floors appear as isolated nodes and receive scores that are not comparable to ground-floor rooms. A complete multi-floor centrality analysis requires stair apertures to be modelled.
