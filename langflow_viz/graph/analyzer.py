from typing import List, Tuple, Dict
from collections import defaultdict, deque


class GraphAnalyzer:
    """Analyzes the properties of a workflow graph."""

    def __init__(self, nodes: List[str], edges: List[Tuple[str, str]]):
        self.nodes = nodes
        self.edges = edges
        self.adj = defaultdict(list)
        for u, v in edges:
            self.adj[u].append(v)

    def has_cycles(self) -> bool:
        visited = set()
        rec_stack = set()

        def dfs(v):
            visited.add(v)
            rec_stack.add(v)
            for neigh in self.adj[v]:
                if neigh not in visited and dfs(neigh):
                    return True
                elif neigh in rec_stack:
                    return True
            rec_stack.remove(v)
            return False

        return any(dfs(node) for node in self.nodes if node not in visited)

    def find_dead_ends(self) -> List[str]:
        return [n for n in self.nodes if n not in [src for src, _ in self.edges]]

    def longest_path_length(self) -> int:
        indegree = {n: 0 for n in self.nodes}
        for u, v in self.edges:
            indegree[v] += 1

        queue = deque([n for n in self.nodes if indegree[n] == 0])
        dist = {n: 0 for n in self.nodes}

        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                dist[v] = max(dist[v], dist[u] + 1)
                indegree[v] -= 1
                if indegree[v] == 0:
                    queue.append(v)
        return max(dist.values()) if dist else 0

    def summary(self) -> Dict:
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "has_cycles": self.has_cycles(),
            "dead_ends": self.find_dead_ends(),
            "longest_path": self.longest_path_length(),
        }


def analyze_graph(nodes, edges):
    """Convenience function to get a graph summary directly."""
    ga = GraphAnalyzer(nodes, edges)
    return ga.summary()
