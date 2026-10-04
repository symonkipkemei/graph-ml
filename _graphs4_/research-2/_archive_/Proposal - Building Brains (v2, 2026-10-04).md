# Research Proposal 2 — Building Brains: Decoding Residential Buildings for the Last 50 Metres of Delivery

| | |
|---|---|
| **Author** | Symon Kipkemei |
| **Supervisor** | Prof. Wassim Jabi, Cardiff University |
| **Topic** | Building graphs for AEC: buildings for autonomous agents |
| **Duration** | 3 months |
| **Status** | Draft |
| **Version** | v2, 2026-10-04 |

---

## 1. Summary

Delivery to the **building entrance** is a largely solved problem: couriers, sidewalk robots and route-optimised logistics get goods to the door. The **last 50 metres** are not solved. From the entrance, an autonomous agent must get through a lobby, choose and ride the right lift, follow a corridor, find "Apt 7B", and possibly climb an internal stair inside a three-level apartment to reach the kitchen. Each step needs knowledge of the building that a robot does not have, but the building's own design data does.

This thesis decodes a residential building's own data, a **verified BIM model checked against a point cloud**, into a **topological "building brain"** that lets delivery agents find their way from the entrance to a room inside an apartment. It **solves for the brain, not the body**: robots are **simulated agents moving through a TopologicPy model**. The method extends the navigation-graph and multi-agent work of Jabi et al. (2025) from hypothetical offices to a real residential building, from one kind of agent to several, and from movement alone to delivery tasks.

The outcome is an assessment of **delivery readiness**: which units and rooms each kind of agent can reach, how long deliveries take, where and why they fail, and which changes to the building would help most.

## 2. Problem

### 2.1 The last 50 metres

Getting a delivery from the entrance to a room breaks into stages. Each stage is a question the agent must answer:

| Stage | What the agent must work out |
|---|---|
| 1. Entrance → lobby | Which entrance to use; where access is controlled |
| 2. Address → place | Which part of the building *is* "Apt 7B": matching the human address to a location |
| 3. Vertical movement | Which lift serves the target level; lift or stairs; how long the wait is |
| 4. Corridor → unit door | The route along the corridor, and what is physically in the way (bikes, clutter, narrow passages) |
| 5. Inside the unit | In a multi-level apartment: can this agent reach the target room, or must it hand over at the entry level? |
| 6. Rules | Which spaces are public, shared or private; where the agent may wait |

### 2.2 Why this is unsolved

- **Robots don't read buildings.** Delivery robots that work indoors usually need each building mapped before they can operate, and integrations built for that building (for example, with the lifts). They don't use the design data the building already has. *(To verify in the literature review.)*
- **Building data already holds the answers.** A BIM model knows the levels, lifts, stairs, unit numbers, room uses and which doors connect what. As Smith (2026) puts it, "BIMs are what BIMs always promised to be: highly accurate, labeled spatial data". But that data is not in a form an agent can reason over.
- **BIM is idealised; real buildings are not.** Corridors fill with bikes and furniture, and doors get narrowed or blocked. A brain built only from the model will plan routes that fail in reality.
- **Existing agent simulation in architecture stops short.** Jabi et al. (2025) built TopologicPy navigation graphs and agents with schedules, but on **hypothetical single-floor offices**, with **identical human agents**, **modelled furniture**, and, as their own limitations section says, **no validation against real-world data**.

## 3. Research questions

**Main question:** Can a residential building's own data (a verified BIM model plus a point cloud) be turned into a topological brain that lets delivery agents find their way over the last 50 metres, from the building entrance to a room inside an apartment?

1. **Representation:** what must the brain contain to support the last 50 metres? Candidates: a graph organised by level, lifts and stairs, mapping from addresses to places, access levels, real clearances.
2. **Reality:** how much does checking the brain against the point cloud change what is reachable and which deliveries succeed, compared with a brain built from the model alone?
3. **Agent capability:** how does delivery readiness differ between kinds of agent (a wheeled robot that cannot climb stairs vs a legged or humanoid agent that can), especially inside multi-level units?
4. **Readiness:** can the simulation identify the **smallest set of changes** to the building (for example, widen a door, add a door opener, clear a corridor, give lift access) that most improves delivery readiness?

