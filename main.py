from typing import TypedDict, Optional
from agents import judge, prosecution_lawyer, defense_lawyer, plaintiff, defendant, witness
from config.case_loader import load_case_data
from tqdm import tqdm
import time

class TrialState(TypedDict):
    case_summary: str
    history: str
    phase: str
    verdict: Optional[str]

def trim_history(history, max_chars=4000):
    return history[-max_chars:]

def run_phase(agent, role, phase, state, extra_context=None, pbar=None):
    if pbar:
        pbar.set_description(f"Processing: {role} - {phase}")
    
    state["phase"] = phase
    context = {
        "case_summary": state["case_summary"],
        "history": trim_history(state["history"]),
        "phase": phase,
        "extra": ""
    }
    if extra_context:
        context.update(extra_context)
    
    # Make API call to the agent
    response = agent.respond(context)
    
    # Update state with response
    state["history"] += f"\n[{role} - {phase}]: {response.content.strip()}\n"
    
    # Update progress bar
    if pbar:
        pbar.update(1)
    
    return state

def main():
    cases = load_case_data("data/summary.csv")
    
    # Main progress bar for all cases
    with tqdm(total=len(cases), desc="Cases", position=0) as case_pbar:
        for idx, case in enumerate(cases):
            print(f"\n\n===== Simulating Case {idx+1}/{len(cases)} =====\n")
            print(f"Summary: {case['summary'][:100]}...")
            
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

            # Example dynamic witnesses
            witnesses = [
                {"name": "Jane Smith", "testimony": "I am a witness to the contract formation and can attest to the negotiation process."},
                {"name": "John Doe", "testimony": "I observed the deposit clause being discussed and can confirm the parties' understanding."}
            ]

            # Calculate total phases for this case
            total_phases = 2 + 2 + len(witnesses) + 2 + 1  # Opening + Argumentation + Witnesses + Closing + Ruling
            
            # Create a progress bar for this case's phases
            with tqdm(total=total_phases, desc=f"Case {idx+1} Phases", position=1, leave=False) as phase_pbar:
                # Opening Statements
                state = run_phase(prosecution_agent, "Prosecution", "Opening Statement", state, pbar=phase_pbar)
                state = run_phase(defense_agent, "Defense", "Opening Statement", state, pbar=phase_pbar)

                # Argumentation
                state = run_phase(prosecution_agent, "Prosecution", "Argumentation", state, pbar=phase_pbar)
                state = run_phase(defense_agent, "Defense", "Argumentation", state, pbar=phase_pbar)

                # Witnesses (dynamic)
                for w in witnesses:
                    witness_agent = witness.create_witness_agent(w["name"], w["testimony"])
                    extra = {"name": w["name"], "testimony": w["testimony"]}
                    state = run_phase(witness_agent, f"Witness {w['name']}", "Witness Testimony", state, 
                                     extra_context=extra, pbar=phase_pbar)

                # Closing Statements
                state = run_phase(prosecution_agent, "Prosecution", "Closing Statement", state, pbar=phase_pbar)
                state = run_phase(defense_agent, "Defense", "Closing Statement", state, pbar=phase_pbar)

                # Judge's Ruling
                state = run_phase(judge_agent, "Judge", "Judge Ruling", state, pbar=phase_pbar)
                
                # Extract judge's verdict
                state["verdict"] = state["history"].split("[Judge - Judge Ruling]:")[-1].strip()

            # Output transcript
            print("\n===== Courtroom Transcript =====\n")
            print(state["history"])
            print("\n===== Judge's Verdict =====\n")
            print(state["verdict"])
            
            # Update the case progress bar
            case_pbar.update(1)

if __name__ == "__main__":
    main()
