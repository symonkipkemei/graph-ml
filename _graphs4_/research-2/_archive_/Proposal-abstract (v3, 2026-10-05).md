### *Name:*  B. 	Building graphs for autonomous delivery agents in mutilevel apartments

*Topic:*   
Graph Generation for AEC 

*Description:*   
Delivery is largely solved up to the building entrance; the last 50 metres are not. From the entrance, an agent must pass the lobby, choose the right lift, follow a corridor, find "Apt 7B", and in a multi-level apartment possibly climb an internal stair to reach the kitchen. This stretch is slow even for human couriers: in the Urban Freight Lab's Seattle study, 12.2 of 20 minutes inside the building went on lifts and door-to-door delivery. Service robots can already do it, but each building is prepared individually. Korea's robot-friendly certifications assess readiness with expert-derived checklists that score each door, lift and corridor separately, and Park & Park (2026) explicitly call for robot-navigation simulation to verify such standards.

This thesis turns a building's own digital model into a "brain" that robots can use. Starting from the building's Revit model, checked against a 3D scan of the building as it really is, it maps how every space connects: entrances, lifts, corridors, apartments and the rooms inside them. Building on Jabi et al. (2025), simulated delivery robots then use this map to attempt a delivery to every apartment, sharing lifts and corridors with simulated residents going about their day. When a delivery fails, the tool shows where and why, for example a door too narrow, a lift the robot cannot use, or a corridor blocked by clutter, and which changes would help most. Because the map captures how spaces connect, not just individual doors and corridors, it reveals what a checklist misses: one narrow door on the only route can cut off a whole wing. The result is a way to tell whether a building is ready for delivery robots before any robot arrives.

*Technologies:* 

TopologicPy (navigation graphs, multi-agent simulation), Revit API, point-cloud processing, Python

*Outcome:*   
A working delivery-readiness simulator that takes a verified Revit model and a point cloud and returns:
- a readiness map by unit and level
- simulated delivery routes, with the cause of each failure
- a ranked list of changes to the building (widen a door, give lift access, clear a corridor) that would most improve readiness

*Resources:*   
Jabi, W., Xue, Y., Woolley, T. E. & Kaouri, K. (2025). 3D Topological Modeling and Multi-Agent Movement Simulation for Viral Infection Risk Analysis. *Architectural Science Review.*

Park, Y. & Park, S. (2026). Development of Human-Centered, Robot-Adaptive Building Design Standards: Focusing on Korea's Building Certification Systems. *Architectural Research* 28:14.

Jung, M., Jang, S., Gu, H., Yoon, D. & Kim, K. (2023). Development of Certification Model of Robot-Friendly Environment for Apartment Complexes. *Journal of Cadastre & Land InformatiX* 53(1), 83–105.

Urban Freight Lab (2018). *The Final 50 Feet of the Urban Goods Delivery System.* University of Washington.
