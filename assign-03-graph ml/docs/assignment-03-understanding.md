# Assignment 03 — Understanding & Breakdown

## What the Assignment Is About

This assignment asks you to model a real building, convert it into a graph representation, and then feed that graph into a pre-trained Graph Neural Network (GNN) to classify the building's architectural type.

The classification task targets five building-relationship categories:

| Label | Category |
|-------|----------|
| 0 | Separation |
| 1 | Separation with Plinth |
| 2 | Adherence |
| 3 | Adherence with Plinth |
| 4 | Interlock |

---

## The Two Notebooks

### Notebook 1 — `S06-13 GML Graph Classification.ipynb` (Reference / Lecture Notebook)

This is the **lecturer's complete notebook**. It demonstrates the full pipeline end-to-end on an existing dataset of 1,496 building graphs:

1. Reads a prepared CSV dataset (`graphs.csv`, `nodes.csv`, `edges.csv`, `meta.yaml`)
2. Loads it into `topologicpy.PyG`
3. Trains a **GraphSAGE** model for graph-level classification (5 classes)
4. Evaluates with train/val/test splits (80/10/10)
5. Plots training curves and confusion matrices
6. Saves the trained model (`pyg_model.pt`)
7. **Phase 2:** Loads a *new unseen* building graph, runs inference, and outputs the predicted label with confidence

The pre-trained model achieves ~99.3% accuracy on the test set. The saved `pyg_model.pt` is what you will reuse in Phase 2 to classify your own building.

### Notebook 2 — `S06-13A GML Creating BGR Graph - STUDENT.ipynb` (Your Working Notebook — Make a Copy)

This is the **student notebook with TODOs**. You fill in the code to go from a 3D Rhino model to a graph CSV, then send that graph to the classifier. The pipeline has seven steps:

1. **Import OBJs** — export four separate OBJ files from Rhino and load them with `Topology.ByOBJPath`
2. **Assign categories** — tag every cell (space volume) with a `cell_type` integer, a `cell_name`, and a display colour
3. **Build CellComplex** — merge all cells into one unified topological model via `Topology.SelfMerge`
4. **Transfer dictionaries** — propagate the `cell_type` tags onto the merged model's cells using selectors
5. **Build adjacency graph** — run `Graph.ByTopology` and encode each node's `cell_type` as a **one-hot vector** (`feature_00` ... `feature_04`)
6. **Export CSV** — write `graphs.csv`, `nodes.csv`, `edges.csv` to disk with `Graph.ExportToCSV`
7. **Predict** — open `S06-13` (Phase 2), point it at your export folder, load `pyg_model.pt`, call `Predict()`, and read the label 0-4

---

## The Dataset Format

Every building in the dataset is stored as three CSV files:

| File | Contents |
|------|----------|
| `graphs.csv` | One row per building — `graph_id`, `label` (0-4) |
| `nodes.csv` | One row per room/space — `node_id`, `graph_id`, `label`, plus one-hot feature columns |
| `edges.csv` | One row per adjacency — `src_id`, `dst_id`, `graph_id`, `label` |

The node features are one-hot encodings of the space type:

| Index | Space type |
|-------|-----------|
| 0 | Ground / slab |
| 1 | Column |
| 2 | Plinth (optional) |
| 3 | Office volume |
| 4 | Core / corridor |

---

## The Rhino Modelling Requirement

Your building must be modelled in **Rhino** and exported as four separate OBJ files, one per layer:

| File | Content |
|------|---------|
| `ground.obj` | Floor slab or podium |
| `columns.obj` | Structural columns |
| `offices.obj` | Office/programme volumes |
| `core.obj` | Stair core and corridors |

The building should be **similar in type and scale** to those already in the dataset — meaning a multi-cell building with a clear structural hierarchy (ground, columns, core, offices) that maps cleanly onto the five category labels.

---

## The ML Model

- **Architecture:** GraphSAGE with two hidden layers (128 x 128), ReLU activations, mean pooling, batch normalisation, residual connections, 20% dropout
- **Task:** Graph-level classification (one label per whole building)
- **Training data:** 1,496 building graphs, 5 classes
- **Optimiser:** AdamW, lr = 0.001, weight decay = 1e-4, gradient clipping = 1.0
- **Validation strategy:** Holdout (80/10/10 split), early stopping (patience = 12)
- **Achieved accuracy:** ~99.3% on the test split

The model takes a building's adjacency graph (rooms as nodes, shared walls as edges) and predicts which of the five architectural relationship types it belongs to.

---

## What You Need to Complete

All cells marked `# TODO` in `S06-13A`:

1. Set `SUPPORT_DIR` to where your OBJ files live
2. Call `Topology.ByOBJPath` for each of the four OBJ files
3. Call `Topology.Show` to visualise the imported geometry
4. Build `selectors` by looping over each layer's cells and attaching a dictionary (`cell_type`, `cell_name`, `cell_color`)
5. Merge all cells into one `model` with `Topology.SelfMerge`
6. Transfer dictionaries onto the merged model
7. Implement `one_hot_encode(value, n)` — returns a list of `n` zeros with a `1` at position `value`
8. Call `Graph.ByTopology(model)` and `Graph.Vertices(graph)` with the correct arguments
9. Loop over vertices: read `cell_type`, encode it, write the five feature keys back to each vertex's dictionary
10. Call `Graph.ExportToCSV` pointing to your export directory
11. Switch to `S06-13`, Phase 2, set the dataset path to your export folder, load the model, and run `Predict()`

---

## Submission Checklist

- [ ] Rhino model built — building type matches the dataset categories
- [ ] Four OBJ files exported (`ground.obj`, `columns.obj`, `offices.obj`, `core.obj`)
- [ ] Student notebook (`S06-13A` copy) runs from top to bottom without errors
- [ ] `graphs.csv`, `nodes.csv`, `edges.csv` generated successfully
- [ ] Prediction obtained from `S06-13` Phase 2 (label 0-4 with confidence score)
- [ ] Both notebooks submitted

---

## Key Dependencies

```
topologicpy >= 0.9.31
torch
torch_geometric
pandas
pyyaml
numpy
plotly
scikit-learn
```

The reference dataset and additional examples can be found at:
`https://github.com/wassimj/topologicpy/tree/main/assets/MachineLearning`
