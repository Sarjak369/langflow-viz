# 🌀 LangFlow-Viz

**A Python Library for Workflow Graph Visualization & Analysis**

LangFlow-Viz is a **lightweight yet powerful** toolkit for building, analyzing, and visualizing directed workflow graphs.

It provides modular components to **model process flows**, **detect structural insights** (like cycles and dead ends), and **generate beautiful visualizations** in Graphviz, Mermaid, and HTML formats — all with a few lines of Python.


<p align="left">
  <a href="https://pypi.org/project/langflow-viz/">
    <img src="https://img.shields.io/pypi/v/langflow-viz.svg?label=PyPI&logo=pypi" alt="PyPI">
  </a>
  <a href="https://img.shields.io/pypi/pyversions/langflow-viz.svg">
    <img src="https://img.shields.io/pypi/pyversions/langflow-viz.svg" alt="Python versions">
  </a>
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
  </a>
</p>



## ✨ Key Features

- 🧩 **StateGraph Builder** — Create nodes, edges, and conditional (dashed) branches programmatically
- 🔍 **GraphAnalyzer** — Automatically detect cycles, isolated nodes, and compute longest paths
- 🎨 **Visualizer** — Export high-quality workflow diagrams (SVG, PNG, Mermaid, HTML)
- ⚙️ **Modular Design** — Use each module independently or together
- 🪄 **Fully Customizable** — Override colors, shapes, fonts, and themes via a global `STYLE` dictionary
- 🔁 **Supports Parallel & Conditional Flows** — Model real-world pipelines and decision trees effortlessly

---

## 📦 Installation

Install directly from PyPI:

```bash
pip install langflow-viz

```

Or from source:

```bash
git clone https://github.com/Sarjak369/langflow-viz.git
cd langflow-viz
pip install -e .

```

---

## 🚀 Quick Start

### Example 1: Simple Sequential Workflow

```python
from langflow_viz import Visualizer, analyze_graph

# Define a simple flow
nodes = ["start", "plan", "act", "reflect", "finish"]
edges = [
    ("start", "plan"),
    ("plan", "act"),
    ("act", "reflect"),
    ("reflect", "finish")
]

# Analyze
report = analyze_graph(nodes, edges)
print("📊 Graph Analysis:", report)

# Visualize
viz = Visualizer("LangFlowViz_Test", nodes, edges)
viz.render_all()

```

### 🧾 Output:

- **SVG:** `outputs/LangFlowViz_Test.svg`
- **Mermaid:** `outputs/LangFlowViz_Test.mmd`
- **PNG / HTML:** Optional rich export formats

---

### Example 2: Conditional Workflow (Decision Branches)

```python
from langflow_viz.graph import StateGraph
from langflow_viz import Visualizer

# Define workflow graph
graph = StateGraph()
graph.add_edge("start", "classify")
graph.add_conditional_edge("classify", "creative")
graph.add_conditional_edge("classify", "general")
graph.add_conditional_edge("classify", "technical")
graph.add_edge("creative", "end")
graph.add_edge("general", "end")
graph.add_edge("technical", "end")

# Visualize and export
viz = Visualizer(
    name="ConditionalFlow",
    nodes=graph.get_nodes(),
    edges=graph.get_edges(),
    conditional_edges=graph.conditional_edges  
)
viz.render_all()

```

💡 *Conditional edges appear as dashed lines, representing optional or decision-based transitions.*

---

### Example 3: Parallel Tasks / Merge Flow

```python
from langflow_viz.graph import StateGraph
from langflow_viz import Visualizer, analyze_graph

g = StateGraph()
g.add_edge("start", "task_A")
g.add_edge("start", "task_B")
g.add_edge("task_A", "merge")
g.add_edge("task_B", "merge")
g.add_edge("merge", "end")

print(analyze_graph(g.get_nodes(), g.get_edges()))

viz = Visualizer("ParallelFlow", g.get_nodes(), g.get_edges())
viz.render_all()

```

---

## 🧠 Core Modules & API Reference

### 🧩 **StateGraph** — Build Workflows

`langflow_viz.graph.state_graph`

