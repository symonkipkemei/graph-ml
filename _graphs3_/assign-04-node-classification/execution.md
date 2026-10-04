# Execution Proposal: Graph Learning Pipeline for Architectural Floor Plans

## Why we are doing this

Architecture is fundamentally relational — a bedroom only makes sense because it connects to a corridor, which connects to a living room, which connects to a staircase. Drawings and 3D models capture geometry, but they don't capture this relational logic in a form a computer can reason about. Graphs do.

This project demonstrates the full pipeline: from a real building design, through graph construction, to a machine learning model that infers room function purely from graph structure — no geometry, no areas, no coordinates. Just connectivity.

The central question is: **can a model trained on 500 Swiss apartment graphs correctly classify the rooms in a building it has never seen?** If it can, that confirms that graph topology alone carries enough architectural meaning to be useful. If it partially fails, the errors themselves are informative — they reveal which room types are structurally ambiguous and why.

The three things the presentation needs to show:
1. That we understood how to translate a physical building into a graph representation that matches the MSD dataset schema
2. That graph metrics reveal something meaningful about the spatial organisation of the building
3. That we can run and interpret a GNN inference result — including honest analysis of where and why the model is wrong

---

## What changed from `_outdated_`

| Old (FA notebooks) | New (NC notebooks) | Why |
|---|---|---|
| `FA_05` tried to train a GNN → NaN loss crash | `NC_03` runs **inference only** with pretrained model | Instructions-2 removed training; instructions-3 points to S06-15C |
| All edges used `door_type="door"` only | Three door types: `passage`, `door`, `entrance_door` | Node_Classification_Instructions.docx requires all three |
| Features hand-crafted as CSV rows | `EncodeMSDGraphFeatures()` from S06-15B derives features from CellComplex | Follows the prescribed workflow |
| Balconies (label=8) used as entry/hub nodes | Architecturally coherent room programme | Spatial sense required for the presentation |

---

## Folder Structure

```
assign-04-node-classification/
  execution.md
  instructions/
    instructions-1.txt
    instructions-2.txt
    instructions-3.txt
    dataset.txt
  model/
    msd_node_classifier.pt            ← pretrained model, tracked in git
  geometry/                           ← OBJ exports from Rhino (inputs)
    rooms.obj
    apertures.obj
  notebooks/
    NC_01_rhino_to_cellcomplex.ipynb  ← manual prep + import from Rhino
    NC_02_graph_construction.ipynb    ← CellComplex → Graph → CSV export
    NC_03_spatial_analysis.ipynb      ← graph metrics + interpretation
    NC_04_node_classification.ipynb   ← inference with pretrained model
  graphs/                          ← CSV outputs from NC_02
    graphs.csv
    nodes.csv
    edges.csv
    floor_plan_meta.json
  outputs/                            ← analysis outputs from NC_03 + NC_04
    spatial_analysis.json
    node_predictions.csv
  _outdated_/                         ← archived previous attempt
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
rooms_raw = Topology.ByOBJPath(r"E:\softwares-4\graph-ml\assign-04-node-classification\geometry\rooms.obj", transposeAxes=False)

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
apertures_raw = Topology.ByOBJPath(r"E:\softwares-4\graph-ml\assign-04-node-classification\geometry\apertures.obj", transposeAxes=False)
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
Graph.ExportToCSV(graph, path=r"graphs/", overwrite=True)

# 5. Post-process: add inference masks (all nodes are test-only)
import pandas as pd
nodes = pd.read_csv("graphs/nodes.csv")
nodes["train_mask"] = False
nodes["val_mask"]   = False
nodes["test_mask"]  = True
nodes.to_csv("graphs/nodes.csv", index=False)
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
1. Reload graph: `Graph.ByCSVPath(path="graphs/")`
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
DATASET_PATH = Path(r"E:\softwares-4\graph-ml\assign-04-node-classification\graphs")
MODEL_PATH   = Path(r"E:\softwares-4\graph-ml\assign-04-node-classification\model\msd_node_classifier.pt")
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

## Step 5 — Scale to Multiple CellComplexes (after single-graph run is verified)

**Prerequisite:** Steps 1–4 completed and NC_04 produces valid predictions for the single sample graph.

**Goal:** Extend the dataset to multiple CellComplexes (e.g. one per floor, one per apartment block) so the pretrained model classifies each independently and results can be compared across units.

**Why this works:** The CSV schema uses `graph_id` to separate graphs. `PyG.ByCSVPath()` and the pretrained model both handle any number of graphs transparently. The S06-15C visualisation cell uses `graphs[i]` — swap `graphs[0]` for a loop over all graphs.

**Workflow — add to `NC_02_graph_construction.ipynb`:**

```python
import pandas as pd
from pathlib import Path

cell_complexes = [cc_floor1, cc_floor2]  # add as many as needed

graphs_dfs, nodes_dfs, edges_dfs = [], [], []

