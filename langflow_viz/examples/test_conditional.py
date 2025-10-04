from graph.state_graph import StateGraph
from visualizer.visualizer import Visualizer
from graph.analyzer import GraphAnalyzer


def build_conditional_workflow():
    g = StateGraph()
    g.add_node("extract_destination")
    g.add_node("check_weather")
    g.add_node("plan_indoor")
    g.add_node("plan_outdoor")
    g.add_node("final_response")

    g.add_edge("START", "extract_destination")
    g.add_edge("extract_destination", "check_weather")
    g.add_edge("check_weather", "plan_indoor",
               conditional=True)   # <-- dashed
    g.add_edge("check_weather", "plan_outdoor",
               conditional=True)   # <-- dashed
    g.add_edge("plan_indoor", "final_response")
    g.add_edge("plan_outdoor", "final_response")
    g.add_edge("final_response", "END")
    return g


if __name__ == "__main__":
    wf = build_conditional_workflow()
    viz = Visualizer(
        name="ConditionalWorkflow",
        nodes=wf.nodes,
        edges=wf.edges,
        conditional_edges=wf.conditional_edges,   # <-- pass dashed set
    )
    viz.render_all()

    analyzer = GraphAnalyzer(wf.nodes, wf.edges)
    print("✅ Conditional Workflow Analysis:", analyzer.summary())