| Method | Description |
| --- | --- |
| `add_node(name)` | Add a node if not already present |
| `add_edge(src, dst, conditional=False)` | Add a directed edge (supports dashed/conditional edges) |
| `add_conditional_edge(src, dst)` | Shortcut for dashed conditional edge |
| `get_nodes()` | Return list of nodes |
| `get_edges()` | Return list of all edges |
| `get_conditional_edges()` | Return set of all dashed conditional edges |

---

### 🔍 **GraphAnalyzer** — Analyze Graph Topology

`langflow_viz.graph.analyzer`

| Method | Description |
| --- | --- |
| `summary()` | Returns node count, edge count, cycle detection, dead ends, and longest path |
| `has_cycles()` | Detect if graph contains cycles |
| `find_dead_ends()` | Identify nodes with no outgoing connections |
| `longest_path_length()` | Compute the longest directed path length |

### Shortcut:

```python
from langflow_viz import analyze_graph
report = analyze_graph(nodes, edges)

```

---

### 🎨 **Visualizer** — Create Beautiful Diagrams

`langflow_viz.visualizer.visualizer`

| Method | Description |
| --- | --- |
| `build_graph()` | Builds internal Graphviz structure |
| `render_all()` | Exports SVG, PNG, Mermaid, and HTML files |
| `to_mermaid(nodes, edges)` | Generates Mermaid diagram text |
| `to_svg()` | Exports as SVG file |
| `to_html(mermaid_text)` | Creates interactive HTML preview |

**Constructor:**

```python
Visualizer(name: str, nodes: List[str], edges: List[Tuple[str, str]], conditional_edges: Optional[Set[Tuple[str, str]]] = None)

```

---

### 📤 **Exporter** — Format Conversion Layer

`langflow_viz.visualizer.exporter`

| Method | Description |
| --- | --- |
| `to_mermaid(nodes, edges, dashed_edges)` | Convert to Mermaid syntax |
| `to_svg()` | Export to SVG via Graphviz |
| `to_png()` | Export to PNG |
| `to_html(mermaid_text)` | Generate interactive HTML view |

---

### 🖌 **STYLE** — Customize Visuals

`langflow_viz.visualizer.style`

```python
from langflow_viz.visualizer import STYLE

STYLE["node"]["fillcolor"] = "#E8DAEF"
STYLE["edge"]["color"] = "#8E44AD"

```

---

## 🧪 Testing

Test the library locally using:

```bash
python -m test_demo

```

Expected Output:

```
📊 Graph Analysis: {'nodes': 5, 'edges': 4, 'has_cycles': False, 'dead_ends': ['finish'], 'longest_path': 4}
✅ SVG saved at: outputs/LangFlowViz_Test.svg
✅ Mermaid saved at: outputs/LangFlowViz_Test.mmd

```

---

## 🤝 Contributing

Contributions are welcome!

To set up your development environment:

```bash
git clone https://github.com/yourusername/langflow-viz.git
cd langflow-viz
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"

```

### 🧩 Run Tests

```bash
pytest

```

### 🧱 Submit a Pull Request

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new visualization option'`)
4. Push and open a Pull Request

---

## 📘 Documentation

Comprehensive developer documentation is coming soon at:

👉 https://langflow-viz.readthedocs.io

---

## 🧾 License

Licensed under the **MIT License** © 2025

Developed and maintained by the LangFlow-Viz Team.

---

## 💬 Community

Join the discussion, share workflows, and suggest improvements:

📢 GitHub Discussions → https://github.com/Sarjak369/langflow-viz/discussions


---

## 🌟 Why LangFlow-Viz?

LangFlow-Viz helps developers, researchers, and AI engineers **visualize and analyze workflow graphs** effortlessly.

It’s built for clarity, precision, and speed — designed to turn your logical pipelines into beautiful, meaningful diagrams.

## 🪶 Attribution

All design, icons, and visual elements are purely for **illustrative and educational purposes**.

LangFlow-Viz is open-source and welcomes contributions, improvements, and feature requests from the community.

That’s it — happy visualizing! ✨

