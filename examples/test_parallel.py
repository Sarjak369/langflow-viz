from graph.state_graph import StateGraph
from visualizer.visualizer import Visualizer
from graph.analyzer import GraphAnalyzer


def build_parallel_workflow():
    g = StateGraph()
    g.add_node("extract_destination")
    g.add_node("weather_search")
    g.add_node("attractions_search")
    g.add_node("final_response")

    g.add_edge("START", "extract_destination")
    g.add_edge("extract_destination", "weather_search")
    g.add_edge("extract_destination", "attractions_search")
    g.add_edge("weather_search", "final_response")
    g.add_edge("attractions_search", "final_response")
    g.add_edge("final_response", "END")
    return g


if __name__ == "__main__":
    wf = build_parallel_workflow()
    viz = Visualizer(name="ParallelWorkflow", nodes=wf.nodes, edges=wf.edges)
    viz.render_all()

    analyzer = GraphAnalyzer(wf.nodes, wf.edges)
    print("✅ Parallel Workflow Analysis:", analyzer.summary())
