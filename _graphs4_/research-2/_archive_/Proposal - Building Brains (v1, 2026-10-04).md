# Research Proposal 2 — Building Brains: Decoding Buildings into Topological Models for Autonomous Agents

| | |
|---|---|
| **Author** | Symon Kipkemei |
| **Supervisor** | Prof. Wassim Jabi, Cardiff University |
| **Topic** | Building graphs for AEC: buildings for autonomous agents |
| **Duration** | 3 months |
| **Status** | Draft |
| **Version** | v1, 2026-10-04 |

---

## 1. Summary

More organisations want autonomous agents (delivery, logistics and service robots) to work inside buildings day after day, in industrial and residential settings. To be useful, an agent must **judge space**: which rooms it can enter, which route it can physically fit through, where it should not go, and where it can wait. This knowledge already exists in the building's design data, but robots do not read it.

This thesis solves **the brain, not the body**. It decodes a building into a **"building brain"**: a layered TopologicPy graph derived from a verified Revit model and checked against a point cloud of the same building. The brain is tested with **simulated agents moving through the topological model**, extending Prof. Jabi's multi-agent movement work. No physical robot is used.

## 2. Problem

- **Robots usually learn buildings from scratch.** They map with their own sensors, and that map does not know what spaces are *for* or what the rules of use are.
- **BIM already contains a building's meaning** (rooms, uses, doors, levels, exits), but it is not in a form an agent can reason over.
- **BIM is idealised.** Real buildings have furniture, clutter, narrowed passages and blocked doors. A brain built only from the model will send agents down routes that do not physically work.

## 3. Research questions

**Main question:** Can we decode a building into a graph-based brain that lets autonomous agents judge and use space?

1. **Representation:** what layers must a building brain contain (topology, metric clearances, semantics and rules of use, real-world obstacles) for agents to do useful tasks?
2. **Reality:** how much does checking the brain against a point cloud improve task success, compared with a brain built from the model alone?
3. **Judgement:** can rules of use (for example, avoid private rooms, or wait only in a defined zone) be expressed in the graph so that agents behave appropriately, not just reach their goal?

## 4. Users

- **Primary:** organisations automating workflows inside buildings, such as delivery, logistics and service tasks.
- **Indirect:** facility managers and building owners who must make their buildings ready for robots.

## 5. Data

| Data | Role |
|---|---|
| Verified as-built Revit model | The source of the brain's topology and meaning: rooms, uses, doors, levels, stairs, lifts |
| Point cloud of the same building | The physical truth: obstacles, real clear widths, blocked routes. Also used as the **ground truth** for whether a route is physically passable |

Both datasets already exist, so this option needs no new data collection.

## 6. Method

1. **Extract the building.** Export from Revit (C# Revit API), then build a TopologicPy CellComplex and a navigation graph, reusing the pipeline from `_graphs3_/assign-01` and `assign-02`.
2. **Build the brain in layers:**
   - **Topological:** places (rooms, corridors) and connections (doors, stairs, lifts), organised in levels: building → floor → zone → room.
   - **Metric:** distances and clear widths from the model, corrected with the scan.
   - **Semantic:** room use, access level (public, staff, private) and rules of use.
   - **Real-world:** obstacles and blocked or narrowed passages, measured from the point cloud.
3. **Agent profiles.** Each agent type has a width, can or cannot use stairs or lifts, can or cannot open doors, and has its own access rights. The brain **filters itself** for each profile into a graph that agent can actually use.
4. **Simulation.** Simulated agents receive tasks (deliver from A to B, visit a set of rooms). They plan on the brain and move through the TopologicPy model, following the multi-agent approach of Jabi et al. (2025).
5. **Optional chat layer.** Tasks can be given in natural language ("take this to the meeting room on level 2") and turned into queries on the brain.

## 7. Validation tool

The validation tool is a working **building-brain simulator**.

- **Input:** the verified Revit model, the point cloud, agent profiles and a set of tasks.
- **Output:** the brain (a layered graph), simulated agent routes, task success or failure with the reasons, and a comparison between brain versions.

## 8. Evaluation

| What is tested | How | Metric |
|---|---|---|
| **Effect of reality** | The same tasks on a model-only brain and on a model + scan brain | Share of planned routes that are physically passable (checked against the scan), task success rate, replans needed |
| **Which layers matter** | Remove one layer at a time (no semantics, no metric data, no scan) | Change in success and in rule violations |
| **Judgement** | Tasks involving restricted spaces and waiting zones | Rule violations per task |
| **Agent variety** | Several agent profiles (narrow vs wide, stairs vs lift only) | Share of the building each profile can reach; failed tasks |

## 9. Plan (12 weeks)

| Weeks | Work |
|---|---|
| 1–2 | Literature review (3D scene graphs, BIM for robots, TopologicPy agents); confirm the data; first supervisor meeting |
| 3–4 | Extraction pipeline: Revit → TopologicPy graph, plus scan enrichment |
| 5–6 | Brain layers and agent profiles; a thin end-to-end version of the tool |
| 7–8 | Agent simulation and task set; rules of use |
| 9–10 | Experiments: reality, layer removal, judgement, agent variety |
| 11–12 | Writing; polish the tool for the final demo |

## 10. Risks

| Risk | Mitigation |
|---|---|
| Agent behaviour grows into its own project | Keep agents simple (planning on the graph and following rules); the research is the brain |
| Point cloud not aligned with the model | Align key routes and doors only |
| Checking passability against the scan is hard | Use a simple measure: clear width along the route compared with the agent's width |
| Crowded robotics literature | Position the work as **BIM + scan → brain for building operations**, rather than robot mapping |

## 11. Expected contribution

- A **layered building-brain model** derived from BIM and checked against a scan, which agents can use for tasks.
- Evidence of **how much real-world data matters** for agents working in buildings.
- A working simulator showing the method on a real building, extending TopologicPy's agent capabilities.

## 12. References (to verify during the literature review)

- Jabi, W., Xue, Y., Woolley, T. E. & Kaouri, K. (2025). 3D Topological Modeling and Multi-Agent Movement Simulation for Viral Infection Risk Analysis. *Architectural Science Review.* arXiv:2408.16417.
- Jabi, W. & Chatzivasileiadi, A. (2021). *Topologic: Exploring Spatial Reasoning Through Geometry, Topology, and Semantics.*
- Armeni, I. et al. (2019). 3D Scene Graph: A Structure for Unified Semantics, 3D Space, and Camera. *ICCV.*
- Rosinol, A. et al. (2020). 3D Dynamic Scene Graphs: Actionable Spatial Perception with Places, Objects, and Humans. *RSS.*
- Hughes, N., Chang, Y. & Carlone, L. (2022). Hydra: A Real-time Spatial Perception System for 3D Scene Graph Construction and Optimization. *RSS.*
- Gu, Q. et al. (2024). ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning. *ICRA.*
- Tang, P. et al. (2010). Automatic reconstruction of as-built building information models from laser-scanned point clouds: A review of related techniques. *Automation in Construction.*

---

## Version history

Before each change, the current version is copied to `_archive_/` as `<name> (vN, date).md`.

| Version | Date | Change |
|---|---|---|
| v1 | 2026-10-04 | First draft |
