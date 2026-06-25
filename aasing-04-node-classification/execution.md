# Execution Proposal: Graph Learning Pipeline for Architectural Floor Plans

## What changed from `_outdated_`

| Old (FA notebooks) | New (NC notebooks) | Why |
|---|---|---|
| `FA_05` tried to train a GNN → NaN loss crash | `NC_03` runs **inference only** with pretrained model | Instructions-2 removed training; instructions-3 points to S06-15C |
| All edges used `door_type="door"` only | Three door types: `passage`, `door`, `entrance_door` | Node_Classification_Instructions.docx requires all three |
| Features hand-crafted as CSV rows | `EncodeMSDGraphFeatures()` from S06-15B derives features from CellComplex | Follows the prescribed workflow |
| Balconies (label=8) used as entry/hub nodes | Architecturally coherent room programme | Spatial sense required for the presentation |

---

## New Folder Structure

```
aasing-04-node-classification/
  msd_node_classifier.pt              ← copied locally (github-ready)
  notebooks/
    NC_01_rhino_to_cellcomplex.ipynb  ← manual prep + import from Rhino
    NC_02_graph_construction.ipynb    ← CellComplex → Graph → CSV export
    NC_03_spatial_analysis.ipynb      ← graph metrics + interpretation
    NC_04_node_classification.ipynb   ← inference with pretrained model
  our_graph/                          ← output from NC_02
    graphs.csv
    nodes.csv
    edges.csv
    floor_plan_meta.json
  outputs/                            ← outputs from NC_03 + NC_04
    spatial_analysis.json
    node_predictions.csv
```

---

## Step 1 — Rhino → TopologicPy CellComplex (manual + `NC_01_rhino_to_cellcomplex.ipynb`)

**Source:** `Node_Classification_Instructions.docx` — this is the prescribed import workflow.  
**Nature:** Partially manual (Rhino modelling + layer naming), partially scripted (Python import).

### 1a. Rhino modelling checklist

- [ ] Model each room as a **closed solid (polysurface)** — rooms must be water-tight
- [ ] Group rooms by layer name matching the `room_type` string exactly (see table below)
- [ ] Model each aperture (door/passage) as a **rectangular face** placed on the shared wall between two rooms — the face must intersect the shared wall surface
- [ ] Group apertures by layer name matching the `door_type` string exactly (see table below)
- [ ] Export rooms as `geometry/rooms.obj` and apertures as `geometry/apertures.obj` (File → Export Selected, OBJ format, Y-up)

**Valid `room_type` layer names (case-sensitive lowercase):**

| Layer name | Label | Zoning |
|---|---:|---|
| `bedroom` | 0 | private |
| `livingroom` | 1 | living |
| `kitchen` | 2 | living |
| `dining` | 3 | living |
| `corridor` | 4 | living |
| `stairs` | 5 | service |
| `storeroom` | 6 | service |
| `bathroom` | 7 | service |
| `balcony` | 8 | outdoor |

**Valid `door_type` layer names:**

| Layer name | Connectivity value | When to use |
|---|---:|---|
| `passage` | 0 | Open archway — no physical door |
| `door` | 1 | Standard room door |
| `entrance_door` | 2 | Front door of an apartment |

### 1b. Python import script (`NC_01_rhino_to_cellcomplex.ipynb`)

