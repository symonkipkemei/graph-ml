# Papers — Research 2: Building Brains

Reference papers for [Proposal - Building Brains](../Proposal%20-%20Building%20Brains.md). Status: **Read** (read in full), **Skimmed**, or **To read**.

## Supervisor's work (the foundation)

| File | Paper | Why it matters | Status |
|---|---|---|---|
| `Jabi2025_3D-Topological-Modeling-Multi-Agent-Movement.pdf` | Jabi, Xue, Woolley & Kaouri (2025). *3D Topological Modeling and Multi-Agent Movement Simulation for Viral Infection Risk Analysis.* Architectural Science Review. arXiv:2408.16417 | **The base Proposal 2 builds on.** Navigation graph from a floor face with obstacles cut out as holes (plus an offset buffer). A faster version for large plans: hand-placed key points, Delaunay triangulation, then removing edges that cross walls or obstacles. Agents with schedules moving along Dijkstra shortest paths. **Gaps:** hypothetical layouts, modelled furniture, all agents identical, no access rules, no real-world validation | Read |

## Indoor navigation models (BIM, point clouds)

| File | Paper | Why it matters | Status |
|---|---|---|---|
| `Afyouni2012_Spatial-Models-Indoor-Navigation-Survey.pdf` | Afyouni, Ray & Claramunt (2012). *Spatial models for context-aware indoor navigation systems: A survey.* JOSIS 4, 85–123 | Survey of indoor spatial models (geometric, symbolic, hybrid). Cited by Jabi; a basis for the brain's layers | To read |
| `Xu2017_BIM-Indoor-Path-Planning-Obstacles.pdf` | Xu, Wei, Zlatanova & Zhang (2017). *BIM-based indoor path planning considering obstacles.* ISPRS Annals IV-2/W4 | **Close prior work:** path planning from BIM with obstacles. The baseline to compare against | To read |
| `DiazVilarino2016_Indoor-Navigation-From-Point-Clouds.pdf` | Díaz-Vilariño, Boguslawski, Khoshelham, Lorenzo & Mahdjoubi (2016). *Indoor navigation from point clouds: 3D modelling and obstacle detection.* ISPRS Archives XLI-B4 | **Close prior work:** obstacles detected from point clouds for navigation, the role the scan plays in Proposal 2 | To read |
| *(not downloaded, see below)* | Boguslawski, Mahdjoubi, Zverovich & Fadli (2016). *Automated construction of variable density navigable networks in a 3D indoor environment for emergency response.* Automation in Construction 72, 115–128 | Cited by Jabi. Navigable networks built from non-manifold models, the same family as TopologicPy | To download |

## 3D scene graphs (robotics)

| File | Paper | Why it matters | Status |
|---|---|---|---|
| `Armeni2019_3D-Scene-Graph.pdf` | Armeni et al. (2019). *3D Scene Graph: A Structure for Unified Semantics, 3D Space, and Camera.* ICCV. arXiv:1910.02527 | The original layered building → room → object graph. Note co-author Martin Fischer (Stanford, AEC) | To read |
| `Rosinol2020_3D-Dynamic-Scene-Graphs.pdf` | Rosinol et al. (2020). *3D Dynamic Scene Graphs: Actionable Spatial Perception with Places, Objects, and Humans.* RSS. arXiv:2002.06289 | Adds a "places" layer for navigation; scene graphs agents can act on | To read |
| `Hughes2022_Hydra.pdf` | Hughes, Chang & Carlone (2022). *Hydra: A Real-time Spatial Perception System for 3D Scene Graph Construction and Optimization.* RSS. arXiv:2201.13360 | Builds the hierarchy (places → rooms → building) in real time. Robots build it from sensors, whereas Proposal 2 builds it from BIM | To read |
| `Gu2024_ConceptGraphs.pdf` | Gu et al. (2024). *ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning.* ICRA. arXiv:2309.16650 | Scene graphs combined with language models for planning tasks; relevant to the optional chat layer | To read |

## Industry viewpoints (web, not peer-reviewed)

