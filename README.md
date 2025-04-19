# Cynaptics Club Inductions 2025 – Agent of Justice

This repository contains our work for the Cynaptics Club inductions at IIT Indore. The task, which we have worked on and describe below, demonstrates our approach to advanced GenAI, LLM engineering, and multi-agent systems for simulating realistic courtroom trials.

---

## Overview

**Agent of Justice** is a modular, multi-agent courtroom simulation platform powered by Large Language Models (LLMs) and **Retrieval-Augmented Generation (RAG)**. The challenge: simulate a full trial—using real Indian Supreme Court judgments as case data—where LLM agents take on roles such as Judge, Lawyers, Plaintiff, Defendant, Witnesses, and Jury, and interact through explicit trial phases.

- **Prompt Engineering:** Each agent uses role-specific, context-rich prompts to ensure realistic, fact-grounded behavior.
- **Multi-Agent System:** Agents interact through a shared trial state, building on each other's arguments and referencing only the provided case facts.
- **Dynamic Phases:** The trial is modeled in explicit, realistic phases (openings, arguments, witness testimony, closings, verdict).
- **Case Grounding:** Simulations are based on real Indian Supreme Court cases, summarized for LLM input.
- **RAG Integration:** Every agent and phase is grounded in actual Indian law, statutes, and landmark judgments via retrieval from a curated legal knowledge base.
- **Progress Tracking:** Progress bars show simulation status for each case and phase.
- **Token Optimization:** Summaries and context trimming prevent LLM token overflows and API errors.

---

## Features

- **LLM Agents:** Modular agents for Judge, Prosecution, Defense, Plaintiff, Defendant, dynamic Witnesses, and Jury.
- **Case Summarization:** Each case is summarized via LLM to provide concise, relevant context.
- **Explicit Trial Phases:** Simulation follows Opening Statements, Argumentation, Witness Testimony, Closing Arguments, Jury Deliberation, and Judge's Ruling.
- **Dynamic Witnesses:** Witness agents are created on-the-fly with custom testimony per case.
- **Progress Bars:** Visual feedback for case and phase progress using `tqdm`.
- **Strict Fact Adherence:** System prompts, summaries, and RAG context ensure agents do not hallucinate facts outside the summary or legal corpus.
- **RAG-Powered Legal Reasoning:** Agents retrieve and cite relevant Indian statutes, constitutional articles, and precedent from a vectorized legal knowledge base, ensuring outputs are grounded in authoritative legal sources and not just LLM memory.

---

## Retrieval-Augmented Generation (RAG) in Legal Simulation

RAG enhances LLMs by integrating a vectorized legal knowledge base (statutes, codes, judgments, glossary) into every agent’s prompt. For each phase:
- The system retrieves the most relevant legal provisions and precedents using vector search (FAISS + Gemini embeddings).
- The retrieved legal context is injected into the agent’s prompt, so arguments, questions, and rulings are grounded in real law and not just LLM “imagination.”
- This approach greatly reduces hallucinations, increases legal accuracy, and enables agents to cite and reason with actual statutes and case law.

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Stonky-Boi/Cynaptics_Inductions_2025_2.git
cd Cynaptics_Inductions_2025_2
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

### 4. Build the Legal Knowledge Base (RAG)

- Place all legal documents (Constitution, IPC, CrPC, Evidence Act, Arbitration Act, landmark judgments, glossary, etc.) in the `legal_knowledge/` directory as `.txt` files.
- Build the vectorstore for retrieval:

```bash
python rag_legal.py
```

### 5. Configure Environment

- Set your API keys in a `.env` file:
  ```
  GOOGLE_API_KEY=your_gemini_api_key
  ```

---

## Usage

### Run the Courtroom Simulation

```bash
python main.py
```

- The simulation will loop through all cases in `data/summary.csv`, running a full trial for each.
- Progress bars show the status for each case and phase.
- At the end of each case, the full courtroom transcript and the judge's verdict are printed.
- **Every agent and phase is now legally grounded via RAG.**

---

## File Structure

| File/Folder              | Purpose                                                      |
|--------------------------|--------------------------------------------------------------|
| `main.py`                | Main script: runs the trial simulation for all cases         |
| `summarize.py`           | Summarizes each judgment for LLM input                       |
| `rag_legal.py`           | Builds/loads the FAISS vectorstore for RAG                   |
| `legal_knowledge/`       | Legal text corpus: constitution, codes, case law, glossary   |
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
- **Dynamic Trial Flow:** Modify `main.py` to change the order or logic of trial phases.
- **Custom Witnesses:** Adjust the witness list in `main.py` per case for greater realism.
- **Prompt Tuning:** Edit `prompts.py` to further refine agent behavior and fact adherence.
- **Expand Legal Knowledge:** Add more statutes, case law, or proprietary legal documents to `legal_knowledge/` and rebuild the vectorstore for richer RAG.

---

## Troubleshooting

- **Token Limit Errors:** If you see 413 errors, ensure your summaries are concise and context trimming is enabled.
- **API Connection Errors:** If Gemini API is unreachable, check your network and API key.
- **RAG Not Grounding Output:** Ensure your legal knowledge base is comprehensive and your prompts instruct agents to use both the summary and legal references.
- **KeyError for `legal_context`:** Always include `legal_context` (even if empty) in your agent context.

---

## Why RAG Matters for Legal AI

Retrieval-Augmented Generation (RAG) is now a best practice in legal GenAI, as it grounds LLM outputs in authoritative sources, reduces hallucinations, and enables accurate citation of statutes and precedent. This approach is increasingly used in legal research, drafting, and simulation tools, and is a core part of this project’s design.

---
