"""
Grasshopper CPython3 Script Component: Spatial Graph Centrality Analysis

SETUP IN GRASSHOPPER (Rhino 8):
1. Add a "Script" component to the canvas (Maths > Script > CPython3 Script)
2. Right-click the component and add these INPUTS:
   - brep_path   (str)         : path to an OpenCASCADE .brep file (optional, alternative to curves)
   - boundary    (Curve)       : outer boundary curve from Rhino (optional if brep_path is set)
   - obstacles   (list[Curve]) : obstacle/wall curves from Rhino (optional if brep_path is set)
   - grid_size   (int)         : grid spacing in model units (default: 3)
   - analysis    (str)         : "closeness" | "betweenness" | "community" | "degree"
3. Right-click the component and add these OUTPUTS:
   - mesh        (Mesh)        : colored analysis mesh for Rhino viewport
   - graph_lines (list[Line])  : graph edges for visualization

If topologicpy does not auto-install, open Rhino's command line and run:
   _EditPythonScript  ->  Tools  ->  Package Manager  ->  search "topologicpy"
Or in Rhino's Python console:
   import subprocess; subprocess.check_call(["pip", "install", "topologicpy"])
"""

# r: topologicpy

import Rhino.Geometry as rg
import System.Drawing as sd

from topologicpy.Vertex import Vertex
from topologicpy.Edge import Edge
from topologicpy.Wire import Wire
from topologicpy.Face import Face
from topologicpy.Shell import Shell
from topologicpy.Topology import Topology
from topologicpy.Dictionary import Dictionary
from topologicpy.Grid import Grid
from topologicpy.Graph import Graph
from topologicpy.Color import Color


# ---------------------------------------------------------------------------
# Helpers: Rhino <-> topologicpy conversion
# ---------------------------------------------------------------------------

def rhino_curve_to_wire(crv):
    rc, polyline = crv.TryGetPolyline()
    if rc:
        pts = list(polyline)
    else:
        nurbs = crv.ToNurbsCurve()
        count = max(int(crv.GetLength() / 0.5), 4)
        params = nurbs.DivideByCount(count, True)
        pts = [nurbs.PointAt(t) for t in params]
    if len(pts) > 1 and pts[0].DistanceTo(pts[-1]) < 0.001:
        pts = pts[:-1]
    verts = [Vertex.ByCoordinates(p.X, p.Y, p.Z) for p in pts]
    edges = [Edge.ByVertices([verts[i], verts[(i + 1) % len(verts)]]) for i in range(len(verts))]
    return Wire.ByEdges(edges)


