from langgraph.graph import StateGraph
from agents import judge, prosecution_lawyer, defense_lawyer, plaintiff, defendant
from config.case_loader import load_case_data

def main():
    case_data = load_case_data("data/data.csv")

    graph = StateGraph()

    # Register agent nodes
    graph.add_node("plaintiff", plaintiff.get_plaintiff_agent())
    graph.add_node("defendant", defendant.get_defendant_agent())
    graph.add_node("prosecution", prosecution_lawyer.get_prosecution_agent())
    graph.add_node("defense", defense_lawyer.get_defense_agent())
    graph.add_node("judge", judge.get_judge_agent())

    # Set trial flow
    graph.set_entry_point("plaintiff")
    graph.add_edge("plaintiff", "defendant")
    graph.add_edge("defendant", "prosecution")
    graph.add_edge("prosecution", "defense")
    graph.add_edge("defense", "judge")

    executable = graph.compile()
    verdict = executable.invoke({"case_summary": case_data[0]["summary"]})  # Example

    print("\n🧑‍⚖️ Judge's Verdict:\n", verdict)

if __name__ == "__main__":
    main()
