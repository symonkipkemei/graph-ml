# Thesis Context — Building Graphs for AEC

> Working context for the thesis research. Keep this file current: it is the starting point for every research session.
> **Status:** Two proposals drafted; Proposal 2 (v3) is the most developed · **Time available:** 3 months · **Last updated:** 2026-10-04

---

## 0. Where we are now (2026-10-04)

| | Proposal 1: Reading the existing (renovation) | Proposal 2: Building brains (last 50 m delivery) |
|---|---|---|
| Version | v1 | **v3** |
| Maturity | Method and evaluation drafted; motivation not yet backed by evidence | **Motivation backed by evidence** (Urban Freight Lab, NMHC, Korean robot-ready certification); gap table; anticipated questions answered |
| Problem | Architects can't see how a renovation changes a building's organisation | Delivery is solved up to the entrance; inside the building, readiness is **assessed by hand, building by building** |
| Contribution | Before/after graph comparison with explained impacts | **Automated delivery-readiness assessment** from the building's own data (BIM + scan), before any robot arrives |
| Papers collected | None yet | 8 PDFs plus sources in [`research-2/_papers_/`](research-2/_papers_/README.md) |
| Blocking question | Is there a real renovation brief? | **Is the scanned building multi-storey residential?** |

**Momentum is with Proposal 2.** It has a specific, evidenced problem and the strongest link to the supervisor's work. The choice is **not final**: it depends on the data question and the first meeting with Prof. Jabi.

### Next steps

1. **Confirm the data:** what building the model and scan cover, the scan format, and whether the scan is aligned with the model. This decides Proposal 2's setting.
2. **Read the key related work:** Jung et al. (2023), the Springer (2026) paper on robot-adaptive standards, and the Urban Freight Lab report. Download the first two by hand.
3. **First supervisor meeting:** present both proposals using the questions in [supervisor-context.md](supervisor-context.md).
4. **Start the shared foundation** (Revit → TopologicPy graph + scan), which is useful whichever option is chosen.

## 1. What I want to achieve

Write a thesis showing how **representing buildings as graphs** can solve a real, practical problem in **Architecture, Engineering and Construction (AEC)**.

The thesis should:

- **Solve a real AEC problem.** The value should be clear to practitioners, not only to a graph-theory audience.
- **Use real project data.** Work on a real building: a point cloud and a verified Revit model.
- **Make a measurable contribution.** End with evidence (metrics, case studies, comparisons) that the graph approach works.
- **Deliver a working tool.** The thesis must end with a tool that validates the research (see section 6).
- **Fit in 3 months.** Every choice of scope has to pass this test.

## 2. The core idea

Drawings and BIM models capture **geometry**. The **relational logic** of a building lives in its graph: which space connects to which, through what, and how robustly. Once a building is a graph, we can **analyse** it (centrality, paths, articulation points), **learn** from it (GNNs, link prediction) and **compare** it (before and after, model vs reality).

## 3. Assets

### Data

| Asset | What it is | What it gives the thesis |
|---|---|---|
| **Verified as-built Revit model** | Semantic model, checked against reality | A clean source for the building graph (rooms, doors, levels) and the ground truth |
| **Point cloud** | Scan of the same building | Physical reality: obstructions, clear widths, furniture, real conditions |

Having **both for the same building** is rare and valuable. The verified model can act as **ground truth** for anything derived from the scan, and the scan can **enrich or check** the graph from the model.

To confirm: how many buildings, the scan format (E57/RCP), whether the scan is registered to the model, and whether the scan includes furniture and clutter.

### Prior work ([`_graphs3_/`](../_graphs3_/))

| Work | What it showed | Relevance |
|---|---|---|
| assign-01: graph types | Primal, dual, circulation and fenestration graphs with TopologicPy | Graph extraction pipeline |
| assign-02: analysis | Shortest path, centrality, exit paths | Baseline metrics |
| assign-03: graph classification | GraphSAGE on building graphs | Graph-level ML |
| assign-04: node classification | Room function from topology alone | Semantic inference |
| assign-05: co-housing | Graph metrics and isovists on real buildings | Reading how a building is organised |

**Professional edge:** Revit API / APS Design Automation in C#, for reliable extraction from Revit.

