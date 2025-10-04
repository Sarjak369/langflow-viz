# Entry point (load workflow + visualize)

import json
from graphviz import Digraph
from visualizer.exporter import Exporter
from visualizer.style import STYLE

# Load workflow JSON
with open("examples/sample_workflow.json") as f:
    workflow = json.load(f)

nodes = workflow["nodes"]
edges = workflow["edges"]
name = workflow["name"]

# Initialize Graphviz
g = Digraph(name=name, format="png")
for node in nodes:
    style = STYLE["node"]
    g.node(node, **style)

g.node("START", **STYLE["start"])
g.node("END", **STYLE["end"])

for src, dst in edges:
    g.edge(src, dst, **STYLE["edge"])

# Exporter
exporter = Exporter(g, name)
exporter.to_png()
exporter.to_svg()
exporter.to_mermaid(nodes, edges)

with open(f"outputs/{name}.mmd") as f:
    mermaid_text = f.read()
exporter.to_html(mermaid_text)

print(f"✅ Workflow '{name}' visualization generated successfully!")
