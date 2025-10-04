from typing import Iterable, Tuple, Set
from graphviz import Digraph
from visualizer.style import STYLE
from visualizer.exporter import Exporter
from graph.analyzer import GraphAnalyzer

Edge = Tuple[str, str]


class Visualizer:
    """Handles drawing and exporting of workflow graphs."""

    # <-- NEW param
    def __init__(self, name: str, nodes, edges, conditional_edges: Iterable[Edge] | None = None):
        self.name = name
        self.nodes = nodes
        self.edges = edges
        self.conditional_edges: Set[Edge] = set(
            conditional_edges or [])
        self.graph = Digraph(name, format="png")

    def build_graph(self):
        self.graph.attr(rankdir="TB", splines="spline")

        # Add nodes
        self.graph.node("START", **STYLE["start"])
        for n in self.nodes:
            self.graph.node(n, **STYLE["node"])
        self.graph.node("END", **STYLE["end"])

        for src, dst in self.edges:
            style = STYLE["edge_dashed"] if (
                src, dst) in self.conditional_edges else STYLE["edge"]
            self.graph.edge(src, dst, **style)

    def render_all(self):
        self.build_graph()
        exporter = Exporter(self.graph, self.name)
        exporter.to_png()
        exporter.to_svg()

        exporter.to_mermaid(self.nodes, self.edges,
                            dashed_edges=self.conditional_edges)
        with open(f"outputs/{self.name}.mmd") as f:
            mermaid_text = f.read()
        exporter.to_html(mermaid_text)

    def analyze(self):
        analyzer = GraphAnalyzer(self.nodes, self.edges)
        return analyzer.summary()