for i, cc in enumerate(cell_complexes):
    graph = Graph.ByTopology(cc, direct=False, directApertures=True)
    graph = EncodeMSDGraphFeatures(graph)
    temp_path = Path(f"temp/graph_{i}")
    temp_path.mkdir(parents=True, exist_ok=True)
    Graph.ExportToCSV(graph, path=str(temp_path), overwrite=True)

    g = pd.read_csv(temp_path / "graphs.csv")
    n = pd.read_csv(temp_path / "nodes.csv")
    e = pd.read_csv(temp_path / "edges.csv")

    # ExportToCSV writes graph_id=0 each time — reassign to unique id
    g["graph_id"] = i
    n["graph_id"] = i
    e["graph_id"] = i

    # Add inference masks if not already present
    for col in ["train_mask", "val_mask", "test_mask"]:
        if col not in n.columns:
            n[col] = col == "test_mask"

    graphs_dfs.append(g)
    nodes_dfs.append(n)
    edges_dfs.append(e)

pd.concat(graphs_dfs).to_csv("graphs/graphs.csv", index=False)
pd.concat(nodes_dfs).to_csv("graphs/nodes.csv",  index=False)
pd.concat(edges_dfs).to_csv("graphs/edges.csv",  index=False)
```

**Update NC_04 visualisation cell to loop over all graphs:**
```python
# Replace single graphs[0] call with a loop
for i, g in enumerate(graphs):
    Topology.Show(g, vertexSize=6, vertexSizeKey="size",
                  vertexColorKey="pred_color",
                  showVertexLabel=True, vertexLabelKey="pred",
                  backgroundColor="white", camera=[0,0,3],
                  vertexLabelFontSize=18)
```

**Notes:**
- `node_id` is local per graph (each starts from 0) — the merge is safe
- Each graph is classified independently — neighbourhood context does not cross CellComplex boundaries
- For the presentation, side-by-side prediction results across floors/apartments make a strong visual comparison

---

---

## Final Outputs — What to Present

### Floor plan & graph construction

| Output | How to produce | What it shows |
|---|---|---|
| 3D render of CellComplex | `Topology.Show(cc)` in TopologicPy or screenshot from Rhino | The physical building — gives the audience a spatial anchor before graphs appear |
| Graph coloured by room type | `Topology.Show(graph)` with `vertexColorKey="room_type"` | The abstract graph laid out spatially; nodes labelled by room type |
| Room and edge count table | Print from `floor_plan_meta.json` | Confirms alignment with MSD schema: 9 room types, 3 door types represented |

### Spatial analysis

| Output | How to produce | What it shows |
|---|---|---|
| Bar chart — degree centrality per node | `matplotlib` bar, nodes on x-axis, coloured by room type | Which rooms are most physically connected; corridors and stairs should dominate |
| Bar chart — closeness centrality per node | Same pattern | Which rooms are most reachable; stairs should score highest as inter-floor bridge |
| Bar chart — clustering coefficient per node | Same pattern | Contrast: high inside apartments (rooms share neighbours), low at stairs (bridge node) |
| Shortest path heatmap | `seaborn.heatmap` on the all-pairs distance matrix | Visual summary of travel depth; group rows/columns by apartment to show unit boundaries |
| One-paragraph interpretation | Written in the notebook as markdown | Links each metric to an architectural observation (accessibility, hierarchy, evacuation depth) |

### Node classification

| Output | How to produce | What it shows |
|---|---|---|
| True-label graph | `Topology.Show()` with `vertexColorKey="true_color"`, `vertexLabelKey="true"` | Ground truth — what the rooms actually are |
| Predicted-label graph | Same with `vertexColorKey="pred_color"`, `vertexLabelKey="pred"` | What the model thinks — place side-by-side with the true graph |
| Confusion matrix | `sklearn.metrics.ConfusionMatrixDisplay` | Which room types are confused with each other; e.g. bedroom vs storeroom |
| Misclassified node table | Filter `node_predictions.csv` where `y_true != y_pred` | For each error: room type, degree, neighbour types — the raw material for the explanation |
| Accuracy by room type | Group `node_predictions.csv` by `y_true`, compute correct% | Shows whether structurally distinctive rooms (stairs, balcony) predict better than ambiguous ones (bedroom, storeroom) |
| Error explanation paragraph | Written analysis | The most important slide — e.g. "bedroom and storeroom are confused because both have degree 1 and connect only to a corridor; the model cannot distinguish them from connectivity alone" |

### Suggested slide order for the presentation

1. Dataset & references — MSD overview, label schema, what the two papers contributed
2. Floor plan — Rhino 3D render, room programme table, design rationale
3. Graph construction — CellComplex → graph pipeline diagram, final graph coloured by room type
4. Spatial analysis — four metric charts, one interpretation paragraph per metric
5. Node classification — true vs predicted side-by-side, confusion matrix, error table
6. Discussion — what the errors reveal, what would improve predictions (richer features, larger graph, balcony connectivity), what the pipeline could be used for in practice

---

## Summary

Four notebooks for the single-graph run (Steps 1–4), then Step 5 scales to multiple CellComplexes once the pipeline is verified end-to-end. The pretrained model (`msd_node_classifier.pt`) is stored locally in this folder and tracked in git.
