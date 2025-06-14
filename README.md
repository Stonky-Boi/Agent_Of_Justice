# Agent of Justice
Cynaptics Club Inductions 2025
---
![GitHub Created At](https://img.shields.io/github/created-at/Stonky-Boi/Cynaptics_Inductions_2025_2)
![GitHub contributors](https://img.shields.io/github/contributors/Stonky-Boi/Cynaptics_Inductions_2025_2)
![GitHub License](https://img.shields.io/github/license/Stonky-Boi/Cynaptics_Inductions_2025_2)

This repository contains our work for the Cynaptics Club inductions at IIT Indore, **including both our original Agent of Justice simulation and our solution for the [Kaggle Agent of Justice contest](https://www.kaggle.com/competitions/agent-of-justice/overview)**.  
Our approach demonstrates advanced GenAI, LLM engineering, multi-agent orchestration, and RAG-powered legal reasoning for realistic courtroom trial simulation and binary verdict prediction.

---

## Overview

**Agent of Justice** is a modular, multi-agent courtroom simulation platform powered by Large Language Models (LLMs) and **Retrieval-Augmented Generation (RAG)**. The system simulates a full trial—using real Indian Supreme Court judgments as case data—where LLM agents take on roles such as Judge, Lawyers, Plaintiff, Defendant, Witnesses, and Jury, and interact through explicit trial phases.  
For the Kaggle contest, the system predicts binary verdicts (GRANTED/1 or DENIED/0) for each case in a test set.

---

## Features

- **LLM Agents:** Modular agents for Judge, Prosecution, Defense, Plaintiff, Defendant, dynamic Witnesses, and Jury.
- **Case Summarization:** Each case is summarized via LLM for concise, relevant context, with robust preprocessing and resumable batching.
- **Explicit Trial Phases:** Simulation follows Opening Statements, Argumentation, Witness Testimony, Closing Arguments, Jury Deliberation, and Judge's Ruling.
- **Dynamic Witnesses:** Witness agents are created on-the-fly with custom testimony per case.
- **Progress Bars:** Visual feedback for case and phase progress using `tqdm`.
- **Strict Fact Adherence:** Prompts, summaries, and RAG context ensure agents do not hallucinate facts outside the summary or legal corpus.
- **RAG-Powered Legal Reasoning:** Agents retrieve and cite relevant Indian statutes, constitutional articles, and precedent from a vectorized legal knowledge base, ensuring outputs are grounded in real law.
- **Resumable and Robust:** Both summarization and simulation scripts support batch processing and checkpointing, so you can resume from where you left off.
- **Contest Output:** For Kaggle, outputs are written as binary predictions (`1`/`0`) in the required `results.csv` format, with immediate file write after each case.
- **Highly Modular:** All agent logic, prompts, and knowledge base code is organized for easy extension and experimentation.

---

## Retrieval-Augmented Generation (RAG) in Legal Simulation

RAG enhances LLMs by integrating a vectorized legal knowledge base (statutes, codes, judgments, glossary) into every agent’s prompt. For each phase:
- The system retrieves the most relevant legal provisions and precedents using vector search (FAISS + Gemini embeddings).
- The retrieved legal context is injected into the agent’s prompt, so arguments, questions, and rulings are grounded in real law and not just LLM “imagination.”
- This approach greatly reduces hallucinations, increases legal accuracy, and enables agents to cite and reason with actual statutes and case law.

---

## Kaggle Contest Workflow

**Key modifications for the contest:**
- **Input:** `cases.csv` (from Kaggle) in the `data/` folder, with case IDs and raw text.
- **Output:** `results.csv` in the format `ID,VERDICT` (`1` for GRANTED, `0` for DENIED), written incrementally after each case.
- **Preprocessing:** Summarization and cleaning of `cases.csv` with whitespace/invisible character removal, batching, and time delays to avoid rate limits.
- **Optimized Knowledge Base:** `legal_knowledge_new/` directory with only the most relevant legal articles, acts, and judgments for the test set.
- **RAG:** `rag_legal_new.py` builds and loads the contest-specific vectorstore.
- **Simulation:** `main_new.py` runs the simulation, outputs verdict for each case, and supports resumability (via `START_INDEX` and batch size).
- **Parallelization:** Batches run on multiple machines/terminals with different API keys for faster throughput.
- **Robustness:** If the simulation crashes or hits rate limits, simply resume from the next case; all outputs are written incrementally.

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

#### For Original Simulation:
- Place your raw judgments in `data/data.csv` (one full judgment per line).
- Run the summarization script to create concise, single-line summaries:
    ```bash
    python summarize.py
    ```
- This will produce `data/summary.csv` with one summary per line (no header).

#### For Kaggle Contest:
- Place `cases.csv` (from Kaggle) in `data/`.
- Run the contest summarizer to preprocess and summarize cases:
    ```bash
    python summarize_new.py
    ```
- Output: `data/new_summary.csv` (summaries for contest cases).

### 4. Build the Legal Knowledge Base (RAG)

#### For Original Simulation:
- Place legal documents in `legal_knowledge/` as `.txt` files.
- Build the vectorstore:
    ```bash
    python rag_legal.py
    ```

#### For Kaggle Contest:
- Place optimized legal documents in `legal_knowledge_new/`.
- Build the contest vectorstore:
    ```bash
    python rag_legal_new.py
    ```

### 5. Configure Environment

- Set your API keys in a `.env` file:
  ```
  GOOGLE_API_KEY=your_gemini_api_key
  ```

---

## Usage

### Run the Original Courtroom Simulation

```bash
python main.py
```
- Simulates all cases in `data/summary.csv`.
- Progress bars show status for each case and phase.
- Full courtroom transcript and judge's verdict are printed.

### Run the Kaggle Contest Simulation

```bash
python main_new.py
```
- Simulates all cases in `data/new_summary.csv` (from `cases.csv`).
- Writes binary verdicts (`1`/`0`) to `results.csv` after each case in the format:
    ```
    ID,VERDICT
    2,1
    5,0
    6,0
    ```
- Supports `START_INDEX` and `BATCH_SIZE` for resumable, batch-wise processing.
- Add or adjust `time.sleep()` between cases to avoid API rate limits.

---

## File Structure

| File/Folder                   | Purpose                                                      |
|-------------------------------|--------------------------------------------------------------|
| `main.py`                     | Original simulation for all cases                            |
| `main_new.py`                 | Kaggle contest simulation (binary verdicts, resumable)       |
| `summarize.py`                | Summarizes original judgments for LLM input                  |
| `summarize_new.py`            | Summarizes contest cases with preprocessing and batching     |
| `rag_legal.py`                | Builds/loads original RAG vectorstore                        |
| `rag_legal_new.py`            | Builds/loads contest-specific RAG vectorstore                |
| `legal_knowledge/`            | Legal corpus for original simulation                         |
| `legal_knowledge_new/`        | Optimized legal corpus for contest/test set                  |
| `config/case_loader.py`       | Loads case summaries for simulation                          |
| `config/prompts.py`           | Role-specific, context-rich prompt templates                 |
| `agents/`                     | Modular agent definitions (Judge, Lawyers, Witness, etc.)    |
| `data/data.csv`               | Raw full-text judgments                                      |
| `data/summary.csv`            | Summaries for original simulation                            |
| `data/cases.csv`              | Kaggle contest input                                         |
| `data/new_summary.csv`        | Summaries for contest simulation                             |
| `results.csv`                 | Output for Kaggle contest submission                         |
| `requirements.txt`            | Python dependencies                                          |
| `.env`                        | API keys and environment variables                           |

---

## Contest-Specific Notes

- **Preprocessing:** Removes whitespace/invisible characters, summarizes in batches, and adds delays to avoid rate limits.
- **Resume Logic:** Both summarization and simulation scripts support `START_INDEX` and `BATCH_SIZE` for safe resumption.
- **Parallelization:** You can run multiple batches in parallel (e.g., on different laptops or terminals) with different API tokens.
- **Output:** Results are written incrementally after each case to avoid data loss on crash.

---

## Troubleshooting

- **Token Limit Errors:** Keep summaries concise and enable context trimming.
- **API Rate Limits:** Use `time.sleep()` between cases and batches; split workload across machines if needed.
- **Resume from Crash:** Set `START_INDEX` to the next case and rerun; script will skip already processed cases.
- **RAG Not Grounding Output:** Ensure your legal knowledge base is comprehensive and your prompts instruct agents to use both the summary and legal references.
- **KeyError for `legal_context`:** Always include `legal_context` (even if empty) in your agent context.

---

## Fun Facts & Team Notes

- When rate limits hit, we used multiple Gmail accounts for new API tokens.
- Ran batches on two laptops and two terminals on one MacBook for speed.
- If the simulation crashed, we simply resumed from the next case.
- Our simulation may not be perfect, but it’s robust, resilient, and “goated.”

---

## Why RAG Matters for Legal AI

Retrieval-Augmented Generation (RAG) is now a best practice in legal GenAI, as it grounds LLM outputs in authoritative sources, reduces hallucinations, and enables accurate citation of statutes and precedent. This approach is increasingly used in legal research, drafting, and simulation tools, and is a core part of this project’s design.

---

## Additional Notes from the Repo

- The `agents/` directory contains modular, extensible agent code for each courtroom role.
- The `config/prompts.py` file is highly customizable for prompt engineering and experimentation.
- The repo is organized for rapid experimentation: you can swap out LLM backends, RAG knowledge bases, or trial flows easily.
- All scripts are designed for robustness: errors are logged, outputs are checkpointed, and you can resume any process from where it crashed.

---

## Contributors

This project was developed by:

- **Alaya D'Cruz** ([alayacruz](https://github.com/alayacruz))
- **Arnav Kumar** ([Stonky-Boi](https://github.com/Stonky-Boi))
- **Prakrati Pawar** ([prakrati28](https://github.com/prakrati28))

---
