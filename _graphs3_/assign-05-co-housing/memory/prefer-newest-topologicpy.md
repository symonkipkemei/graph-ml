---
name: prefer-newest-topologicpy
description: User prefers the newest topologicpy, not the course-pinned 0.9.18
metadata:
  type: feedback
---

The MACAD course instructions pin `topologicpy==0.9.18`, but the user explicitly chose to use the **newest** topologicpy instead (installed 0.9.52 on 2026-06-25).

**Why:** they want current features/fixes over exact course reproducibility.
**How to apply:** when installing or upgrading topologicpy in [[gmlenv-environment]], use the latest PyPI release (`pip install --upgrade topologicpy`) rather than the 0.9.18 pin — unless the user says otherwise for a specific course notebook.
