from graph.state_graph import StateGraph
from visualizer.visualizer import Visualizer
from graph.analyzer import GraphAnalyzer


def build_linear_workflow():
    g = StateGraph()
    g.add_node("n1")
    g.add_node("n2")
    g.add_node("n3")
    g.add_edge("START", "n1")
    g.add_edge("n1", "n2")
    g.add_edge("n2", "n3")
    g.add_edge("n3", "END")
    return g


if __name__ == "__main__":
    wf = build_linear_workflow()
    viz = Visualizer(name="LinearWorkflow", nodes=wf.nodes, edges=wf.edges)
    viz.render_all()

    analyzer = GraphAnalyzer(wf.nodes, wf.edges)
    print("✅ Linear Workflow Analysis:", analyzer.summary())
