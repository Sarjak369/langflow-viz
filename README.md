# 🌀 LangFlow-Viz

**LangFlow-Viz** is a lightweight and elegant **workflow visualizer and analyzer** for LangGraph-like AI workflows.

It helps developers, researchers, and engineers **build, inspect, and export workflow graphs** for agentic or state-based systems with **zero configuration**.

> 🚀 Install in seconds
> 
> 
> `pip install langflow-viz`
> 

---

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

---

## 🧩 Overview

LangFlow-Viz brings clarity to complex agentic/state workflows:

- **Build** directed graphs programmatically (nodes, edges, conditions).
- **Visualize** instantly in **Mermaid**, **Graphviz** (PNG/SVG), or **interactive HTML**.
- **Analyze** structure for **cycles**, **dead-ends**, **path depth**, and more.
- **Export** visuals & artifacts for docs, dashboards, or CI reports.

---

## ✨ Features

- 🧠 **Graph Construction** – Create directed workflow graphs programmatically.
- 🎨 **Visual Rendering** – Export to **PNG**, **SVG**, **Mermaid**, or **interactive HTML**.
- 🔍 **Graph Analysis** – Detect **cycles**, find **dead-ends**, compute **depth** & **fan-out**.
- ⚙️ **Custom Styling** – Theme nodes/edges; highlight conditional branches & terminals.
- 📦 **Lightweight** – No heavy deps; only `graphviz` required for Graphviz exports.

---

## 📦 Installation

```bash
pip install langflow-viz
# Optional: if you plan to export PNG/SVG via Graphviz
# macOS: brew install graphviz
# Linux: sudo apt-get install graphviz
# Windows: choco install graphviz

```

---

## ⚡ Quickstart (30 seconds)

> The snippet below shows the typical flow: build → visualize → export.
> 
> 
> Adjust to your graph objects / data structures; see in-code docstrings for details.
> 

```python
# Quickstart example
# (Names here illustrate the intended flow; see docstrings in the package for exact APIs.)
from langflow_viz.visualizer import Visualizer
from langflow_viz.analyzer import analyze
from langflow_viz.exporter import save_mermaid, save_graphviz

# 1) Define a tiny workflow
nodes = ["start", "plan", "act", "reflect", "finish"]
edges = [
    ("start", "plan"),
    ("plan", "act"),
    ("act", "reflect"),
    ("reflect", "plan"),   # loop
    ("act", "finish"),
]

# 2) Visualize (Mermaid & Graphviz)
mermaid = Visualizer.to_mermaid(nodes, edges, title="LangFlow-Viz: Hello World")
gv      = Visualizer.to_graphviz(nodes, edges, engine="dot")  # PNG/SVG/PDF via Graphviz

# 3) Analyze
report = analyze(nodes, edges)  # e.g., {"cycles": [...], "dead_ends": [...], "depth": 4}
print(report)

# 4) Export
save_mermaid(mermaid, "workflow.html")    # interactive HTML
save_graphviz(gv, out="workflow.svg")     # vector graphics for docs

```

**Outputs you’ll get**

- `workflow.html` – shareable, interactive graph (Mermaid).
- `workflow.svg` – crisp vector export (Graphviz).
- Console report – structural insights (cycles, dead-ends, depth).

---

## 🛠 API at a Glance

> Full docstrings are included in the code; hover in your IDE or run help().
> 
- `Visualizer.to_mermaid(nodes, edges, title=None, theme="default")`
- `Visualizer.to_graphviz(nodes, edges, engine="dot", theme="light")`
- `analyzer.analyze(nodes, edges)` → `dict` report (cycles, dead-ends, depth, fan-out)
- `exporter.save_mermaid(mermaid_str, path)`
- `exporter.save_graphviz(graphviz_obj, out="workflow.svg" | "workflow.png")`

*Notes*

- **Nodes** may be strings or richer objects (id, label, type).
- **Edges** are tuples `(src, dst)` or `(src, dst, label/condition)`.

---

## 📚 Examples

- **Minimal** – 5 nodes + loop, export Mermaid + SVG.
- **Agentic** – plan → act → reflect loop with conditional exit to `finish`.
- **State Machine** – clear state labels + terminal highlighting.

> Add an examples/ folder with runnable scripts to help users (recommended).
> 

---

## ✅ Best Practices

- Keep labels **short & meaningful**.
- Use **terminal styling** for `finish`/`error` nodes.
- Keep the primary path visually **straight**, push alternates to branches.
- Export **SVG** for docs and **HTML** for interactive sharing.

---

## 🧪 Test locally

```bash
python - <<'PY'
from langflow_viz.visualizer import Visualizer
nodes = ["A","B","C"]; edges = [("A","B"), ("B","C")]
print(Visualizer.to_mermaid(nodes, edges))
PY

```

---

## 🚀 Using in CI

- Generate a Mermaid HTML and attach as a **build artifact**.
- Export Graphviz PNG/SVG and publish to **GitHub Pages** or docs site.
- Fail builds when analysis finds **bad smells** (e.g., cycles in forbidden areas).

---

## 🔗 Copy-Ready Badges (optional)

```markdown
[![PyPI](https://img.shields.io/pypi/v/langflow-viz.svg?label=PyPI&logo=pypi)](https://pypi.org/project/langflow-viz/)
![Python versions](https://img.shields.io/pypi/pyversions/langflow-viz.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

```

---

## 🧵 One-liner install (for your docs)

```bash
pip install langflow-viz

```

---

## 🤝 Contributing

PRs are welcome!

Good first issues: examples, docs, small features, or test coverage.

- **Dev setup**
    
    ```bash
    git clone https://github.com/Sarjak369/langflow-viz
    cd langflow-viz
    python -m venv .venv && source .venv/bin/activate
    pip install -e .[dev]
    
    ```
    
- **Before committing (nice to have)**
    
    Add `pre-commit`, black/ruff/isort, and run tests locally.
    

---

## 🗺 Roadmap

- [ ]  Node/edge **themes** & presets
- [ ]  Built-in **layout helpers**
- [ ]  **Jupyter** widget for interactive notebooks
- [ ]  Export **PNG/SVG** without system Graphviz (pure-Python fallback)

---

## 🧾 License

**MIT** – do anything with attribution & no warranty. See `LICENSE`.

---

## 🙋 FAQ

**Q: Do I need Graphviz installed?**

A: Only for Graphviz exports (PNG/SVG/PDF). Mermaid/HTML works without it.

**Q: Does it support conditional branches?**

A: Yes—edges can carry labels/conditions; styled distinctly in output.

**Q: Can I embed the graph in my docs site?**

A: Yes—use the Mermaid HTML export or SVG.

---

## 📣 Changelog

See [**Releases**](https://github.com/Sarjak369/langflow-viz/releases) for what’s new.

---

## ⭐ Why LangFlow-Viz?

- Clear mental model for complex agent pipelines
- High-quality exports for docs, PRDs, and dashboards
- Tiny API surface; ergonomic defaults; fast iterations

If this saves you time, please consider **starring the repo** — it helps others find it. 💙

---

### Attribution

Logo/emoji and brand elements are used for illustrative purposes only.

## 🧠 TL;DR

- Build a graph → `StateGraph()`
- Analyze → `analyze(graph)`
- Render/export → `render(graph)` → `.to_mermaid() | .to_svg() | .to_png() | .to_html()`

That’s it. Happy visualizing! ✨
