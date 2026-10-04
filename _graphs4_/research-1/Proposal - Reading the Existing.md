# Research Proposal 1 — Reading the Existing: Graph-Based Impact Analysis for Renovation Design

| | |
|---|---|
| **Author** | Symon Kipkemei |
| **Supervisor** | Prof. Wassim Jabi, Cardiff University |
| **Topic** | Building graphs for AEC: renovation and existing buildings |
| **Duration** | 3 months |
| **Status** | Draft |
| **Version** | v1, 2026-10-04 |

---

## 1. Summary

Renovation architects start from an existing building, not a blank site. Every proposal changes how that building is organised: which spaces connect, how people move, where the bottlenecks and single points of failure are. These effects are hard to see in drawings or in a BIM model, because a model captures **geometry**, while organisation lives in **relationships**.

This thesis turns a verified as-built Revit model, enriched with a point cloud of the same building, into a **baseline building graph** using TopologicPy. Each renovation proposal produces a **proposal graph**. Comparing the two graphs reveals and explains what the proposal does to the building's organisation. The research is validated through a working tool that runs this comparison on a real building.

## 2. Problem

- **Existing buildings are hard to read.** Architects understand a building's spatial logic through experience and repeated study of drawings. That understanding is implicit and is not recorded anywhere.
- **The impact of changes is invisible until late.** Removing a door, merging rooms or changing a room's use can lengthen egress routes, create bottlenecks or isolate parts of the building. These effects are often found only at compliance review, or never.
- **BIM shows what the building is meant to be, not what it is.** Furniture, obstructions and narrowed clear widths exist on site but not in the model. Decisions about the existing condition should be based on the building as it physically is.

## 3. Research questions

**Main question:** Can a building graph help renovation architects read how an existing building is organised, and understand what happens to that organisation when they change it?

1. **Baseline:** which graph representations and metrics best capture the organisation of an existing building (connectivity, depth, centrality, egress, accessibility)?
2. **Change:** how can the difference between a baseline graph and a proposal graph be computed and explained in terms architects recognise ("this door was the only route from the east wing to an exit")?
3. **Reality:** how much does adding point-cloud data (real clear widths and obstructions) change the baseline and the impacts found, compared with a graph built from the model alone?

## 4. Users

- **Primary:** renovation architects, at feasibility and early design stages, working from an existing verified model.
- **Secondary (extension):** facility managers who track many small changes over a building's life. These are the same comparison method, applied as a series of snapshots over time.

## 5. Data

| Data | Role |
|---|---|
| Verified as-built Revit model | The source of the baseline graph: rooms, doors, openings, levels, stairs. Revit element IDs stay the same across versions, which makes matching between graphs reliable |
| Point cloud of the same building | Records the existing condition: real clear widths, obstructions, blocked doors. Assumed to be aligned with the model (to confirm) |
| Renovation proposals | Revit **phases** (existing / new / demolished) or design options. These are Revit's own renovation tools, so proposals come in a format architects already use. Use a real brief if one is available; otherwise write realistic scenarios |

## 6. Method

1. **Extract the building.** Export spaces, doors and openings from Revit (C# Revit API), then build a TopologicPy CellComplex and the dual and circulation graphs. This reuses the pipeline from `_graphs3_/assign-01`.
2. **Enrich with the scan.** For each door and room, crop the point cloud and measure clear width, obstructions and usable floor area. Store these as edge and node attributes.
3. **Profile the organisation.** Compute metrics per room, per connection and for the whole building:
   - integration and depth (space syntax)
   - betweenness centrality
   - articulation points and bridges (single points of failure)
   - distance to the nearest exit
   - step-free accessibility
   - which uses sit next to which
4. **Model the change.** Build the proposal graph from the proposal phase. Describe the difference as **graph edit operations** (add or remove a door, merge or split a room, change a room's use), following Prof. Jabi's work on graph grammars.
5. **Compare and explain.** Match rooms and doors between the two graphs by element ID, compute the change in every metric, and turn significant changes into plain-language findings ranked by severity (for example, "new single point of failure for egress", "the reception becomes less central").
6. **Optional chat layer.** Let the architect ask questions about the findings, or describe a "what if" change that is converted into graph edits. Generating full Revit geometry from chat is out of scope.

## 7. Validation tool

The validation tool is a working **Revit-to-graph impact analyser**. Its form (Revit add-in, or Revit exporter plus a Python app) is to be decided with the supervisor.

- **Input:** the verified model, the point cloud and a renovation proposal.
- **Output:** a baseline profile, a proposal profile and a ranked list of impacts, each explained and linked back to the Revit elements involved.

## 8. Evaluation

| What is tested | How | Metric |
|---|---|---|
| **Correctness** | Seed scenarios with known expected impacts (for example, remove a door that is an articulation point) | Precision and recall of the impacts found |
| **Effect of the scan** | Run each scenario with a model-only baseline and with a model + scan baseline | Number and type of findings that differ |
| **Usefulness** | Short sessions with 3–5 renovation architects on real scenarios | Task-based feedback: did they find the impacts relevant and understandable? |

## 9. Plan (12 weeks)

| Weeks | Work |
|---|---|
| 1–2 | Literature review; confirm the data (scan format, alignment); first supervisor meeting |
| 3–4 | Extraction pipeline: Revit → TopologicPy graph, plus scan enrichment |
| 5–6 | Organisation metrics; a thin end-to-end version of the tool |
| 7–8 | Proposal graph, comparison and findings; build the scenarios |
| 9–10 | Evaluation: correctness, scan comparison, architect sessions |
| 11–12 | Writing; polish the tool for the final demo |

## 10. Risks

| Risk | Mitigation |
|---|---|
| Point cloud not aligned with the model | Align on a few key rooms only; enrich doors and corridors rather than the whole building |
| No real renovation brief | Write scenarios from common renovation types (office to residential, opening up floor plans, adding accessibility) |
| Chat layer grows in scope | Keep it optional; the main contribution is the comparison |
| Architects not available | Use seeded scenarios as the main evaluation; keep the sessions small |

## 11. Expected contribution

- A method for **comparing a building's organisation before and after a change**, with explained findings, aimed at renovation.
- Evidence of how much **scan-based existing conditions** change the analysis compared with model-only graphs.
- A working tool showing the method on a real building.

## 12. References (to verify during the literature review)

- Jabi, W. & Chatzivasileiadi, A. (2021). *Topologic: Exploring Spatial Reasoning Through Geometry, Topology, and Semantics.*
- Jabi, W. *TopologicPy: A Syntopic Integration of Geometry, Topology, and Semantics in Architectural Design.*
- Dounas, T. & Jabi, W. (2025). *Towards Bridging Shape and Graph Grammars Through Topology.* eCAADe 2025.
- Al-Harasis & Jabi, W. (2025). *Graph-Based Analysis of Best Practices in Autism Centre Design.*
- Hillier, B. & Hanson, J. (1984). *The Social Logic of Space.* Cambridge University Press.
- Volk, R., Stengel, J. & Schultmann, F. (2014). Building Information Modeling (BIM) for existing buildings: Literature review and future needs. *Automation in Construction.*
- Tang, P. et al. (2010). Automatic reconstruction of as-built building information models from laser-scanned point clouds: A review of related techniques. *Automation in Construction.*
- Rasmussen, M. H. et al. (2021). BOT: The Building Topology Ontology of the W3C Linked Building Data Group. *Semantic Web.*

---

## Version history

Before each change, the current version is copied to `_archive_/` as `<name> (vN, date).md`.

| Version | Date | Change |
|---|---|---|
| v1 | 2026-10-04 | First draft |