def hex_to_color(hex_str):
    h = hex_str.lstrip("#")
    return sd.Color.FromArgb(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def add_face_to_mesh(rhino_mesh, topo_face, color):
    wire = Face.ExternalBoundary(topo_face)
    verts = Wire.Vertices(wire)
    coords = [Vertex.Coordinates(v) for v in verts]
    idx = rhino_mesh.Vertices.Count
    for c in coords:
        rhino_mesh.Vertices.Add(c[0], c[1], c[2])
        rhino_mesh.VertexColors.Add(color)
    n = len(coords)
    if n == 3:
        rhino_mesh.Faces.AddFace(idx, idx + 1, idx + 2)
    elif n == 4:
        rhino_mesh.Faces.AddFace(idx, idx + 1, idx + 2, idx + 3)
    else:
        for i in range(1, n - 1):
            rhino_mesh.Faces.AddFace(idx, idx + i, idx + i + 1)


# ---------------------------------------------------------------------------
# Helpers: dictionary transfer (from notebook utils.py)
# ---------------------------------------------------------------------------

def reset_dicts(shell):
    for f in Topology.Faces(shell):
        d = Topology.Dictionary(f)
        for key in Dictionary.Keys(d):
            if key != "face_id":
                d = Dictionary.RemoveKey(d, key)
        Topology.SetDictionary(f, d)


def transfer_dicts(topologies, selectors, key):
    lookup = {}
    for t in topologies:
        d = Topology.Dictionary(t)
        val = Dictionary.ValueAtKey(d, key, None)
        if val:
            lookup[str(val)] = t
    for s in selectors:
        d = Topology.Dictionary(s)
        val = Dictionary.ValueAtKey(d, key, None)
        if val and str(val) in lookup:
            Topology.SetDictionary(lookup[str(val)], d)


# ===========================================================================
# MAIN PIPELINE
# ===========================================================================

# 1. Build the floorplan face -------------------------------------------
if brep_path:
    floorplan = Topology.ByBREPPath(brep_path)
else:
    bw = rhino_curve_to_wire(boundary)
    ow = [rhino_curve_to_wire(c) for c in obstacles] if obstacles else []
    floorplan = Face.ByWires(bw, ow)
    floorplan = Topology.RemoveCollinearEdges(floorplan)

# 2. Grid overlay + slice into shell ------------------------------------
b_r = Wire.BoundingRectangle(floorplan)
dd = Topology.Dictionary(b_r)
width = Dictionary.ValueAtKey(dd, "width")
length = Dictionary.ValueAtKey(dd, "length")
gs = grid_size if grid_size else 3
uRange = list(range(0, int(width) + gs, gs))
vRange = list(range(0, int(length) + gs, gs))
grid = Grid.EdgesByDistances(floorplan, clip=True, uRange=uRange, vRange=vRange)

shell = Topology.Slice(floorplan, grid)
faces = Topology.Faces(shell)
for i, f in enumerate(faces):
    f = Topology.SetDictionary(f, Dictionary.ByKeyValue("face_id", f"face_{i+1}"))

# 3. Build analysis graph -----------------------------------------------
analysis_graph = Graph.ByTopology(shell)
g_verts = Graph.Vertices(analysis_graph)

# 4. Run selected analysis ----------------------------------------------
analysis_type = (analysis or "closeness").lower().strip()
color_key = None

if analysis_type == "closeness":
    Graph.ClosenessCentrality(analysis_graph, colorScale="thermal")
    color_key = "cc_color"

elif analysis_type == "betweenness":
    Graph.BetweennessCentrality(analysis_graph, normalize=True, colorScale="thermal")
    color_key = "bc_color"

elif analysis_type == "community":
    Graph.CommunityPartition(analysis_graph, colorScale="thermal")
    color_key = "cp_color"

elif analysis_type == "degree":
    # Step A: community partition (needed to group faces)
    Graph.CommunityPartition(analysis_graph, colorScale="thermal")
    reset_dicts(shell)
    faces = Topology.Faces(shell)
    transfer_dicts(faces, g_verts, "face_id")

    # Step B: bin faces by community and create room-level faces
    bins = Topology.BinByDictionaryKey(faces, key="community")
    bin_dict = bins[0]
    face_groups = []
    for key in bin_dict:
        temp_shell = Shell.ByFaces(bin_dict[key])
        eb = Shell.ExternalBoundary(temp_shell)
        eb = Wire.RemoveCollinearEdges(eb)
        face_groups.append(Face.ByWire(eb))

    # Step C: new shell & graph at room level
    new_shell = Shell.ByFaces(face_groups)
    new_graph = Graph.ByTopology(new_shell)
    new_verts = Graph.Vertices(new_graph)
    dc_values = Graph.DegreeCentrality(new_graph, normalize=False)

    # Step D: interpolate back to original graph vertices
    for v in g_verts:
        Vertex.InterpolateValue(v, vertices=new_verts, n=3, key="degree_centrality")

    # Step E: derive colors
    min_dc, max_dc = min(dc_values), max(dc_values)
    for v in g_verts:
        d = Topology.Dictionary(v)
        dc = Dictionary.ValueAtKey(d, "degree_centrality")
        hex_c = Color.AnyToHex(
            Color.ByValueInRange(dc, minValue=min_dc, maxValue=max_dc, colorScale="viridis")
        )
        d = Dictionary.SetValueAtKey(d, "dc_color", hex_c)
        Topology.SetDictionary(v, d)

    color_key = "dc_color"

# 5. Transfer analysis data from graph vertices to shell faces ----------
reset_dicts(shell)
faces = Topology.Faces(shell)
transfer_dicts(faces, g_verts, "face_id")

# 6. Build colored Rhino Mesh ------------------------------------------
mesh = rg.Mesh()
gray = sd.Color.Gray
for face in faces:
    d = Topology.Dictionary(face)
    hx = Dictionary.ValueAtKey(d, color_key) if color_key else None
    c = hex_to_color(hx) if hx else gray
    add_face_to_mesh(mesh, face, c)
mesh.Normals.ComputeNormals()

# 7. Build graph-edge lines for optional visualisation ------------------
graph_lines = []
for e in Graph.Edges(analysis_graph):
    sv, ev = Edge.StartVertex(e), Edge.EndVertex(e)
    sc, ec = Vertex.Coordinates(sv), Vertex.Coordinates(ev)
    graph_lines.append(rg.Line(rg.Point3d(*sc), rg.Point3d(*ec)))
