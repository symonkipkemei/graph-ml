### *Name:*  B. 	Building Brains: The Last 50 Metres

*Topic:*   
Building graphs for autonomous agents

*Description:*   
Delivery is largely solved up to the building entrance; the last 50 metres are not. From the entrance, an agent must pass the lobby, choose the right lift, follow a corridor, find "Apt 7B", and in a multi-level apartment possibly climb an internal stair to reach the kitchen. This stretch is slow even for human couriers: in the Urban Freight Lab's Seattle study, 12.2 of 20 minutes inside the building went on lifts and door-to-door delivery. Service robots can already do it, but each building is prepared individually. Korea's robot-friendly certifications assess readiness with expert-derived checklists that score each door, lift and corridor separately, and Park & Park (2026) explicitly call for robot-navigation simulation to verify such standards.

This thesis decodes a residential building's own data, a verified Revit model checked against a point cloud of the same building, into a topological "building brain" in TopologicPy. The brain is a graph organised by level, from building to level to unit to room, with lifts and stairs as connections. It links each address to its place in the graph, and carries access rules and real clearances measured from the scan. It solves for the brain, not the body. Extending Jabi et al. (2025) from hypothetical offices to a real multi-storey residential building, simulated delivery agents with different abilities, such as wheeled and stair-climbing, perform deliveries to every unit, while resident agents following daily schedules create congestion in lifts and corridors. The graph turns item-by-item checks into network-level checks: a single narrow door on the only route can cut off a whole wing, which a checklist cannot show. The evaluation compares a model-only brain with a model + scan brain, and measures readiness against published door, passageway and lift standards. The contribution is an automated readiness assessment based on the building's own data, made before any robot is deployed.

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