| Source | Why it matters | Status |
|---|---|---|
| Smith, P. (2026). [*Buildings (Still) Equal Data*](https://nimblebim.substack.com/p/buildings-still-equal-data). nimble (Substack), 15 Jan 2026 | Argues that BIMs are "the sensory data of tomorrow's machines". Industry motivation for Proposal 2 v2. The author works in scan-to-BIM automation, so he has a commercial interest: cite as viewpoint, not evidence. His angle is BIM as *training data*; ours is BIM as the *working map* for one specific building | Read |

## Motivation and robot readiness (added for Proposal 2 v3)

| Source | Why it matters | Status |
|---|---|---|
| `Jung2023_Robot-Friendly-Certification-Apartment-Complexes.pdf`: Jung, Jang, Gu, Yoon & Kim (2023). *Development of Certification Model of Robot-Friendly Environment for Apartment Complexes.* Journal of Cadastre & Land InformatiX 53(1), 83–105. [doi:10.22640/lxsiri.2023.53.1.83](https://doi.org/10.22640/lxsiri.2023.53.1.83). Mostly in Korean, with an English abstract and tables | **Key related work: the readiness checklist for apartments.** See the [detailed notes below](#jung-et-al-2023-robot-friendly-certification-for-apartment-complexes) | Read |
| `Park2026_Human-Centered-Robot-Adaptive-Design-Standards.pdf`: Park, Y. & Park, S. (2026). *Development of Human-Centered, Robot-Adaptive Building Design Standards: Focusing on Korea's Building Certification Systems.* Architectural Research 28:14. [doi:10.1007/s44515-026-00016-y](https://doi.org/10.1007/s44515-026-00016-y). Open access (CC BY-NC-ND) | **Key related work: numerical design standards for circulation.** It explicitly calls for **robot-navigation simulation** to verify its standards. See the [detailed notes below](#park--park-2026-human-centered-robot-adaptive-design-standards) | Read |
| Urban Freight Lab (2018). [*The Final 50 Feet of the Urban Goods Delivery System*, final report](https://www.urbanfreightlab.com/wp-content/uploads/2023/10/Final_50-Feet-of-Urban-Goods-Delivery_full_report.pdf) | 12.2 of 20 minutes inside the Seattle Municipal Tower went on lifts and door-to-door delivery. The academic anchor for the "final 50 feet" framing (office building) | To read |
| NMHC / Kingsley (2018). [*Package Delivery Survey*](https://www.nmhc.org/research-insight/research-report/nmhc-package-delivery-report) | About 150 packages a week (about 270 in the holidays) per apartment community; package rooms often too small | To read |
| News: [Elevator World: Korea lift standards for delivery robots](https://elevatorworld.com/news/daily-news/south-korea-sets-standards-for-delivery-robot-elevator-use/) · [The Spoon: Woowa robots ride lifts](https://thespoon.tech/woowa-delivery-robots-to-access-buildings-and-ride-elevators-next-year/) · [Freethink: Naver 1784](https://www.freethink.com/robots-ai/1784-naver-labs) | Robots already deliver inside buildings, but each building is set up individually | Skimmed |
| Indicative stats: [GoBolt](https://www.gobolt.com/blog/last-mile-delivery-problems/) · [Luxer One](https://www.luxerone.com/last-mile-delivery-challenges-for-property-managers/) · [Multifamily Executive](https://www.multifamilyexecutive.com/property-management/apartment-trends/multifamily-properties-face-flood-of-packages_o) | Failed deliveries about 5% (8–20% at peak), about $17 each. Vendor sources: **indicative only** | Skimmed |

## Detailed notes: key related work

### Jung et al. (2023): robot-friendly certification for apartment complexes

**What it is.** It extends Korea's **Certification of Robot-Friendly Environment (CORE)**, run by the Smart City Association since 2022 and originally for offices only (Lee et al., 2022), to **apartment complexes**.

**How it was built.** Focus groups with **21 experts** (5 sessions, July–October 2022) and an AHP survey of **8 experts**. The criteria come from expert opinion, **not empirical data**. The authors state this as a limitation and call for pilot projects.

**Structure.**
- **28 items**: 17 shared with the office scheme plus 11 specific to apartments. **15 are mandatory** (12 shared, 3 apartment-specific); the rest are bonus items.
- **Category weights:** architecture and facility design 0.55 (97 points), networks and systems 0.24 (45), building operations management 0.15 (20), robot support and other services 0.05 (14). Total: **176 points**.
- **Grades** (all mandatory items must be met): best ≥ 95% (143 points), excellent ≥ 90% (135), general ≥ 85% (128).
- **Highest-weighted items:** wireless coverage (18), **indoor clear width (17)**, **building entrance/exit (16)**, **lift support for robots (10)**, **lift (9)**, slope (9), entrance/access (9), floor finish (7).

**Standard robot.** A **wheeled** robot, because it is the least capable kind: if a wheeled robot can move through a space, legged and tracked robots usually can too. Indoor shared spaces assume a robot **1,350 mm high, 550 mm wide and 600 mm long**; outdoors, 1,550 × 900 × 1,500 mm. These sizes come from a survey of about 40 manufacturers.

**Spatial scope.** Outdoors, indoor shared spaces, and indoor private spaces. Delivery is listed as an indoor shared-space service. **Private dwelling units are excluded from the standard-robot definition**: smart-home and IoT systems are replacing those services, and robot sizes vary too much. Delivery to individual units appears only as **bonus items**: "robot delivery support facility" (2 points) and "call service for individual house" (1 point). Underground driving is not covered.

**Disclosure.** The corresponding author led the CORE certification project.

**What it means for Proposal 2:**
1. **The gap is confirmed.** The criteria come from experts, it is a checklist scored item by item, and there is **no simulation, BIM or data-based assessment**.
2. **Agent profiles can be grounded.** Use the 550 × 600 mm wheeled robot as the baseline profile, rather than inventing dimensions.
3. **Delivery inside the unit is uncovered.** It is excluded or only a bonus item, so stage 5 of Proposal 2 (inside multi-level units) goes **beyond** the existing certification.
4. **Element checks vs network checks.** Each item (width, entrance, lift) is checked **separately**. A graph can show **network effects** that a checklist cannot, such as one non-compliant door on the only route making a whole wing unreachable.

### Park & Park (2026): human-centered, robot-adaptive design standards

**What it is.** It compares Korea's **Robotics-Enabled Environment Certification (REEC)** with the mandatory **Barrier-Free (BF)** certification. It then proposes **combined numerical standards** for circulation spaces (entrances, lifts, passageways) at three levels: minimum, recommended and optimal. The authors are from Heerim Architects, with funding from the Korean Ministry of Land (KAIA).

**The certification landscape.**

| Scheme | Type | Items | Notes |
|---|---|---|---|
| Korea REEC (Smart City Association) | Private, voluntary, no legal force | **102** | Weights: architecture and facilities 40%, network 30%, operations 20%, robot support 10%. Key issues: network dead zones, **robot–lift interface failures** |
| Singapore BCA *Design for Maintainability Guide* | Public guidance, recommendations only | 22 | Not a certification; no numerical criteria |
| Japan RFA Manual (Robot Friendly Asset Promotion Association) | Private grading | 15 | Based on Japanese Industrial Standards; grades A/B/C |
| Korea BF (Barrier-Free) | **Mandatory** for public and larger private buildings | — | Dimensions, slopes, level differences, handrails, braille signage |

All three robot schemes focus on **circulation**. None is legally enforceable, and **none systematically covers conflicts when people and robots share the same space**.

**Proposed standards** (minimum / recommended / optimal). These are directly checkable against BIM plus a scan:

| Element | Criterion | Min | Rec | Opt |
|---|---|---|---|---|
| Doors | Clear opening width | 0.9 m | 1.0 m | 1.2 m (busy areas) |
| | Access route width | 1.2 m | 1.5 m | 1.8 m |
| | Clear floor space in front of and behind the door | 1.2 m | 1.5 m | 1.8 m |
| | Threshold height | ≤ 20 mm | 0 mm | 0 mm |
| | Ramp slope | ≤ 1/12 | ≤ 1/18 | ≤ 1/24 |
| | Automatic doors linked to robots (API) | ≥ 1 per zone | ≥ 80% | 100% |
| Lifts | Door clear width | 0.8 m | 1.0 m | 1.2 m |
| | Clear floor space in front of the lift | 1.4 × 1.4 m | 1.5 × 1.5 m | same |
| | Car interior (W × D) | 1.6 × 1.35 m | 1.6 × 1.4 m | same |
| | Gap between landing and car | ≤ 30 mm | same | same |
| | Lift lobby clear width | ≥ 1.2 m | same | same |
| | Lifts robots can operate (API) | ≥ 1 | ≥ 50% | 100% |
| Passageways | Effective width | 1.2 m | 1.5 m | 1.8 m |
| | Width at crossing and waiting zones | 2.0 m | 2.2 m | 2.4 m |
| | Slope | ≤ 1/12 | ≤ 1/18 | ≤ 1/24 |
| | Floor friction / grout joints / reflectivity | ≥ 0.4 / ≤ 10 mm / low | ≥ 0.75 / ≤ 5 mm / non-reflective | same |

**Robot failures it cites** (SBS News): a Korean city-hall service robot destroyed after falling down a staircase (2024), and a US sidewalk delivery robot that crashed through a glass panel its sensors missed (2026).

**Stated limitation and future work:** the standards were "derived from a comparative analysis of existing certification criteria… rather than from field experiments", and "will be… refined through follow-up research combining **robot-navigation simulations** and field experiments in operating buildings".

**What it means for Proposal 2:**
1. **A direct invitation.** The authors themselves name robot-navigation simulation as the next step. Proposal 2 does exactly this, on a real building.
2. **Readiness levels from published standards.** Graph edges (doors, passageways, lifts) can be tagged as below minimum, minimum, recommended or optimal using these numbers. The readiness levels then come from a published standard rather than being invented.
3. **Conflicts between people and robots are an open gap.** Existing schemes don't cover them. Proposal 2's resident agents and records of meetings in narrow passages address it directly.
4. **The scan matters for exactly these criteria.** Clear widths, threshold heights and clutter in corridors are what drift from the design model.

## To download manually

- **Urban Freight Lab final report (2018).** The direct PDF link is above.
- **Boguslawski et al. (2016).** The open copy is at [CORE](https://files.core.ac.uk/download/pdf/323894336.pdf), but CORE blocks automated downloads. Download it in a browser and save it here as `Boguslawski2016_Variable-Density-Navigable-Networks.pdf`.

## Sources

- [arXiv 2408.16417 (Jabi et al.)](https://arxiv.org/abs/2408.16417)
- [JOSIS (Afyouni et al.)](https://josis.org/index.php/josis/article/view/26)
- [ISPRS Annals 2017 (Xu et al.)](https://isprs-annals.copernicus.org/articles/IV-2-W4/417/2017/isprs-annals-IV-2-W4-417-2017.pdf)
- [ISPRS Archives 2016 (Díaz-Vilariño et al.)](https://isprs-archives.copernicus.org/articles/XLI-B4/275/2016/isprs-archives-XLI-B4-275-2016.pdf)
- [CORE (Boguslawski et al.)](https://files.core.ac.uk/download/pdf/323894336.pdf)
- [Jung et al. 2023 (doi)](https://doi.org/10.22640/lxsiri.2023.53.1.83) · [KoreaScience](https://koreascience.or.kr/article/JAKO202321351785716.page)
- [Park & Park 2026 (doi)](https://doi.org/10.1007/s44515-026-00016-y)
- arXiv: [1910.02527](https://arxiv.org/abs/1910.02527) · [2002.06289](https://arxiv.org/abs/2002.06289) · [2201.13360](https://arxiv.org/abs/2201.13360) · [2309.16650](https://arxiv.org/abs/2309.16650)
