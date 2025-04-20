import time
from typing import TypedDict, Optional, List
from agents import judge, prosecution_lawyer, defense_lawyer, plaintiff, defendant, witness, jury
from config.case_loader import load_case_data
from tqdm import tqdm
import random
import csv
import os

from rag_legal_new import load_legal_vectorstore, retrieve_legal

class TrialState(TypedDict):
    case_summary: str
    history: str
    phase: str
    verdict: Optional[str]

def trim_history(history, max_chars=4000):
    return history[-max_chars:]

def run_phase(agent, role, phase, state, vectorstore=None, extra_context=None, pbar=None):
    if pbar:
        pbar.set_description(f"Processing: {role} - {phase}")
    state["phase"] = phase
    legal_context = ""
    if vectorstore is not None:
        query = f"{state['case_summary']} {phase} {role}"
        legal_context = retrieve_legal(query, vectorstore, k=3)
    context = {
        "case_summary": state["case_summary"],
        "history": trim_history(state["history"]),
        "phase": phase,
        "legal_context": legal_context,
        "extra": ""
    }
    if extra_context:
        context.update(extra_context)
    response = agent.respond(context)
    response_text = response.content.strip()
    state["history"] += f"\n[{role} - {phase}]: {response_text}\n"
    if pbar:
        pbar.update(1)
    return state

def generate_dynamic_witnesses(case_summary, num=2):
    names = [
        "Alex Patel", "Priya Singh", "Rohan Sharma", "Fatima Khan",
        "Jane Smith", "John Doe", "Sara Ali", "Vikram Mehta"
    ]
    random.shuffle(names)
    return [
        {
            "name": names[i],
            "testimony": f"This is the testimony of {names[i]} regarding the case: {case_summary[:60]}..."
        }
        for i in range(num)
    ]

def run_single_interrogation(lawyer_agent, witness_agent, lawyer_role, witness_role, state, phase, vectorstore, pbar=None):
    state["phase"] = phase
    legal_context = retrieve_legal(f"{state['case_summary']} {phase} {lawyer_role}", vectorstore, k=2)
    lawyer_context = {
        "case_summary": state["case_summary"],
        "history": trim_history(state["history"]),
        "phase": phase,
        "legal_context": legal_context,
        "extra": f"You are {lawyer_role}. Ask the most important question(s) for this phase to {witness_role}. Output all questions in a single block."
    }
    lawyer_q = lawyer_agent.respond(lawyer_context).content.strip()
    state["history"] += f"\n[{lawyer_role} - {phase}]: {lawyer_q}\n"
    if pbar:
        pbar.update(0.5)

    legal_context = retrieve_legal(f"{state['case_summary']} {phase} {witness_role}", vectorstore, k=2)
    witness_context = {
        "case_summary": state["case_summary"],
        "history": trim_history(state["history"]),
        "phase": phase,
        "legal_context": legal_context,
        "extra": f"You are {witness_role}. Respond thoroughly and truthfully to all the questions just asked."
    }
    witness_a = witness_agent.respond(witness_context).content.strip()
    state["history"] += f"\n[{witness_role} - {phase}]: {witness_a}\n"
    if pbar:
        pbar.update(0.5)
    return state

