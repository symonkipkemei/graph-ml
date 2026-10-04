# Research Proposal 2 — Building Brains: Assessing Residential Buildings' Readiness for the Last 50 Metres of Delivery

| | |
|---|---|
| **Author** | Symon Kipkemei |
| **Supervisor** | Prof. Wassim Jabi, Cardiff University |
| **Topic** | Building graphs for AEC: buildings for autonomous agents |
| **Duration** | 3 months |
| **Status** | Draft |
| **Version** | v3, 2026-10-04 |

---

## 1. Summary

Delivery is largely solved **up to the building entrance**. Inside the building it is not. From the entrance, someone must get through a lobby, ride the right lift, follow a corridor, find "Apt 7B", and possibly climb an internal stair inside a three-level apartment to reach the kitchen. This part is slow even for human couriers, it overwhelms apartment buildings as parcel volumes grow, and parcel lockers simply hand it over to the residents.

Robots can already do this, but **each building has to be checked and prepared by hand**. South Korea has created a robot-friendly building certification with 28 evaluation items for apartment complexes, and robot delivery to apartment doors has been piloted, but only in buildings that were set up for it individually. **There is no method for assessing a building's readiness from its own data before any robot arrives.**

This thesis builds that method. It decodes a residential building's **verified BIM model, checked against a point cloud**, into a **topological "building brain"**, and tests it with **simulated delivery agents in TopologicPy**. It solves for **the brain, not the body**. The outcome is a **delivery-readiness assessment**: which units and rooms each kind of agent can reach, how long deliveries take, where and why they fail, and which changes to the building would help most. The method extends Jabi et al. (2025) from infection risk in hypothetical offices to delivery readiness in a real residential building.

## 2. Motivation: why deliveries inside apartment buildings matter

### 2.1 What doesn't work today

| Evidence | What it shows | Source quality |
|---|---|---|
| In the Seattle Municipal Tower, **12.2 of the 20 minutes** a driver spent in the building went on moving between floors in freight lifts and going door to door. Removing those steps could more than halve delivery time (Urban Freight Lab, "Final 50 Feet") | The building interior is the slowest part of the delivery, even for humans | Academic (University of Washington). *Note: an office tower, not apartments* |
| Average apartment communities receive about **150 packages a week**, rising to about **270 a week in the holidays (+81%)**; 61% of managers report year-on-year growth. Renters receiving 6–10 packages a month rose from 15% to 25% (NMHC surveys) | Parcel volumes are growing and overwhelming apartment buildings | Industry association surveys |
| 77% of apartment buildings have a package room, but managers report they are often too small at peak times (NMHC) | Storage-based solutions run out of space | Industry association surveys |
| About **5% of last-mile deliveries fail** (8–20% at peak), costing about **$17 each**. Common causes are absent recipients, address problems and no access to the building | Getting into and through the building is part of the failure | Vendor blogs: **indicative only** |

### 2.2 Why lockers and package rooms are not enough

Lockers and package rooms **store** parcels; they do not **deliver** them. The last 50 metres moves to the resident, who must go down to the lobby and back. That is hardest for older and disabled residents, and for heavy or bulky goods (groceries, medicines, household supplies). Package rooms also overflow at peak times.

### 2.3 Robots are already here, but buildings are prepared by hand

- **Korea's robot-friendly building certification (2022)** was first aimed at offices. Jung et al. (2023) extended it to **apartment complexes**, with **28 evaluation items** in four categories (architecture and facility design; networks and systems; building operations management; support for robot activity), worth up to 176 points across three certification levels.
- Recent work compares Korea's **Robotics-Enabled Environment Certification** with its **Barrier-Free certification**, and proposes combined design standards for **circulation spaces** shared by robots and people.
- Korea is preparing **national standards for delivery robots using lifts**.
- **Woowa Brothers** piloted robots that ride lifts and deliver to apartment doors in a large apartment complex, made possible by linking the robots to **that building's** management system. **Naver** built a robot-only lift system ("Roboport") in its 1784 headquarters.

**The pattern:** the need is real and readiness criteria exist, but readiness is **assessed and prepared building by building, by hand**. Nothing yet assesses a building automatically from data it already has.

### 2.4 Industry viewpoint

Smith (2026) argues that "the BIMs that we produce today are the sensory data of tomorrow's machines". He sees BIM as **training data** for robots in general. This thesis uses one building's BIM, checked against a scan, as the **working map and assessment model** for that building.

## 3. Problem

### 3.1 The last 50 metres, stage by stage

