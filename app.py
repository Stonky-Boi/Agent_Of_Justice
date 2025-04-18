from typing import TypedDict, Optional
from agents import judge, prosecution_lawyer, defense_lawyer, plaintiff, defendant, witness
from config.case_loader import load_case_data

class TrialState(TypedDict):
    case_summary: str
    history: str
    phase: str
    verdict: Optional[str]

def trim_history(history, max_chars=4000):
    return history[-max_chars:]

def run_phase(agent, role, phase, state, extra_context=None):
    state["phase"] = phase
    context = {
        "case_summary": state["case_summary"],
        "history": trim_history(state["history"]),
        "phase": phase,
        "extra": ""
    }
    if extra_context:
        context.update(extra_context)
    response = agent.respond(context)
    state["history"] += f"\n[{role} - {phase}]: {response.content.strip()}\n"
    return state

def main():
    cases = load_case_data("data/summary.csv")
    for idx, case in enumerate(cases):
        print(f"\n\n===== Simulating Case {idx+1} =====\n")
        state: TrialState = {
            "case_summary": case["summary"],
            "history": "",
            "phase": "",
            "verdict": None
        }

        # Initialize agents
        plaintiff_agent = plaintiff.get_plaintiff_agent()
        defendant_agent = defendant.get_defendant_agent()
        prosecution_agent = prosecution_lawyer.get_prosecution_agent()
        defense_agent = defense_lawyer.get_defense_agent()
        judge_agent = judge.get_judge_agent()

        # Example dynamic witnesses (replace with actual witness data as needed)
        witnesses = [
            {"name": "Jane Smith", "testimony": "I am a witness to the contract formation and can attest to the negotiation process."},
            {"name": "John Doe", "testimony": "I observed the deposit clause being discussed and can confirm the parties' understanding."}
        ]

        # Opening Statements
        state = run_phase(prosecution_agent, "Prosecution", "Opening Statement", state)
        state = run_phase(defense_agent, "Defense", "Opening Statement", state)

        # Argumentation
        state = run_phase(prosecution_agent, "Prosecution", "Argumentation", state)
        state = run_phase(defense_agent, "Defense", "Argumentation", state)

        # Witnesses (dynamic)
        for w in witnesses:
            witness_agent = witness.create_witness_agent(w["name"], w["testimony"])
            extra = {"name": w["name"], "testimony": w["testimony"]}
            state = run_phase(witness_agent, f"Witness {w['name']}", "Witness Testimony", state, extra_context=extra)

        # Closing Statements
        state = run_phase(prosecution_agent, "Prosecution", "Closing Statement", state)
        state = run_phase(defense_agent, "Defense", "Closing Statement", state)

        # Judge's Ruling
        state = run_phase(judge_agent, "Judge", "Judge Ruling", state)
        # Extract judge's verdict (last judge ruling in history)
        state["verdict"] = state["history"].split("[Judge - Judge Ruling]:")[-1].strip()

        # Output richer transcript
        print("\n===== Courtroom Transcript =====\n")
        print(state["history"])
        print("\n===== Judge's Verdict =====\n")
        print(state["verdict"])

if __name__ == "__main__":
    main()
