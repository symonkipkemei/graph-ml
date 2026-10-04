### *Name:*  A. 	Elements to Edges, Building Graphs as a QAQC Tool 

*Topic:*   
Graph Generation for AEC 

*Description:*   
Quality assurance and quality control (QAQC) on BIM models is still largely a manual, end-of-project exercise: someone opens the model and checks adjacency, circulation, and egress compliance by eye, usually once, near delivery, rather than as the design develops. This thesis reframes the building graph as a continuous QAQC instrument rather than a one-off audit. 

A Revit add-in maintains a live graph of the model's relational structure, using the Revit API's Document.Changed event and Updater framework so checks run automatically as the design changes, without a separate review being scheduled. The checks themselves go beyond simple adjacency rules: betweenness centrality and articulation-point analysis flag which rooms or corridors are single points of failure for egress, giving QAQC a network-robustness dimension that rule-based clash detection does not provide. 

Because a QAQC tool is only useful if it works on real project files, not clean benchmark data, TopologicPy's defeaturing capability simplifies messy geometry before analysis, and link-prediction methods infer likely missing adjacency or circulation relationships where the model itself is incomplete. Extraction reliability is validated by comparing TopologicPy against a custom Revit API geometric approach across a set of real, imperfect practice models. The completed tool is then tested against the saved version history of real projects, restaging each iteration and running the QAQC checks at every stage, to measure whether continuous graph-based QAQC would have caught violations earlier than the manual review actually did. A natural-language query layer remains a secondary, exploratory feature. The contribution is evidence, from real project histories, that graph-based QAQC can meaningfully shorten the gap between a problem occurring and a problem being caught. 

*Technologies:* 

Revit API, TopologicPy (defeaturing, ontology/BOT),  Python

*Outcome:*   
A working Revit add-in that runs on demand at model sign-off and returns a structured report of relational and network violations, adjacency inconsistencies, egress single points of failure, incomplete or missing relationships .

*Resources:*   
Jabi, W., & Chatzivasileiadi, A. (2021). *Topologic: Exploring Spatial Reasoning Through Geometry, Topology, and Semantics.* Formal Methods in Architecture, Cardiff University / UCL. 

