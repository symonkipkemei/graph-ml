---
name: gmlenv-environment
description: How the .gmlenv virtual environment for this MACAD Graph ML project is set up and repaired
metadata:
  type: project
---

The project venv is `.gmlenv/`, a **Python 3.11** environment (interpreter at `C:\Users\giofo\AppData\Local\Programs\Python\Python311`). It was originally created with `uv` (leaves an empty `.lock` file). The official MACAD course setup (Discord, channel @canale) is minimal: `py -3.11 -m venv .gmlenv`, activate `.gmlenv\Scripts\Activate.ps1`, then `pip install topologicpy==0.9.18` and `pip install nbformat>=4.2.0`.

This venv goes beyond the course baseline: it also carries an ML stack — `torch 2.5.1+cu121` (CUDA 12.1, GPU works), `torchvision`/`torchaudio` cu121, `torch_geometric 2.8.0`, plus specklepy, igraph, scikit-learn, plotly, ipykernel. The `+cu121` torch wheels come from `https://download.pytorch.org/whl/cu121`, not plain PyPI — needed when rebuilding.

Repair tip: this venv has shown up missing its `Scripts/` and `pyvenv.cfg` (only `Lib/`, `Include/`, `.lock` present) — making it look unusable. Running `py -3.11 -m venv .gmlenv` over the existing folder regenerates the interpreter/launcher **without deleting `Lib/site-packages`**, so the ~2.5 GB torch download is preserved. A full package manifest now lives in `requirements.txt` at the repo root. See [[prefer-newest-topologicpy]].
