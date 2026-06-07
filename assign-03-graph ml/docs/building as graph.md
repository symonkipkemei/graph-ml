# Assignment 03 — Building as a Graph: Documentation

## Overview

This assignment models a real building as a graph and uses a pre-trained Graph Neural Network (GNN)
to classify the building's relationship to the ground. The model is trained on a dataset of 1,496
buildings and predicts one of five architectural categories called the Building-Ground Relationship (BGR).

| Label | Category | Description |
|-------|----------|-------------|
| 0 | Separation | Building floats above ground — clear gap underneath (pilotis) |
| 1 | Separation with Plinth | Detached from ground but raised on a base |
| 2 | Adherence | Building sits flush on the ground, direct contact |
| 3 | Adherence with Plinth | Sits on a podium/plinth that sits on the ground |
| 4 | Interlock | Building penetrates into the ground (basement, sunken) |

---

## Folder Structure

```
assign-03-graph ml/
│
├── docs/
│   └── assignment-03-understanding.md       — this file
│
├── notebooks/
│   ├── S06-13 GML Graph Classification.ipynb  — lecturer reference (do not run)
│   ├── S06-13A GML Creating BGR Graph - STUDENT.ipynb  — Step 1: build graph
│   └── S06-13B GML Predict BGR Graph.ipynb     — Step 2: predict BGR label
│
├── outputs/
│   ├── building-1.png                       — Rhino building render
│   ├── building-2.png                       — Rhino building render
│   ├── graph.png                            — adjacency graph visualisation
│   ├── prediction.png                       — prediction result screenshot
│   ├── topology-1.png                       — CellComplex visualisation
│   └── topology-2.png                       — CellComplex with transferred tags
│
└── supporting_files/
    ├── building.3dm                         — Rhino source model
    ├── bgr_model.pt                         — pre-trained GraphSAGE model (provided by faculty)
    ├── obj/
    │   ├── ground.obj                       — floor slab / podium geometry
    │   ├── columns.obj                      — structural columns geometry
    │   ├── offices.obj                      — office programme volumes
    │   └── core.obj                         — stair core and corridors
    └── bgr_dataset/
        ├── graphs.csv                       — one row: graph_id=0, label=3
        ├── nodes.csv                        — 146 nodes with one-hot features
        ├── edges.csv                        — 748 adjacency edges
        └── meta.yaml                        — dataset metadata
```

---

## The Building

The building is a stepped, podium-based structure modelled in Rhino. It has:
- A wide flat **podium/ground slab** sitting directly on the ground
- **Structural columns** supporting upper volumes in the central section
- Multiple **office volumes** stepping up from the podium
- A **stair core** rising from the building mass

The building was assessed as **Label 3 — Adherence with Plinth**: the podium adheres to
the ground with upper programme volumes rising from it.

---

## Workflow

The assignment runs across two notebooks in sequence.

### Step 1 — S06-13A: Build the Graph

Takes the Rhino model from OBJ files and converts it into a graph dataset.

**Paths configured:**
- `SUPPORT_DIR` = `supporting_files/obj/` — source OBJ files
- `EXPORT_DIR` = `supporting_files/bgr_dataset/` — output CSVs

**Pipeline:**

1. **Import OBJs** — load `ground.obj`, `columns.obj`, `offices.obj`, `core.obj`
   via `Topology.ByOBJPath`

2. **Assign categories** — tag every cell with `cell_type`, `cell_name`, `cell_color`
   using a selector + `Dictionary.ByKeysValues`:

   | Layer | cell_type | cell_color |
   |-------|-----------|------------|
   | ground | 0 | green |
   | column | 1 | gray |
   | office | 3 | blue |
   | core | 4 | red |

3. **Build CellComplex** — merge all cells into one unified model:
   `Topology.SelfMerge(Cluster.ByTopologies(all_cells))`

4. **Transfer dictionaries** — propagate tags from selectors onto the merged model:
   `Topology.TransferDictionariesBySelectors(model, selectors, tranCells=True)`

5. **Build adjacency graph** — create graph and encode each node as a one-hot vector:
   - `Graph.ByTopology(model)` → adjacency graph where nodes = spaces, edges = shared walls
   - `one_hot_encode(cell_type, 5)` → `[feat_00, feat_01, feat_02, feat_03, feat_04]`
   - Visualised with `Topology.Show(graph, vertexColorKey='cell_color', vertexSize=10)`

6. **Export CSV** — write graph to disk:
   `Graph.ExportToCSV(graph, path=EXPORT_DIR, nodeFeaturesKeys=feature_names, overwrite=True)`

**Output dataset (your building):**

| File | Contents |
|------|----------|
| `graphs.csv` | 1 graph — `graph_id=0`, `label=3` (your assessment) |
| `nodes.csv` | 146 nodes — `cell_type` + one-hot features + X/Y/Z coordinates |
| `edges.csv` | 748 edges — adjacency pairs between spaces |

---

### Step 2 — S06-13B: Predict the BGR Label

Loads the exported CSVs and the pre-trained model, then classifies the building.

**Paths configured:**
- `DATASET_PATH` = `supporting_files/bgr_dataset/`
- `MODEL_PATH` = `supporting_files/bgr_model.pt`

**Pipeline:**
1. Load the dataset with `PyG.ByCSVPath`
2. Load the pre-trained model with `pyg_2.LoadModel`
3. Set the full dataset as test split: `SetHyperparameters(split=(0.0, 0.0, 1.0))`
4. Run `pyg_2.Predict()` — returns predicted label, actual label, and confidence

**Reading the result:**

| Column | Meaning |
|--------|---------|
| Actual Label | Your assessment set in `graphs.csv` (label=3, Adherence with Plinth) |
| Predicted Label | What the model classified your building as |
| Confidence | Model's certainty (0.0 to 1.0) |

The goal is to see whether the pre-trained model agrees with your own assessment.

---

## The Pre-trained Model

- **File:** `bgr_model.pt` (provided by faculty — 35 MB)
- **Architecture:** GraphSAGE — two hidden layers (128 x 128), ReLU, mean pooling,
  batch normalisation, residual connections, 20% dropout
- **Trained on:** 1,496 building graphs, 5 BGR classes
- **Test accuracy:** ~99.3%

The model was trained on the following class distribution:

| Label | Type | Training count |
|-------|------|---------------|
| 0 | Separation | 525 |
| 1 | Separation with Plinth | 543 |
| 2 | Adherence | 72 |
| 3 | Adherence with Plinth | 56 |
| 4 | Interlock | 300 |

---


---

## Dependencies

```
topologicpy >= 0.9.31
torch (CPU build — 2.12.0+cpu)
torch_geometric >= 2.8.0
pandas
pyyaml
numpy
plotly
scikit-learn
```

Python 3.11 | Virtual environment: `E:\softwares-4\graph-ml\venv\`
