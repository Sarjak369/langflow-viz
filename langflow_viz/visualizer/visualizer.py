# langflow_viz/visualizer/visualizer.py
from typing import Iterable, Tuple, Set
from graphviz import Digraph
from langflow_viz.visualizer.style import STYLE
from langflow_viz.visualizer.exporter import Exporter
from langflow_viz.graph.analyzer import GraphAnalyzer

Edge = Tuple[str, str]


class Visualizer:
    """Handles drawing, exporting, and analysis of workflow graphs."""

    def __init__(
        self,
        name: str,
        nodes: Iterable[str],
        edges: Iterable[Edge],
        conditional_edges: Iterable[Edge] | None = None
    ):
        self.name = name
        self.nodes = list(nodes)
        self.edges = list(edges)
        self.conditional_edges: Set[Edge] = set(conditional_edges or [])
        self.graph = Digraph(name, format="png")

    # ------------------------------------------------------------------
    # Build Graphviz Diagram
    # ------------------------------------------------------------------
    def build_graph(self) -> None:
        """Constructs a Graphviz directed graph with styles."""
        self.graph.attr(**STYLE["graph"])

        # Add visual nodes
        self.graph.node("START", **STYLE["start"])
        for n in self.nodes:
            self.graph.node(n, **STYLE["node"])
        self.graph.node("END", **STYLE["end"])

        # Link START → first, last → END
        if self.nodes:
            self.graph.edge("START", self.nodes[0], **STYLE["edge"])
            self.graph.edge(self.nodes[-1], "END", **STYLE["edge"])

        # Add edges
        for src, dst in self.edges:
            style = STYLE["edge_dashed"] if (
                src, dst) in self.conditional_edges else STYLE["edge"]
            self.graph.edge(src, dst, **style)

    # ------------------------------------------------------------------
    # Export Methods
    # ------------------------------------------------------------------
    def render_all(self):
        # Step 1: Build Graphviz graph
        self.build_graph()

        # Step 2: Create exporter (new signature)
        exporter = Exporter(
            name=self.name,
            nodes=self.nodes,
            edges=self.edges,
            dashed_edges=self.conditional_edges
        )

        # Step 3: Export Graphviz-based formats
        exporter.to_svg()
        exporter.to_png()

        # Step 4: Export Mermaid & HTML
        exporter.to_mermaid()
        with open(f"outputs/{self.name}.mmd", "r", encoding="utf-8") as f:
            mermaid_text = f.read()
        exporter.to_html(mermaid_text)

        # Step 5: Print success summary
        print(f"\n✅ Visualization files generated for {self.name}:")
        print(f"- outputs/{self.name}.mmd")
        print(f"- outputs/{self.name}.svg")
        print(f"- outputs/{self.name}.png")
        print(f"- outputs/{self.name}.html")

    # ------------------------------------------------------------------
    # Graph Analysis
    # ------------------------------------------------------------------

    def analyze(self):
        """Return a structural summary using GraphAnalyzer."""
        analyzer = GraphAnalyzer(self.nodes, self.edges)
        return analyzer.summary()

    # ------------------------------------------------------------------
    # Debug/Utility
    # ------------------------------------------------------------------
    def __repr__(self):
        return f"<Visualizer name={self.name!r}, nodes={len(self.nodes)}, edges={len(self.edges)}>"
