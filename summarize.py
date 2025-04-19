import csv
import sys
import time
# from langchain_groq import ChatGroq
# from config.settings import GROQ_API_KEY, LLAMA_MODEL
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GOOGLE_API_KEY

csv.field_size_limit(sys.maxsize)

def llm_summarize(text, llm):
    snippet = text[:1500]  # Only summarize a manageable chunk
    prompt = (
    "Summarize the following Indian Supreme Court judgment in 5-6 sentences, "
    "focusing on the main dispute, legal question, and parties involved. "
    "Return only the summary as a single line, with no headings, no introductory text, and no blank lines. "
    "Do not include any line breaks in your response.\n\n"
    f"Judgment:\n{snippet}\n"
    )
    response = llm.invoke(prompt)
    return response.content.strip()

def main():
    input_file = "data/data.csv"
    output_file = "data/summary.csv"

    # === CONFIGURABLE PARAMETERS ===
    BATCH_SIZE = 500    # Number of cases to summarize per run
    START_INDEX = 0    # Index to start from (0-based)
    # ===============================

    # llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=LLAMA_MODEL)
    llm = ChatGoogleGenerativeAI(
        google_api_key=GOOGLE_API_KEY,
        model="gemini-2.0-flash-lite"  # or "models/gemini-pro" if needed
    )

    # Read all input cases
    with open(input_file, mode="r", encoding="utf-8") as infile:
        all_rows = [row for row in csv.reader(infile) if row and row[0].strip()]

    total_cases = len(all_rows)
    end_index = min(START_INDEX + BATCH_SIZE, total_cases)

    print(f"Summarizing cases {START_INDEX+1} to {end_index} of {total_cases}")

    # Open output file in append mode
    with open(output_file, mode="a", encoding="utf-8", newline='') as outfile:
        for idx in range(START_INDEX, end_index):
            full_text = all_rows[idx][0].strip()
            # Retry logic for rate limits or connection errors
            for attempt in range(5):
                try:
                    summary = llm_summarize(full_text, llm)
                    outfile.write(summary + "\n")
                    print(f"Summarized case {idx+1}/{total_cases}")
                    break
                except Exception as e:
                    print(f"Error on case {idx+1}: {e}")
                    if attempt < 4:
                        print("Waiting 60 seconds before retrying...")
                        time.sleep(60)
                    else:
                        print("Skipping this case after 5 attempts.")
                        outfile.write("[ERROR: Could not summarize]\n")
            # Optional: sleep between requests to avoid rate limits
            time.sleep(1)

if __name__ == "__main__":
    main()
