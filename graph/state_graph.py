from typing import List, Tuple, Set


class StateGraph:
    """Represents a simple directed workflow graph."""

    def __init__(self):
        self.nodes: List[str] = []
        self.edges: List[Tuple[str, str]] = []
        self.conditional_edges: Set[Tuple[str, str]] = set()

    def add_node(self, name: str):
        if name not in self.nodes:
            self.nodes.append(name)

    def add_edge(self, src: str, dst: str, conditional: bool = False):
        if src not in self.nodes:
            self.nodes.append(src)
        if dst not in self.nodes:
            self.nodes.append(dst)
        self.edges.append((src, dst))
        if conditional:
            self.conditional_edges.add((src, dst))

    def add_conditional_edge(self, src: str, dst: str) -> None:
        self.add_edge(src, dst, conditional=True)

    def get_nodes(self) -> List[str]:
        return self.nodes

    def get_edges(self) -> List[Tuple[str, str]]:
        return self.edges
