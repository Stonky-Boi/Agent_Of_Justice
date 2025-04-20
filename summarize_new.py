import csv
import sys
import time
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GOOGLE_API_KEY

csv.field_size_limit(sys.maxsize)

def clean_text(text):
    # Remove excessive whitespace and invisible characters
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\u200c', '').replace('\u200b', '')  # Remove zero-width spaces
    return text.strip()

def llm_summarize(text, llm):
    snippet = text[:2000]  # Use more context if needed, but keep it manageable
    prompt = (
        "Summarize the following Indian Supreme Court judgment in 5-6 sentences, "
        "focusing on the main dispute, legal question, and parties involved. "
        "Return only the summary as a single line, with no headings, no introductory text, and no blank lines. "
        "Do not include any line breaks in your response.\n\n"
        f"Judgment:\n{snippet}\n"
    )
    response = llm.invoke(prompt)
    # Remove any line breaks just in case
    summary = response.content.replace('\n', ' ').replace('\r', ' ').strip()
    # Collapse multiple spaces
    summary = re.sub(r'\s+', ' ', summary)
    return summary

def main():
    input_file = "data/cases.csv"
    output_file = "data/new_summary.csv"

    # === CONFIGURABLE PARAMETERS ===
    BATCH_SIZE = 100    # Number of cases to summarize per run
    START_INDEX = 0     # Index to start from (0-based)
    # ===============================

    llm = ChatGoogleGenerativeAI(
        google_api_key=GOOGLE_API_KEY,
        model="gemini-2.0-flash-lite"
    )

    # Read all input cases, skipping header if present
    with open(input_file, mode="r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        rows = list(reader)
        # Detect and skip header
        if rows and ("id" in rows[0] or "text" in rows[0]):
            all_rows = rows[1:]
        else:
            all_rows = rows

    # Only keep rows with non-empty text (assume text is in the last column)
    all_rows = [row for row in all_rows if row and row[-1].strip()]
    total_cases = len(all_rows)
    end_index = min(START_INDEX + BATCH_SIZE, total_cases)

    print(f"Summarizing cases {START_INDEX+1} to {end_index} of {total_cases}")

    # Open output file in append mode
    with open(output_file, mode="a", encoding="utf-8", newline='') as outfile:
        writer = csv.writer(outfile)
        for idx in range(START_INDEX, end_index):
            raw_text = all_rows[idx][-1].strip()
            clean_judgment = clean_text(raw_text)
            # Retry logic for rate limits or connection errors
            for attempt in range(5):
                try:
                    summary = llm_summarize(clean_judgment, llm)
                    writer.writerow([summary])
                    print(f"Summarized case {idx+1}/{total_cases}")
                    break
                except Exception as e:
                    print(f"Error on case {idx+1}: {e}")
                    if attempt < 4:
                        print("Waiting 60 seconds before retrying...")
                        time.sleep(60)
                    else:
                        print("Skipping this case after 5 attempts.")
                        writer.writerow(["[ERROR: Could not summarize]"])
            time.sleep(1)  # Optional: avoid rate limits

if __name__ == "__main__":
    main()
