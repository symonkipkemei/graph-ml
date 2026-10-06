# Supervisor Context — Prof. Wassim Jabi

> Who my supervisor is, what he works on, and how the thesis can align with his research.
> **Last updated:** 2026-10-04 · Sources are listed at the bottom. Check details against his LinkedIn and Cardiff profile.

---

## 1. Profile

- **Role:** Professor and Chair of Computational Methods in Architecture, Welsh School of Architecture, **Cardiff University**.
- **Research interests:** parametric design, the representation of space, building performance simulation, and robotic fabrication in architecture.
- **Known for:** creating **Topologic / TopologicPy**, an open-source library that combines geometry, topology and semantics for architectural modelling. All my prior work in `_graphs3_/` uses it.
- **Robotics:** he secured a grant for a 6-axis industrial robot and works on **robotic fabrication** (nonplanar printing of earth-based materials). He does **not** work on mobile robots or robot navigation.

## 2. Research threads relevant to the thesis

| Thread | Key work | What it means for me |
|---|---|---|
| **Topology for architectural representation** | *TopologicPy: A Syntopic Integration of Geometry, Topology, and Semantics in Architectural Design*; Jabi & Chatzivasileiadi (2021), *Topologic: Exploring Spatial Reasoning Through Geometry, Topology, and Semantics* | The core method reference. The thesis should use TopologicPy as its main toolkit |
| **Graph machine learning** | Alymani, Jabi & Corcoran (2023), *Graph ML classification using architectural 3D topological models*; Alymani, Jabi & Alammar (2025), *Graph ML for heating and cooling loads* (Buildings 15(18)) | GNNs on TopologicPy graphs. The building–ground relationship dataset in assign-03 came from this line of work |
| **Graph datasets** | Massafra, Al-Harasis, Stefanini & Jabi (2025), *Semi-Automated Dataset Generation for Residential Buildings Using Graph-Based Topological Modelling* (Buildings 15(8)) | How to build graph datasets from buildings |
| **Agents moving through buildings** | Jabi, Xue, Woolley & Kaouri (2025), *3D Topological Modeling and Multi-Agent Movement Simulation for Viral Infection Risk Analysis* (Architectural Science Review; arXiv 2408.16417) | TopologicPy navigation graphs plus agents following schedules. **The closest bridge to Option 2 (robots)**: agents can stand in for robots |
| **Shape and graph grammars** | Dounas & Jabi (eCAADe 2025), *Towards Bridging Shape and Graph Grammars Through Topology* | A formal language for **changing** buildings. **The closest bridge to Option 1 (renovation edits)** |
| **Reading how buildings are organised** | Al-Harasis & Jabi (2025), *Graph-Based Analysis of Best Practices in Autism Centre Design* | Graph metrics used to judge design quality. Supports Option 1's baseline analysis |
| **Performance and ML** | Alyahya, Lannon & Jabi (2025), *Optimising biomimetic ventilated façades with CFD and ML* (Buildings 15(22)) | Less relevant |

## 3. How the two options fit his work

| | Option 1: Renovation (architects) | Option 2: Building brains (simulated agents) |
|---|---|---|
| Fit with his research | **Strong.** Graph analysis of design quality, plus graph grammars to describe changes | **Strong.** Builds directly on his multi-agent movement simulation in TopologicPy |
| What he can guide well | Topology, graph metrics, grammars, TopologicPy internals | Navigation graphs, agent simulation, TopologicPy internals |
| Risk | Low | Low. It is framed as simulation, so no robotics hardware expertise is needed |

**Takeaway:** frame the thesis around **TopologicPy** and topology. Option 2 is framed as *agents in topological models* (simulation): solve the brain, not the body.

## 4. Questions for the first meeting

1. Which option does he see as the stronger contribution in 3 months?
2. Does the thesis need a **graph ML** component, or is topological and graph analysis enough?
3. **Option 1:** could his graph-grammar work (with Dounas) describe renovation edits formally?
4. **Option 2:** can TopologicPy's agent and navigation-graph tools from the infection-risk paper be reused for robot-like agents?
5. Does TopologicPy support bringing in **point clouds** or comparing a model against a scan, or is that outside its scope?
6. What output does he expect: a tool, a dataset, a paper-style evaluation, or a combination?
7. How often will we meet, and what are the milestones within the 3 months?

## 5. Meeting log

| Date | Discussed | Outcome / actions |
|---|---|---|
| | | |

---

## Sources

- [Cardiff University profile](https://profiles.cardiff.ac.uk/staff/jabiw)
- [ORCA: Cardiff publications](https://orca.cardiff.ac.uk/view/cardiffauthors/A1121339.html)
- [ResearchGate profile](https://www.researchgate.net/profile/Wassim-Jabi)
- [3D Topological Modeling and Multi-Agent Movement Simulation (arXiv)](https://arxiv.org/abs/2408.16417) · [Architectural Science Review](https://www.tandfonline.com/doi/full/10.1080/00038628.2025.2603534)
- [Graph ML classification using 3D topological models (2023)](https://doi.org/10.1177/00375497221105894)
- [Graph ML for heating and cooling loads (2025)](https://doi.org/10.3390/buildings15183256)
- [Semi-Automated Dataset Generation for Residential Buildings (2025)](https://www.researchgate.net/publication/390830822_Semi-Automated_Dataset_Generation_for_Residential_Buildings_Using_Graph-Based_Topological_Modelling)
- [TopologicPy: A Syntopic Integration of Geometry, Topology, and Semantics](https://www.researchgate.net/publication/396681527_TopologicPy_A_Syntopic_Integration_of_Geometry_Topology_and_Semantics_in_Architectural_Design)
- [LinkedIn post on TopologicPy](https://nl.linkedin.com/posts/wassim_topologicpy-activity-7155137105872977920-zChl)
