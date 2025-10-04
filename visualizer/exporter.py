# visualizer/exporter.py
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple, Set

from graphviz import Digraph

Edge = Tuple[str, str]


class Exporter:
    """Small helper to export Graphviz to PNG/SVG and Mermaid/HTML."""

    def __init__(self, graph: Digraph, name: str):
        self.graph = graph
        self.name = name
        Path("outputs").mkdir(parents=True, exist_ok=True)

    # ---------- Graphviz ----------
    def to_png(self) -> str:
        out = self.graph.render(
            filename=f"outputs/{self.name}", format="png", cleanup=True
        )
        return out

    def to_svg(self) -> str:
        out = self.graph.render(
            filename=f"outputs/{self.name}", format="svg", cleanup=True
        )
        return out

    # ---------- Mermaid ----------
    def to_mermaid(
        self,
        nodes: Iterable[str],
        edges: Iterable[Edge],
        dashed_edges: Iterable[Edge] | None = None,
    ) -> str:
        """Write a .mmd file. Edges listed in `dashed_edges` are dashed."""
        dashed: Set[Edge] = set(dashed_edges or [])

        parts: list[str] = [
            "flowchart TD",
            # classes
            "classDef start fill:#efe9ff,stroke:#c7b8ff,stroke-width:1.2px,color:#1f2937,rx:12,ry:12;",
            "classDef endClass fill:#efe9ff,stroke:#c7b8ff,stroke-width:1.2px,color:#1f2937,rx:12,ry:12;",
            "classDef node fill:#efe9ff,stroke:#c7b8ff,stroke-width:1.2px,color:#1f2937,rx:12,ry:12;",
            "classDef highlight fill:#efe9ff,stroke:#6d28d9,stroke-width:2px,color:#1f2937,rx:12,ry:12;",
        ]

        # nodes
        parts.append('n_START(["START"]):::start')
        for n in nodes:
            parts.append(f'n_{n}(["{n}"]):::node')
        parts.append('n_END(["END"]):::endClass')

        # edges
        edges_list = list(edges)
        for src, dst in edges_list:
            parts.append(f"    n_{src} --> n_{dst}")

        # style each link (dashed for conditionals)
        for i, (src, dst) in enumerate(edges_list):
            if (src, dst) in dashed:
                parts.append(
                    f"linkStyle {i} stroke:#6d28d9,stroke-width:3px,stroke-dasharray:6 4"
                )
            else:
                parts.append(f"linkStyle {i} stroke:#6d28d9,stroke-width:3px")

        text = "\n".join(parts)
        mmd_path = Path("outputs") / f"{self.name}.mmd"
        mmd_path.write_text(text, encoding="utf-8")
        return str(mmd_path)

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