### Supervisor: Prof. Wassim Jabi (Cardiff University)

Creator of **TopologicPy**. Both options fit his research: **Option 1** through graph analysis of design quality and graph grammars for changes, and **Option 2** through his work on agents moving through topological models (his robotics work is fabrication, which is why Option 2 is framed as simulation). See [supervisor-context.md](supervisor-context.md) for details and questions for the first meeting.

## 4. The two options

### Option 1: Reading the existing, graph-based impact analysis for renovation design

> **Research question:** Can a building graph help renovation architects read how an existing building is organised, and understand what happens to that organisation when they change it?

- **Primary users:** **renovation architects**, the broader market. They work from a verified as-built model at feasibility and early design stages.
- **Secondary users (extension):** **facility managers**, a narrower niche. They need the same comparison applied to many small changes over a building's life.
- **Idea:** the verified as-built graph is the **baseline**. Each renovation proposal produces a **proposal graph**, and comparing the two shows the impact: lost connections, new bottlenecks or single points of failure, longer egress routes, rooms becoming more or less central.
- **Proposals as the change:** Revit **phases** (existing / new / demolished) and design options are Revit's own renovation tools. The "change" is the architect's proposal, so **no change history is needed**.
- **The point cloud's role:** makes the baseline match the existing condition (real clear widths, obstructions), not only the model's idealised geometry.
- **Full proposal:** [research-1/Proposal - Reading the Existing.md](research-1/Proposal%20-%20Reading%20the%20Existing.md)

### Option 2: Building brains, assessing residential buildings' readiness for the last 50 metres of delivery

> **Research question:** Can a residential building's own data (a verified BIM model plus a point cloud) be turned into a topological brain that **assesses how ready the building is** for autonomous delivery over the last 50 metres, from the entrance to a room inside an apartment?

- **Argument:** delivery is largely solved up to the building entrance. Inside a 12-storey block, or a three-level apartment, it is not: the lobby, the lift, the corridor, finding "Apt 7B", internal stairs.
- **Why it matters (evidence):**
  - Interiors are the slowest part of delivery: 12.2 of 20 minutes in the Urban Freight Lab's Seattle study went on lifts and door-to-door delivery.
  - Parcel volumes are overwhelming apartment buildings: about 150 packages a week per community, about 270 in the holidays (NMHC).
  - Lockers store parcels but don't deliver them, which pushes the last 50 metres onto residents.
