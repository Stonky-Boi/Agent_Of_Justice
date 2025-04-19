# from langchain_groq import ChatGroq
# from config.settings import GROQ_API_KEY, LLAMA_MODEL
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GOOGLE_API_KEY
from agents.base_agent import CourtroomAgent
from config.prompts import WITNESS_PROMPT_TEMPLATE

def create_witness_agent(name, testimony):
    """
    Returns a CourtroomAgent for a witness.
    At runtime, context must include 'name' and 'testimony'.
    """
    # llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=LLAMA_MODEL)
    llm = ChatGoogleGenerativeAI(
        google_api_key=GOOGLE_API_KEY,
        model="gemini-2.0-flash-lite"  # or "models/gemini-pro" if needed
    )
    # We do NOT format the template here; let base_agent handle it at runtime
    return CourtroomAgent(llm, WITNESS_PROMPT_TEMPLATE, f"Witness: {name}")