```python
from topologicpy.Topology import Topology
from topologicpy.CellComplex import CellComplex
from topologicpy.Cluster import Cluster
from topologicpy.Dictionary import Dictionary

# --- Import room geometry ---
rooms_raw = Topology.ByOBJPath(r"geometry/rooms.obj", transposeAxes=False)

# Build CellComplex from merged room solids
all_cells = []
for obj in rooms_raw:
    cells = Topology.Cells(obj)
    all_cells.extend(cells)
cc = Topology.SelfMerge(Cluster.ByTopologies(all_cells))
cc = Topology.RemoveCoplanarFaces(cc)

# --- Assign room_type via selector vertices (one per cell) ---
# Layer names from OBJ groups drive the room_type value.
# Map each cell to its layer group and assign dictionary.
selectors = []
for obj in rooms_raw:
    layer_name = ...  # parse from OBJ group name
    for cell in Topology.Cells(obj):
        d = Dictionary.ByKeyValue("room_type", layer_name)
        s = Topology.InternalVertex(cell)
        s = Topology.SetDictionary(s, d)
        selectors.append(s)

cc = Topology.TransferDictionariesBySelectors(cc, selectors, tranCells=True)

# --- Import apertures and assign door_type ---
apertures_raw = Topology.ByOBJPath(r"geometry/apertures.obj", transposeAxes=False)
aperture_faces = []
for obj in apertures_raw:
    layer_name = ...  # parse from OBJ group name — must be passage/door/entrance_door
    for face in (Topology.Faces(obj) or [obj]):
        d = Dictionary.ByKeyValue("door_type", layer_name)
        face = Topology.SetDictionary(face, d)
        aperture_faces.append(face)

# --- Add apertures to CellComplex ---
cc = Topology.AddApertures(cc, aperture_faces,
                           exclusive=False,
                           subTopologyType="Face",
                           tolerance=0.001)

# --- Verify ---
cells = Topology.Cells(cc)
print(f"Cells: {len(cells)}")
for c in cells[:3]:
    d = Topology.Dictionary(c)
    print(Dictionary.ValueAtKey(d, "room_type"))

apers = Topology.Apertures(cc)
print(f"Apertures: {len(apers)}")
for a in apers[:3]:
    d = Topology.Dictionary(a)
    print(Dictionary.ValueAtKey(d, "door_type"))
```

### 1c. Checklist before moving to Step 2

- [ ] `len(cells)` matches the intended room count (target: 34)
- [ ] Every cell has a `room_type` value — no `None` values
- [ ] Every aperture has a `door_type` value — no `None` values
- [ ] All `room_type` values are in the 9-item valid list
- [ ] All `door_type` values are in `passage`, `door`, `entrance_door`
- [ ] At least one aperture of each `door_type` exists (passage, door, entrance_door)

---

## Step 2 — `NC_02_graph_construction.ipynb`

**Goal:** Convert CellComplex to Graph, encode MSD features, export CSVs.

**Floor plan: 2-storey, 4 apartments (A,B = floor 1; C,D = floor 2)**

| Count | Room type | MSD label | Zoning |
|---|---|---|---|
| 8 | bedroom | 0 | private |
| 4 | livingroom | 1 | living |
| 4 | kitchen | 2 | living |
| 4 | corridor | 4 | living |
| 2 | stairs | 5 | service |
| 4 | storeroom | 6 | service |
| 4 | bathroom | 7 | service |
| 4 | balcony | 8 | outdoor |
| **34 total** | | | |

**Door type distribution:**
- `entrance_door` — staircase ↔ apartment corridor (building entry point)
- `door` — bedroom, bathroom, storeroom, kitchen, balcony to corridor
- `passage` — corridor ↔ livingroom (open plan connection)

**Workflow:**
```python
from topologicpy.Graph import Graph

# 1. Build graph from CellComplex with apertures as edges
graph = Graph.ByTopology(cc, direct=False, directApertures=True)

# 2. Verify dictionaries
from S06_15B import EncodeMSDGraphFeatures, CheckMSDGraphPreparation
summary = CheckMSDGraphPreparation(graph)   # must show 0 unsupported types

# 3. Encode MSD features
graph = EncodeMSDGraphFeatures(graph)

# 4. Export to CSV
Graph.ExportToCSV(graph, path=r"our_graph/", overwrite=True)

# 5. Post-process: add inference masks (all nodes are test-only)
import pandas as pd
nodes = pd.read_csv("our_graph/nodes.csv")
nodes["train_mask"] = False
nodes["val_mask"]   = False
nodes["test_mask"]  = True
nodes.to_csv("our_graph/nodes.csv", index=False)
```

**Verify exported schema matches reference `dataset_node_classification/nodes.csv`:**
```
graph_id, node_id, label,
feat_zoning_type_0, feat_zoning_type_1, feat_zoning_type_2, feat_zoning_type_3,
feat_connectivity_0, feat_connectivity_1, feat_connectivity_2,
train_mask, val_mask, test_mask
```

