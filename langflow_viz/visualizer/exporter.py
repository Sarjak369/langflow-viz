# visualizer/exporter.py
from __future__ import annotations
from pathlib import Path
from typing import Iterable, Tuple, Set
from graphviz import Digraph

Edge = Tuple[str, str]


class Exporter:
    """Exports workflow graphs to Mermaid, SVG, PNG, and HTML formats."""

    def __init__(self, name: str, nodes: Iterable[str], edges: Iterable[Edge], dashed_edges: Iterable[Edge] | None = None):
        self.name = name
        self.nodes = list(nodes)
        self.edges = list(edges)
        self.dashed_edges = set(dashed_edges or [])
        Path("outputs").mkdir(parents=True, exist_ok=True)

    # ---------- Graphviz ----------
    def _build_graphviz(self) -> Digraph:
        dot = Digraph(name=self.name, format="png")
        dot.attr(rankdir="TB", bgcolor="white",
                 style="filled", color="transparent")
        dot.attr("node", shape="box", style="filled", fillcolor="#EFE9FF",
                 color="#6D28D9", fontname="Inter", fontsize="11")

        # Nodes
        dot.node("START", "START", fillcolor="#C7B8FF")
        for n in self.nodes:
            dot.node(n, n)
        dot.node("END", "END", fillcolor="#C7B8FF")

        # Edges
        edges_list = self.edges
        for src, dst in edges_list:
            style = "dashed" if (src, dst) in self.dashed_edges else "solid"
            dot.edge(src, dst, color="#6D28D9", penwidth="2", style=style)

        # Auto-connect START and END
        node_set = set(self.nodes)
        successors = {u for u, _ in edges_list}
        predecessors = {v for _, v in edges_list}
        roots = list(
            node_set - predecessors) or ([next(iter(node_set))] if node_set else [])
        sinks = list(
            node_set - successors) or ([list(node_set)[-1]] if node_set else [])

        for r in roots:
            dot.edge("START", r, color="#6D28D9", penwidth="2")
        for s in sinks:
            dot.edge(s, "END", color="#6D28D9", penwidth="2")

        return dot

    def to_png(self) -> str:
        dot = self._build_graphviz()
        out_path = Path("outputs") / f"{self.name}.png"
        dot.render(filename=str(out_path.with_suffix("")),
                   format="png", cleanup=True)
        return str(out_path)

    def to_svg(self) -> str:
        dot = self._build_graphviz()
        out_path = Path("outputs") / f"{self.name}.svg"
        dot.render(filename=str(out_path.with_suffix("")),
                   format="svg", cleanup=True)
        return str(out_path)

    # ---------- Mermaid ----------
    def to_mermaid(self) -> str:
        dashed = self.dashed_edges
        parts: list[str] = [
            "flowchart TD",
            "classDef start fill:#efe9ff,stroke:#c7b8ff,stroke-width:1.2px,color:#1f2937,rx:12,ry:12;",
            "classDef endClass fill:#efe9ff,stroke:#c7b8ff,stroke-width:1.2px,color:#1f2937,rx:12,ry:12;",
            "classDef node fill:#efe9ff,stroke:#c7b8ff,stroke-width:1.2px,color:#1f2937,rx:12,ry:12;",
            "classDef highlight fill:#efe9ff,stroke:#6d28d9,stroke-width:2px,color:#1f2937,rx:12,ry:12;",
        ]

        parts.append('n_START(["START"]):::start')
        for n in self.nodes:
            parts.append(f'n_{n}(["{n}"]):::node')
        parts.append('n_END(["END"]):::endClass')

        for i, (src, dst) in enumerate(self.edges):
            parts.append(f"n_{src} --> n_{dst}")
            if (src, dst) in dashed:
                parts.append(
                    f"linkStyle {i} stroke:#6d28d9,stroke-width:3px,stroke-dasharray:6 4")
            else:
                parts.append(f"linkStyle {i} stroke:#6d28d9,stroke-width:3px")

        node_set = set(self.nodes)
        successors = {u for u, _ in self.edges}
        predecessors = {v for _, v in self.edges}
        roots = list(
            node_set - predecessors) or ([next(iter(node_set))] if node_set else [])
        sinks = list(
            node_set - successors) or ([list(node_set)[-1]] if node_set else [])

        for r in roots:
            parts.append(f"n_START --> n_{r}")
        for s in sinks:
            parts.append(f"n_{s} --> n_END")

        text = "\n".join(parts)
        out_path = Path("outputs") / f"{self.name}.mmd"
        out_path.write_text(text, encoding="utf-8")
        return str(out_path)

    # ---------- HTML wrapper ----------
    def to_html(self, mermaid_text: str) -> str:
        html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{self.name}</title>
  <style>
    body {{ background: white; margin: 0; padding: 24px;
           font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({{ startOnLoad: true, theme: "default" }});</script>
</head>
<body>
<div class="mermaid">
{mermaid_text}
</div>
</body>
</html>"""
        out_path = Path("outputs") / f"{self.name}.html"
        out_path.write_text(html, encoding="utf-8")
        return str(out_path)