def main():
    # ---- Load RAG vectorstore ----
    vectorstore = load_legal_vectorstore()

    # === CONFIGURABLE PARAMETERS ===
    START_INDEX = 0
    BATCH_SIZE = None  # Set to None to process all, or set to e.g. 50 for a batch
    # ===============================

    cases = load_case_data("data/new_summary.csv")
    total_cases = len(cases)
    end_index = total_cases if BATCH_SIZE is None else min(START_INDEX + BATCH_SIZE, total_cases)

    # Prepare results file for appending and check existing IDs
    results_file = "data/results.csv"
    existing_ids = set()
    if os.path.exists(results_file):
        with open(results_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row and row[0].isdigit():
                    existing_ids.add(int(row[0]))

    # If file doesn't exist, write header
    if not os.path.exists(results_file):
        with open(results_file, "w", encoding="utf-8", newline='') as f:
            f.write("ID,VERDICT\n")

    with tqdm(total=end_index-START_INDEX, desc="Cases", position=0) as case_pbar:
        for idx in range(START_INDEX, end_index):
            case = cases[idx]
            # Get ID (from your csv, should be int)
            case_id = int(case.get("id") or case.get("ID") or idx)
            if case_id in existing_ids:
                print(f"Skipping already processed case ID {case_id}")
                case_pbar.update(1)
                continue

            print(f"\n\n===== Simulating Case {idx+1}/{total_cases} (ID: {case_id}) =====\n")
            print(f"Summary: {case['summary'][:100]}...")

            state: TrialState = {
                "case_summary": case["summary"],
                "history": "",
                "phase": "",
                "verdict": None
            }

            plaintiff_agent = plaintiff.get_plaintiff_agent()
            defendant_agent = defendant.get_defendant_agent()
            prosecution_agent = prosecution_lawyer.get_prosecution_agent()
            defense_agent = defense_lawyer.get_defense_agent()
            judge_agent = judge.get_judge_agent()
            jury_agent = jury.get_jury_agent()

            plaintiff_witnesses = generate_dynamic_witnesses(case["summary"], num=2)
            defense_witnesses = generate_dynamic_witnesses(case["summary"], num=2)

            total_phases = (
                2 + 2 +
                len(plaintiff_witnesses) * 3 +
                len(defense_witnesses) * 3 +
                2 + 2 +
                2
            )
            with tqdm(total=total_phases, desc=f"Case {idx+1} Phases", position=1, leave=False) as phase_pbar:
                state = run_phase(plaintiff_agent, "Plaintiff", "Opening Statement", state, vectorstore, pbar=phase_pbar)
                state = run_phase(prosecution_agent, "Prosecution Lawyer", "Opening Statement", state, vectorstore, pbar=phase_pbar)
                state = run_phase(defendant_agent, "Defendant", "Opening Statement", state, vectorstore, pbar=phase_pbar)
                state = run_phase(defense_agent, "Defense Lawyer", "Opening Statement", state, vectorstore, pbar=phase_pbar)

                for w in plaintiff_witnesses:
                    witness_agent = witness.create_witness_agent(w["name"], w["testimony"])
                    state = run_single_interrogation(prosecution_agent, witness_agent, "Prosecution Lawyer", f"Witness {w['name']}", state, "Direct Examination", vectorstore, pbar=phase_pbar)
                    state = run_single_interrogation(defense_agent, witness_agent, "Defense Lawyer", f"Witness {w['name']}", state, "Cross Examination", vectorstore, pbar=phase_pbar)
                    state = run_single_interrogation(prosecution_agent, witness_agent, "Prosecution Lawyer", f"Witness {w['name']}", state, "Re-Direct Examination", vectorstore, pbar=phase_pbar)

                for w in defense_witnesses:
                    witness_agent = witness.create_witness_agent(w["name"], w["testimony"])
                    state = run_single_interrogation(defense_agent, witness_agent, "Defense Lawyer", f"Witness {w['name']}", state, "Direct Examination", vectorstore, pbar=phase_pbar)
                    state = run_single_interrogation(prosecution_agent, witness_agent, "Prosecution Lawyer", f"Witness {w['name']}", state, "Cross Examination", vectorstore, pbar=phase_pbar)
                    state = run_single_interrogation(defense_agent, witness_agent, "Defense Lawyer", f"Witness {w['name']}", state, "Re-Direct Examination", vectorstore, pbar=phase_pbar)

                state = run_phase(plaintiff_agent, "Plaintiff", "Closing Argument", state, vectorstore, pbar=phase_pbar)
                state = run_phase(prosecution_agent, "Prosecution Lawyer", "Closing Argument", state, vectorstore, pbar=phase_pbar)
                state = run_phase(defendant_agent, "Defendant", "Closing Argument", state, vectorstore, pbar=phase_pbar)
                state = run_phase(defense_agent, "Defense Lawyer", "Closing Argument", state, vectorstore, pbar=phase_pbar)

                state = run_phase(jury_agent, "Jury", "Jury Deliberation", state, vectorstore, pbar=phase_pbar)
                state = run_phase(judge_agent, "Judge", "Judge's Order", state, vectorstore, pbar=phase_pbar)
                state["verdict"] = state["history"].split("[Judge - Judge's Order]:")[-1].strip()

            print("\n===== Courtroom Transcript =====\n")
            print(state["history"])
            print("\n===== Judge's Final Order =====\n")
            print(state["verdict"])

            verdict_text = state["verdict"].lower()
            verdict = 1 if any(word in verdict_text for word in ["grant", "allowed", "accept", "favour"]) else 0

            # ---- Write result after each case ----
            with open(results_file, "a", encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([case_id, verdict])

            case_pbar.update(1)
            time.sleep(10)  # Pause between cases to avoid rate limit

if __name__ == "__main__":
    main()