- **The gap:** robots already deliver inside buildings (Korea's robot-friendly certification, with 28 items for apartment complexes; lift standards; Woowa and Naver), but readiness is **assessed and prepared by hand for each building**. Nothing assesses it from the building's own data before robots arrive.
- **Framing:** solve **the brain, not the body**. Simulated agents in TopologicPy are the **means**; **delivery readiness** is the outcome, as infection risk is in Jabi et al. (2025).
- **The brain:** a graph organised by level (building → level → unit → room), with lifts and stairs, links from addresses to places, access rules, and real clearances from the scan.
- **Agents:** delivery agents with different abilities (wheeled vs stair-climbing), plus residents following daily schedules who create congestion.
- **Outputs:** a readiness map by unit and level, failures and their causes, and a ranked list of changes to the building, compared with existing certification criteria.
- **Key assumption:** the available data is a **multi-storey residential building** (to confirm).
- **Full proposal:** [research-2/Proposal - Building Brains.md](research-2/Proposal%20-%20Building%20Brains.md) (v3)

### Shared foundation

Both options start from the same thing: a **building graph from the verified Revit model, enriched with the point cloud**. Building this first (weeks 1–4) moves the project forward whichever option is chosen.

### Assessment against 3 months

| | Option 1: Renovation (architects) | Option 2: Last 50 m delivery (agents) |
|---|---|---|
| Fit with prior work | **High.** Same pipeline plus a before/after comparison | **High.** Circulation and egress graphs plus agents |
| Fit with supervisor | Strong (graph analysis of design quality, graph grammars for changes) | **Strong** (multi-agent movement in TopologicPy) |
| Existing research | Thin on graph-based before/after comparison for renovation | Readiness criteria exist (Korea) but are assessed by hand; robotics scene graphs are built after deployment. **The gap is automated, data-based readiness assessment** |
| How to validate | Seeded renovation scenarios, plus sessions with architects | Simulated deliveries: model-only vs model + scan, agent abilities, congestion, value of changes, comparison with certification criteria |
| Data needed | One verified model plus one scan, plus renovation proposals (a real brief, or written scenarios) | One verified model plus one scan, which I already have |
| Biggest risk | The chat layer grows in scope; access to architects | The data may not be a multi-storey residential building; agent behaviour grows into its own project |
| **3-month feasibility** | **Good.** The proposals are the change, so no history is needed | **Good.** No hardware, and the data is already in hand |

## 5. Current leaning: Proposal 2, not final

Both options remain **feasible in 3 months**, and both fit the supervisor's work. **Proposal 2 is now the stronger candidate:**

- It has a **specific, evidenced problem** (the last 50 metres) and a **clear gap**: readiness is assessed by hand today, with no data-based method.
- Its structure mirrors the supervisor's own paper: agents as the means, a measurable outcome, a decision-support tool.
- It has a clean core experiment (model-only vs model + scan brain), and its "changes" output links back to Proposal 1 (renovating for robot readiness).

**What would change this:** the data turns out not to be a multi-storey residential building, or the supervisor prefers Proposal 1. Proposal 1 would also need its motivation backed by evidence (it is still at v1) to compete on equal terms.

Whichever option is chosen:

- **Chat:** an interface for *asking about* the building or a change. Generating full Revit geometry from chat is out of scope.
- **Link between the options:** a renovation baseline graph can serve as an agent's brain, and the reverse. The option not chosen becomes future work or a discussion chapter.

## 6. The validation tool (required)

The thesis must end with a **working tool that validates the research**. The tool is not an extra on top of the thesis. It is **how the method is tested**: the evaluation is run through it, on the real building.

### What the tool must do

- **Put the research method into practice** from start to finish on the real data (Revit model and point cloud).
- **Produce evidence**: the outputs that are measured or judged in the evaluation chapter.
- **Be usable by the target user**, so that it can be tested with them (renovation architects for Option 1; building owners, facility managers and delivery operators for Option 2).

### What the tool would be for each option

| | Option 1: Renovation (architects) | Option 2: Last 50 m delivery (agents) |
|---|---|---|
| Input | Verified Revit model + point cloud, and a renovation proposal (Revit phases or design option, or a "what if" from chat) | Verified Revit model + point cloud, agent profiles, resident schedules, and delivery tasks ("deliver to Apt 7B, kitchen") |
| Core | Baseline graph → proposal graph → **graph comparison** with explained impacts | Building brain organised by level (lifts, addresses, rules, clearances), plus delivery and resident agents |
| Output | A view or report: what changed, what it affects (egress, bottlenecks, accessibility), linked to Revit elements | Delivery routes with success or failure and its cause, a delivery-readiness map by unit and level, and a ranked list of changes to the building |
| Validation | Seeded scenarios with known impacts (precision and recall), model-only vs model + scan, architects' feedback | Model-only vs model + scan; agent abilities; congestion; layer removal; value of each change |

### Scope and time

- **Time split:** roughly half the 3 months goes to research and method, and half to building the tool and evaluating with it. Start the tool early, as a thin end-to-end version, rather than in the last month.
- **Form still open:** a Revit add-in (closest to the user's workflow; I already work with the Revit API) or a standalone app or notebook pipeline (faster to build). Decide early.
- **Keep it thin:** only build what the evaluation needs. Polish, extra UI and extra features are future work.

## 7. Open questions

- [ ] **Option 1 or 2.** Confirm the choice (leaning towards Option 2, see section 5).
- [ ] Does the thesis have to make a **graph ML** contribution, or is graph analysis enough?
- [ ] How many buildings? Scan format, registration, level of detail?
- [ ] **Option 1:** is there a **real renovation brief** for this building, or will scenarios be written?
- [ ] **Option 1:** can I run short sessions with 3–5 **renovation architects**?
- [ ] **Option 2:** is the scanned and verified building a **multi-storey residential** building, ideally with multi-level units?
- [ ] **Option 2:** confirm through the literature and industry sources how indoor delivery robots are deployed today (mapping run for each building? lift integration?)
- [x] **Option 2:** download and read **Jung et al. (2023)** and **Park & Park (2026)**. Done. Findings:
  - Both are expert-derived checklists or standards, with no simulation or BIM.
  - The certification covers dwelling units only through bonus items.
  - Park & Park publish numerical door, lift and passageway standards and **call for robot-navigation simulation** as future work.
  - Notes are in [`research-2/_papers_/README.md`](research-2/_papers_/README.md). These findings are not yet in the proposal (planned for v4).
- [ ] **Option 2:** find **apartment-specific** evidence on the time spent inside buildings (the UFL figure is from an office tower)
- [ ] Discuss the option choice with Prof. Jabi. Ask about reusing his agent simulation work for Option 2, and graph grammars for describing changes in Option 1.
- [ ] Industry partner? Who will validate the results (for example, renovation architects for Option 1)?
- [ ] What **form** does the validation tool take: Revit add-in, standalone app, or a pipeline with a simple interface? What does the programme or supervisor require?

## 8. Constraints and principles

- **3 months.** One contribution, done well. Everything else is plumbing or future work.
- **Feasibility first.** Confirm data before committing.
- **Measurable evaluation.** Every claim needs a metric or a case study behind it.
- **The tool serves the evaluation.** Build only what is needed to validate the research.

## 9. Workspace layout

**Archive convention (applies to every change):**

1. **Before** any change to a proposal, copy the current version into the `_archive_/` folder beside it as `<name> (vN, YYYY-MM-DD).md`.
2. Edit the live proposal, raise its **Version** field, and add a row to its **Version history** table.
3. Record notable changes in the decision log below.
4. Drafts that are fully replaced are moved to `_archive_/` and marked "(superseded)". Nothing is deleted.

Together, the archive, the version tables and the decision log show how the research developed.

```
_graphs4_/
  thesis-context.md     ← this file: goals, status, decisions
  supervisor-context.md ← supervisor profile, alignment, meeting log
  research-1/           ← Option 1 proposal: renovation (archived QAQC draft in _archive_/)
  research-2/           ← Option 2 proposal: last 50 m delivery (v3); _archive_/ holds v1–v2; _papers_/ holds the reference PDFs and source index
  ...               ← literature reviews, experiments, decisions to come
```

## 10. Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-10-04 | Thesis research lives in `_graphs4_/` | Keeps it separate from coursework in `_graphs3_/` |
| 2026-10-04 | QAQC framing (research-1) set aside in favour of renovation / robot options | User's interest moved to renovation architects and robots |
| 2026-10-04 | Time available fixed at 3 months | User constraint |
| 2026-10-04 | Supervisor: Prof. Wassim Jabi (Cardiff) | Creator of TopologicPy; the topic should use TopologicPy |
| 2026-10-04 | A working tool is a required outcome and validates the research | Thesis requirement |
| 2026-10-04 | Option 1 reframed around facility managers and building change over time | User: FMs benefit from continuously understanding how a building changes; their problems give the context |
| 2026-10-04 | Option 2 reframed as agents in topological models (simulation), not robotics hardware | Solve the brain, not the body; matches the supervisor's multi-agent work; no physical robot needed |
| 2026-10-04 | Option 1 primary user: renovation architects; facility managers become secondary | Architects are a broader market; FMs are a tighter niche. Proposals act as the change, so no change history is needed |
| 2026-10-04 | Proposals written: research-1 (renovation), research-2 (building brains); QAQC draft archived | Ready to share with the supervisor |
| 2026-10-04 | Proposal 2 v2: building brains focused on the **last 50 metres of delivery** in residential buildings | Strategic critique: v1 described a capability, not a problem. Following Jabi et al. (2025), agents became the means and delivery readiness the outcome. Motivated by the user's "delivery is solved up to the doorstep" argument and Smith (2026) |
| 2026-10-04 | Proposal 2 v3: added evidence for the motivation and repositioned the contribution as an **automated delivery-readiness assessment** | Answers "why deliveries inside apartments?": UFL final 50 feet, NMHC package volumes, lockers push the last 50 m onto residents, and Korea's robot-ready certification shows readiness is assessed by hand today |
| 2026-10-04 | Current leaning: Proposal 2, not final | Most developed and best evidenced; mirrors the supervisor's paper. Depends on data confirmation and the supervisor meeting |