| Stage | What the agent must work out | What the building brain must provide |
|---|---|---|
| 1. Entrance → lobby | Which entrance to use; where access is controlled | Entrances, door types, access points |
| 2. Address → place | Which part of the building *is* "Apt 7B" | A link from each unit number and room name to its node in the graph |
| 3. Vertical movement | Which lift serves the target level; lift or stairs; how long the wait is | A graph organised by level, with lifts and stairs as connections |
| 4. Corridor → unit door | The route, and what is physically in the way | Real clearances and obstacles from the scan |
| 5. Inside the unit | In a multi-level apartment: can this agent reach the room, or must it hand over at the entry level? | Agent abilities matched against the graph; hand-over zones |
| 6. Rules | Which spaces are public, shared or private; where it may wait | Access levels; waiting and hand-over zones |

### 3.2 The gap

| Existing work | What it does | What is missing |
|---|---|---|
| Jabi et al. (2025) | TopologicPy navigation graphs and agents with schedules, for infection risk | Hypothetical single-floor offices; identical human agents; modelled furniture; **no real-world validation** (their stated limitation) |
| Korean robot-friendly certification (Jung et al., 2023; REEC/BF comparison) | Criteria for whether a building is ready for robots | Assessed **by hand**; not linked to building data or simulation *(to confirm when the papers are read in full)* |
| Indoor delivery robots in practice (e.g. Woowa) | Lift-riding delivery to apartment doors | Set up **for each building**: mapping and system integration *(to verify)* |
| BIM-based and point-cloud navigation (Xu et al., 2017; Díaz-Vilariño et al., 2016) | Path planning with obstacles | Paths for one agent, not building-wide **readiness** across units, agent types and busy periods |
| 3D scene graphs (Armeni 2019; Hughes 2022; Gu 2024) | Layered building graphs built by robots from their sensors | Built **after** the robot arrives, rather than from design data **before** deployment |

## 4. Research questions

**Main question:** Can a residential building's own data (a verified BIM model plus a point cloud) be turned into a topological brain that **assesses how ready the building is** for autonomous delivery over the last 50 metres, from the entrance to a room inside an apartment?

1. **Representation:** what must the brain contain to support the last 50 metres? Candidates: a graph organised by level, lifts and stairs, links from addresses to places, access levels, real clearances.
2. **Reality:** how much does checking the brain against the point cloud change which units and rooms are reachable and which deliveries succeed, compared with a brain built from the model alone?
3. **Agent capability:** how does readiness differ between kinds of agent (wheeled vs stair-climbing), especially inside multi-level units?
4. **Readiness and changes:** can the simulation identify the **smallest set of changes** to the building that most improves readiness, and how do its findings relate to existing readiness criteria such as Korea's certification items?

## 5. Users

- **Primary:** owners and facility managers of residential buildings deciding whether and how to support autonomous delivery, and delivery or robotics operators assessing a building before deploying.
- **Secondary:** architects designing new residential buildings, or renovating existing ones, to be "robot-ready". This links to Proposal 1.
- **Wider:** standards and certification bodies. An automated, data-based assessment could support certification schemes like Korea's.

## 6. Data

| Data | Role |
|---|---|
| Verified as-built Revit model | Source of the brain: levels, lifts, stairs, units, rooms, room uses, doors, entrances |
| Point cloud of the same building | Physical reality: obstacles, real clear widths, blocked routes. Also the **ground truth** for whether a route is physically passable |
| *(Optional)* MSD apartment dataset / Jabi's generated residential datasets | Test whether the method works across many apartment layouts, in graph form only |

> **Key assumption to confirm:** this proposal needs the data to cover a **multi-storey residential building**, ideally with multi-level units. If not, adjust the setting (for example, office or mixed-use) and keep the stages of the delivery journey.

## 7. Method

