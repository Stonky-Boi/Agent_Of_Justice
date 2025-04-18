# Cynaptics Club Inductions 2025 – Agent of Justice

This repository contains our work for the Cynaptics Club inductions at IIT Indore. The task, which we have worked on and describe below, demonstrates our approach to advanced GenAI, LLM engineering, and multi-agent systems for simulating realistic courtroom trials.

---

## Overview

**Agent of Justice** is a modular, multi-agent courtroom simulation platform powered by Large Language Models (LLMs). The challenge: simulate a full trial—using real Indian Supreme Court judgments as case data—where LLM agents take on roles such as Judge, Lawyers, Plaintiff, Defendant, and Witnesses, and interact through explicit trial phases.

- **Prompt Engineering:** Each agent uses role-specific, context-rich prompts to ensure realistic, fact-grounded behavior.
- **Multi-Agent System:** Agents interact through a shared trial state, building on each other's arguments and referencing only the provided case facts.
- **Dynamic Phases:** The trial is modeled in explicit, realistic phases (openings, arguments, witness testimony, closings, verdict).
- **Case Grounding:** Simulations are based on real Indian Supreme Court cases, summarized for LLM input.
- **Progress Tracking:** Progress bars show simulation status for each case and phase.
- **Token Optimization:** Summaries and context trimming prevent LLM token overflows and API errors.

---

## Features

- **LLM Agents:** Modular agents for Judge, Prosecution, Defense, Plaintiff, Defendant, and dynamic Witnesses.
- **Case Summarization:** Each case is summarized via LLM to provide concise, relevant context.
- **Explicit Trial Phases:** Simulation follows Opening Statements, Argumentation, Witness Testimony, Closing Statements, and Judge's Ruling.
- **Dynamic Witnesses:** Witness agents are created on-the-fly with custom testimony per case.
- **Progress Bars:** Visual feedback for case and phase progress using `tqdm`.
- **Strict Fact Adherence:** System prompts and context ensure agents do not hallucinate facts outside the summary.

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Stonky-Boi/Cynaptics-Inductions-2025-2.git
cd Cynaptics-Inductions-2025-2
```

### 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Prepare Data

- Place your raw judgments in `data/data.csv` (one full judgment per line).
- Run the summarization script to create concise, single-line summaries:

```bash
python summarize.py
```
- This will produce `data/summary.csv` with one summary per line (no header).

### 4. Configure Environment

- Set your Groq API key in a `.env` file:
  ```
  GROQ_API_KEY=your_actual_api_key
  ```

---

## Usage

### Run the Courtroom Simulation

```bash
python app.py
```

- The simulation will loop through all cases in `data/summary.csv`, running a full trial for each.
- Progress bars show the status for each case and phase.
- At the end of each case, the full courtroom transcript and the judge's verdict are printed.

---

## File Structure

| File/Folder              | Purpose                                                      |
|--------------------------|--------------------------------------------------------------|
| `app.py`                 | Main script: runs the trial simulation for all cases         |
| `summarize.py`           | Summarizes each judgment for LLM input                       |
| `config/case_loader.py`  | Loads case summaries for simulation                          |
| `config/prompts.py`      | Role-specific, context-rich prompt templates                 |
| `agents/`                | Modular agent definitions (Judge, Lawyers, Witness, etc.)    |
| `data/data.csv`          | Raw full-text judgments                                      |
| `data/summary.csv`       | LLM-generated, single-line summaries for each case           |
| `requirements.txt`       | Python dependencies                                          |
| `.env`                   | API keys and environment variables                           |

---

## Customization & Extensibility

- **Add More Agents:** Easily add new roles (e.g., Jury, Expert Witness) by extending the `agents/` folder.
- **Dynamic Trial Flow:** Modify `app.py` to change the order or logic of trial phases.
- **Custom Witnesses:** Adjust the witness list in `app.py` per case for greater realism.
- **Prompt Tuning:** Edit `prompts.py` to further refine agent behavior and fact adherence.

---

## Troubleshooting

- **Token Limit Errors:** If you see 413 errors, ensure your summaries are concise and context trimming is enabled.
- **Connection Errors:** If Groq API is unreachable, check your network and API key.
- **Hallucinated Facts:** Ensure your summaries are explicit and prompts instruct agents to use only the provided summary.