---

## Step 3 — `NC_03_spatial_analysis.ipynb`

**Goal:** Run four graph metrics on the floor plan, interpret spatially.

**Workflow:**
1. Reload graph: `Graph.ByCSVPath(path="our_graph/")`
2. Convert to NetworkX undirected graph via adjacency extraction
3. Compute:
   - `nx.degree_centrality(G)` — connectivity richness per room
   - `nx.closeness_centrality(G)` — reachability from each room
   - `nx.clustering(G)` — neighbourhood interconnectedness
   - `nx.all_pairs_shortest_path_length(G)` — travel depth between rooms
4. Visualise: bar plots coloured by room type; highlight stairs (label=5) and corridors (label=4)
5. Interpret along 5 axes: accessibility, circulation, apartment isolation, spatial hierarchy, evacuation depth
6. Export metrics to `outputs/spatial_analysis.json`

**Expected findings:**
- Stairs (label=5): highest closeness — inter-floor bridge
- Corridors (label=4): highest degree within apartments
- Low clustering at stairs (connects unlike rooms across units); high clustering inside apartments
- Bedrooms (label=0): deepest from exits — highest evacuation depth

---

## Step 4 — `NC_04_node_classification.ipynb`

**Goal:** Run the pretrained GraphSAGE model on our graph; analyse and explain predictions.

**Paths — model is now local to this assignment:**
```python
DATASET_PATH = Path(r"E:\softwares-4\graph-ml\aasing-04-node-classification\our_graph")
MODEL_PATH   = Path(r"E:\softwares-4\graph-ml\aasing-04-node-classification\msd_node_classifier.pt")
```

**Workflow (mirrors S06-15C exactly):**
1. Verify three CSVs exist (`graphs.csv`, `nodes.csv`, `edges.csv`)
2. Load: `PyG.ByCSVPath(path, level="node", task="classification", nodeLabelType="categorical")`
3. Load model: `pyg.LoadModel(str(MODEL_PATH))`
4. Predict all: `pyg.Predict(split="all", return_probs=True, attach_to_data=True)`
5. Export predictions → `outputs/node_predictions.csv` with `graph_id, node_id, y_true, y_pred, y_pred_prob`
6. Visualise: `Topology.Show()` with `true_color` and `pred_color` per node (pattern from S06-15C)  
   — `graphs[0]` since we have a single graph
7. Confusion matrix: `sklearn.metrics.ConfusionMatrixDisplay`
8. Error analysis: for each misclassified node, print `room_type`, `degree`, and neighbouring room types

**Analysis questions for presentation:**
- Which room types does the model confuse, and why (neighbourhood similarity)?
- Do errors cluster spatially (e.g., all upper-floor bedrooms)?
- Does a low-degree node (balcony/storeroom with one neighbour) predict correctly?
- Contrast with old approach: `FA_05` crashed on training; `NC_04` gets predictions immediately.

---

## Key Risks and Mitigations

| Risk | Mitigation |
|---|---|
| OBJ group names don't match `room_type`/`door_type` strings | Print layer names immediately after `ByOBJPath`; rename Rhino layers before export |
| `AddApertures` finds no matches (aperture face misses the shared wall) | Increase `tolerance` from 0.001 to 0.01; verify aperture geometry intersects the wall face in Rhino |
| `CheckMSDGraphPreparation` reports unsupported types | Fix typos in Rhino layer names (must be lowercase, no spaces) |
| `Graph.ExportToCSV` omits mask columns | Post-process step in NC_02 adds them explicitly |
| `LoadModel` fails on feature dimension mismatch | Reference `nodes.csv` has 7 features (zoning ×4 + connectivity ×3); our export must match exactly |

---

## Summary

Four notebooks. NC_01 handles the manual Rhino → CellComplex import (the only step requiring geometry work outside Python). NC_02 builds the graph and exports MSD-compatible CSVs. NC_03 runs spatial analysis. NC_04 runs inference with the pretrained model — no training, no custom model. The pretrained model (`msd_node_classifier.pt`) is stored locally in this folder and tracked in git.