1. **Extract the building.** Export levels, units, rooms, doors, stairs, lifts and entrances from Revit (C# Revit API) into a TopologicPy CellComplex, reusing the pipeline from `_graphs3_/assign-01` and `assign-02`.
2. **Build the brain** as a graph organised in levels: building → level → unit → room. Its layers:
   - **Topology:** places (rooms, corridors, lobbies) and connections (doors, stairs, lifts). A lift is a connection between levels with a waiting time and a capacity.
   - **Addresses:** each unit number and room name is linked to its graph node, so "Apt 7B, kitchen" resolves to a target.
   - **Clearances:** distances and clear widths from the model, corrected with the scan.
   - **Rules:** access levels (public, shared, private) and permitted waiting and hand-over zones.
   - **Reality:** obstacles and narrowed or blocked passages measured from the point cloud.
3. **Agent profiles.** Each agent type has a radius, can or cannot climb stairs, can or cannot open doors, and has access rights. Following Jabi et al. (2025), the navigation surface is **offset by each agent's radius**, so each agent type gets its own navigation graph.
4. **Simulation.** Delivery agents receive tasks ("deliver to Apt 7B, kitchen"), plan with shortest-path search, and move through the TopologicPy model. **Resident agents with daily schedules**, following Jabi et al.'s method, create realistic congestion in lifts and corridors. Meetings between delivery agents and residents are recorded using the same distance calculations between agents.
5. **Readiness assessment.** Combine the results into a **readiness profile** for each unit, level and building. Where possible, link the findings to existing criteria (for example, Korea's certification items on circulation and lifts).
6. **Changes.** Test candidate changes (widen a door, add a door opener, clear a corridor, give lift access, add a hand-over zone) and rank them by the readiness gained.
7. **Optional chat layer.** Delivery tasks given in natural language are turned into queries on the brain.

## 8. Validation tool

The validation tool is a **delivery-readiness simulator** for residential buildings.

- **Input:** the verified Revit model, the point cloud, agent profiles, resident schedules and delivery tasks.
- **Output:**
  - the building brain (a graph organised by level)
  - simulated delivery routes, with success or failure and the cause of each failure
  - a **readiness map** by unit and level
  - a **ranked list of changes** to the building

## 9. Evaluation

| What is tested | How | Metric |
|---|---|---|
| **Effect of reality** | The same deliveries on a model-only brain and on a model + scan brain | Share of planned routes that are physically passable (checked against the scan); failures the model-only brain does not foresee |
| **Agent capability** | Deliveries to every unit and room by each agent type | Share of units and rooms reachable; where hand-overs are needed |
| **Congestion** | Busy and quiet times of day, using resident schedules | Delivery time; lift waiting time; meetings in passages too narrow for both |
| **Which layers matter** | Remove one layer at a time (addresses, rules, clearances, scan) | Change in success rate and in rule violations |
| **Value of changes** | Apply each candidate change and re-run | Readiness gained per change |
| **Comparison with existing criteria** | Compare simulated findings with relevant certification items, where they can be obtained | Agreement and differences, and what the simulation adds beyond a checklist |

## 10. Anticipated questions

| Question | Answer |
|---|---|
| Why do we need deliveries inside apartments at all? | Interiors are the slowest part of delivery (12 of 20 minutes in the UFL study), parcel volumes are rising (NMHC), and storage solutions push the last 50 metres onto residents, especially older and disabled ones |
| Why not just use lockers? | Lockers store parcels but don't deliver them, and package rooms overflow at peak times |
| Isn't this science fiction? | No. Korea certifies buildings for robots and is writing lift standards, and robot delivery to apartment doors has been piloted |
| What is new here? | Readiness is currently assessed and prepared by hand for each building. This thesis assesses it from the building's own data before any robot arrives, and ranks the changes that would help |
| Why does the point cloud matter? | Robots fail on the real condition (clutter, real door widths), not on the design model |
| Why simulation and not a real robot? | The research question is about the building, not robot hardware. Simulation allows testing every unit, agent type and time of day, as Jabi et al. (2025) did for infection risk |

## 11. Plan (12 weeks)

| Weeks | Work |
|---|---|
| 1–2 | Literature review: Korean certification papers, Urban Freight Lab, indoor delivery deployments, BIM-based navigation, scene graphs. Confirm the data; first supervisor meeting |
| 3–4 | Extraction pipeline: Revit → TopologicPy graph organised by level, plus scan enrichment |
| 5–6 | Brain layers (addresses, rules, clearances) and agent profiles; a thin end-to-end version of the tool |
| 7–8 | Delivery and resident simulation; readiness measures; link to certification criteria |
| 9–10 | Experiments: reality, agent capability, congestion, layer removal, changes, comparison with criteria |
| 11–12 | Writing; polish the tool for the final demo |

## 12. Risks

| Risk | Mitigation |
|---|---|
| The available data is not a multi-storey residential building | Confirm in week 1. If needed, adjust the setting and keep the stages of the delivery journey |
| The Korean certification criteria are not available in full or in English | Use the published category structure and the circulation-related criteria that are accessible; treat comparison with the criteria as secondary |
| Lifts are hard to simulate | Treat a lift as a connection with a waiting time and a capacity; do not model lift control systems |
| Agent behaviour grows into its own project | Keep agents simple (plan on the graph and follow the rules). The research is the brain and the readiness assessment |
| Point cloud not aligned with the model | Align key routes only: entrance, lobby, lift lobbies, corridors, a sample of units |
| The motivating statistics are weak or not about apartments | Rely on the academic (UFL) and industry-association (NMHC) sources; label vendor figures as indicative; look for apartment-specific data |

## 13. Expected contribution

- A **building brain for the last 50 metres**: a topological model from BIM, checked against a scan, covering vertical movement, addresses, access rules and real clearances.
- An **automated delivery-readiness assessment** that works from the building's own data before deployment, and ranks the changes that make a building robot-ready.
- Evidence of **how much the real condition matters** compared with the model alone for delivery inside buildings.
- An extension of TopologicPy's agent simulation from hypothetical offices to a real multi-storey residential building with agents of different capabilities.

## 14. References (to verify during the literature review)

Papers are stored in [`_papers_/`](_papers_/README.md).

**Supervisor and method**
- Jabi, W., Xue, Y., Woolley, T. E. & Kaouri, K. (2025). 3D Topological Modeling and Multi-Agent Movement Simulation for Viral Infection Risk Analysis. *Architectural Science Review.* arXiv:2408.16417.
- Jabi, W. & Chatzivasileiadi, A. (2021). *Topologic: Exploring Spatial Reasoning Through Geometry, Topology, and Semantics.* Formal Methods in Architecture, Springer.

**Motivation and readiness**
- Urban Freight Lab (2018). *The Final 50 Feet of the Urban Goods Delivery System.* Final report, University of Washington.
- NMHC / Kingsley (2018). *Package Delivery Survey.* National Multifamily Housing Council.
- Jung, M., Jang, S., Gu, H., Yoon, D. & Kim, K. (2023). Development of Certification Model of Robot-Friendly Environment for Apartment Complexes. *Journal of Cadastre & Land Information* 53(1), 83–105. doi:10.22640/lxsiri.2023.53.1.83.
- *(Authors to confirm)* (2026). Development of Human-Centered, Robot-Adaptive Building Design Standards: Focusing on Korea's Building Certification Systems. Springer. doi:10.1007/s44515-026-00016-y.
- Smith, P. (2026). Buildings (Still) Equal Data. *nimble* (Substack), 15 January 2026. Industry viewpoint.

**Indoor navigation**
- Afyouni, I., Ray, C. & Claramunt, C. (2012). Spatial models for context-aware indoor navigation systems: A survey. *Journal of Spatial Information Science* 4, 85–123.
- Boguslawski, P., Mahdjoubi, L., Zverovich, V. & Fadli, F. (2016). Automated construction of variable density navigable networks in a 3D indoor environment for emergency response. *Automation in Construction* 72, 115–128.
- Xu, M., Wei, S., Zlatanova, S. & Zhang, R. (2017). BIM-based indoor path planning considering obstacles. *ISPRS Annals* IV-2/W4.
- Díaz-Vilariño, L., Boguslawski, P., Khoshelham, K., Lorenzo, H. & Mahdjoubi, L. (2016). Indoor navigation from point clouds: 3D modelling and obstacle detection. *ISPRS Archives* XLI-B4.

**3D scene graphs**
- Armeni, I. et al. (2019). 3D Scene Graph: A Structure for Unified Semantics, 3D Space, and Camera. *ICCV.*
- Rosinol, A. et al. (2020). 3D Dynamic Scene Graphs: Actionable Spatial Perception with Places, Objects, and Humans. *RSS.*
- Hughes, N., Chang, Y. & Carlone, L. (2022). Hydra: A Real-time Spatial Perception System for 3D Scene Graph Construction and Optimization. *RSS.*
- Gu, Q. et al. (2024). ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning. *ICRA.*

**Industry and news sources (not peer-reviewed)**
- Elevator World: South Korea sets standards for delivery-robot lift use.
- The Spoon: Woowa delivery robots to access buildings and ride elevators.
- Freethink: Naver 1784, a robot-friendly building.
- Multifamily Executive; GoBolt; Luxer One: parcel volumes and failed deliveries (indicative).

---

## Version history

Before each change, the current version is copied to `_archive_/` as `<name> (vN, date).md`.

| Version | Date | Change |
|---|---|---|
| v1 | 2026-10-04 | First draft: general "building brain" for autonomous agents |
| v2 | 2026-10-04 | Focused on a specific problem: the **last 50 metres** of delivery in multi-storey and multi-level residential buildings. Restructured on the model of Jabi et al. (2025): agents as the means, delivery readiness as the outcome |
| v3 | 2026-10-04 | Added **Motivation** (§2) with evidence: Urban Freight Lab, NMHC, failed-delivery figures, why lockers are not enough, Korea's robot-friendly certification and lift standards, Woowa and Naver. Repositioned the contribution as an **automated readiness assessment** from the building's own data, compared with readiness that is assessed by hand. Added the gap table (§3.2), RQ4 link to certification criteria, standards bodies as wider users, comparison with criteria in the evaluation, Anticipated questions (§10), and new risks and references |
