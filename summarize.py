import csv
import sys
from langchain_groq import ChatGroq
from config.settings import GROQ_API_KEY, LLAMA_MODEL

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
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=LLAMA_MODEL)

    with open(input_file, mode="r", encoding="utf-8") as infile, \
         open(output_file, mode="w", encoding="utf-8", newline='') as outfile:
        reader = csv.reader(infile)
        for row in reader:
            if not row or not row[0].strip():
                continue
            full_text = row[0].strip()
            summary = llm_summarize(full_text, llm)
            # Write only the summary, no header, no full text
            outfile.write(summary.replace('\r\n', '\n').replace('\r', '\n').strip() + "\n")
            print(f"Summarized case.")

if __name__ == "__main__":
    main()