## 4. Users

- **Primary:** owners and facility managers of residential buildings deciding whether and how to support autonomous delivery, and delivery or robotics operators assessing a building before deploying.
- **Secondary:** architects designing new residential buildings or renovating existing ones to be "robot-ready". This links to Proposal 1.

## 5. Data

| Data | Role |
|---|---|
| Verified as-built Revit model | Source of the brain: levels, lifts, stairs, units, rooms, room uses, doors, entrances |
| Point cloud of the same building | Physical reality: obstacles, real clear widths, blocked routes. Also the **ground truth** for whether a route is physically passable |
| *(Optional)* MSD apartment dataset / Jabi's generated residential datasets | Test whether the brain-building method works across many apartment layouts, in graph form only |

> **Key assumption to confirm:** this proposal needs the data to cover a **multi-storey residential building**, ideally with multi-level units. If the available model and scan cover a different building type, the setting must be adjusted or other data found.

## 6. Method

1. **Extract the building.** Export levels, units, rooms, doors, stairs, lifts and entrances from Revit (C# Revit API) into a TopologicPy CellComplex, reusing the pipeline from `_graphs3_/assign-01` and `assign-02`.
2. **Build the brain** as a graph organised in levels: building → level → unit → room, with these layers:
   - **Topology:** places (rooms, corridors, lobbies) and connections (doors, stairs, lifts). Lifts are connections between levels, with a waiting time.
   - **Addresses:** each unit number and room name is linked to its node in the graph, so "Apt 7B, kitchen" resolves to a target.
   - **Clearances:** distances and clear widths from the model, corrected with the scan.
   - **Rules:** access levels (public, shared, private) and permitted waiting and hand-over zones.
   - **Reality:** obstacles and narrowed or blocked passages measured from the point cloud.
3. **Agent profiles.** Each agent type has a width (or radius), can or cannot climb stairs, can or cannot open doors, and has access rights. Following Jabi et al. (2025), the navigation surface is **offset by each agent's own radius**, so each agent type gets its own navigation graph.
4. **Simulation.** Simulated delivery agents receive tasks ("deliver to Apt 7B, kitchen"), plan routes on the brain with shortest-path search, and move through the TopologicPy model. **Resident agents with daily schedules**, following Jabi et al.'s schedule method, create realistic congestion in lifts and corridors. Meetings between delivery agents and residents are recorded using the same distance calculations between agents.
5. **Readiness and changes.** Combine the results per unit and per level into a delivery-readiness profile. Test candidate changes to the building and rank them by how much they improve it.
6. **Optional chat layer.** Delivery tasks given in natural language are turned into queries on the brain.

## 7. Validation tool

The validation tool is a **delivery-readiness simulator** for residential buildings.

- **Input:** the verified Revit model, the point cloud, agent profiles, resident schedules and delivery tasks.
- **Output:**
  - the building brain (a graph organised by level)
  - simulated delivery routes, with success or failure and the cause of each failure
  - a delivery-readiness map by unit and level
  - a ranked list of changes to the building

## 8. Evaluation

| What is tested | How | Metric |
|---|---|---|
| **Effect of reality** | The same deliveries planned on a model-only brain and on a model + scan brain | Share of planned routes that are physically passable (checked against the scan); share of failures the model-only brain does not foresee |
| **Agent capability** | Deliveries to every unit and room by each agent type | Share of units and rooms reachable; where hand-overs are needed |
| **Congestion** | Deliveries during busy and quiet times of day, using resident schedules | Delivery time; lift waiting time; meetings in passages too narrow for both |
| **Which layers matter** | Remove one layer at a time (addresses, rules, clearances, scan) | Change in success rate and in rule violations |
| **Value of changes** | Apply each candidate change and re-run | Gain in readiness per change |

## 9. Plan (12 weeks)

| Weeks | Work |
|---|---|
| 1–2 | Literature review (how indoor delivery robots are deployed today, BIM-based navigation, 3D scene graphs, TopologicPy agents); confirm the data; first supervisor meeting |
| 3–4 | Extraction pipeline: Revit → TopologicPy graph organised by level, plus scan enrichment |
| 5–6 | Brain layers (addresses, rules, clearances) and agent profiles; a thin end-to-end version of the tool |
| 7–8 | Delivery and resident simulation; readiness measures |
| 9–10 | Experiments: reality, agent capability, congestion, layer removal, changes |
| 11–12 | Writing; polish the tool for the final demo |

## 10. Risks

| Risk | Mitigation |
|---|---|
| The available data is not a multi-storey residential building | Confirm in week 1. If needed, adjust the setting (for example, an office or mixed-use building) and keep the stages of the delivery journey |
| Lifts are hard to simulate | Treat a lift as a connection with a waiting time and a capacity; do not model lift control systems |
| Agent behaviour grows into its own project | Keep agents simple (plan on the graph and follow the rules). The research is the brain and the readiness assessment |
| Point cloud not aligned with the model | Align key routes only: entrance, lobby, lift lobbies, corridors, a sample of units |
| The assumption that indoor deployment is the barrier proves wrong | Check it early in the literature and industry sources; reframe around the gaps actually found |

## 11. Expected contribution

- A **building brain for the last 50 metres**: a topological model derived from BIM and checked against a scan, covering vertical movement, addresses, access rules and real clearances.
- Evidence of **how much the real condition matters** compared with the model alone for delivery inside buildings.
- A **delivery-readiness assessment** that identifies the changes that make a building robot-ready.
- An extension of TopologicPy's agent simulation from hypothetical offices to a real multi-storey residential building with agents of different capabilities.

## 12. References (to verify during the literature review)

Papers are stored in [`_papers_/`](_papers_/README.md).

- Jabi, W., Xue, Y., Woolley, T. E. & Kaouri, K. (2025). 3D Topological Modeling and Multi-Agent Movement Simulation for Viral Infection Risk Analysis. *Architectural Science Review.* arXiv:2408.16417.
- Jabi, W. & Chatzivasileiadi, A. (2021). *Topologic: Exploring Spatial Reasoning Through Geometry, Topology, and Semantics.* Formal Methods in Architecture, Springer.
- Smith, P. (2026). Buildings (Still) Equal Data. *nimble* (Substack), 15 January 2026. Industry viewpoint.
- Afyouni, I., Ray, C. & Claramunt, C. (2012). Spatial models for context-aware indoor navigation systems: A survey. *Journal of Spatial Information Science* 4, 85–123.
- Boguslawski, P., Mahdjoubi, L., Zverovich, V. & Fadli, F. (2016). Automated construction of variable density navigable networks in a 3D indoor environment for emergency response. *Automation in Construction* 72, 115–128.
- Xu, M., Wei, S., Zlatanova, S. & Zhang, R. (2017). BIM-based indoor path planning considering obstacles. *ISPRS Annals* IV-2/W4.
- Díaz-Vilariño, L., Boguslawski, P., Khoshelham, K., Lorenzo, H. & Mahdjoubi, L. (2016). Indoor navigation from point clouds: 3D modelling and obstacle detection. *ISPRS Archives* XLI-B4.
- Armeni, I. et al. (2019). 3D Scene Graph: A Structure for Unified Semantics, 3D Space, and Camera. *ICCV.*
- Rosinol, A. et al. (2020). 3D Dynamic Scene Graphs: Actionable Spatial Perception with Places, Objects, and Humans. *RSS.*
- Hughes, N., Chang, Y. & Carlone, L. (2022). Hydra: A Real-time Spatial Perception System for 3D Scene Graph Construction and Optimization. *RSS.*
- Gu, Q. et al. (2024). ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning. *ICRA.*

---

## Version history

Before each change, the current version is copied to `_archive_/` as `<name> (vN, date).md`.

| Version | Date | Change |
|---|---|---|
| v1 | 2026-10-04 | First draft: general "building brain" for autonomous agents |
| v2 | 2026-10-04 | Focused on a specific problem: the **last 50 metres** of delivery in multi-storey and multi-level residential buildings. Restructured on the model of Jabi et al. (2025): agents are the means, delivery readiness is the outcome. Added: the stages of the delivery journey, address matching, lifts, resident agents for congestion, ranking of changes, Smith (2026) as industry motivation, and the papers on BIM and point-cloud navigation |
