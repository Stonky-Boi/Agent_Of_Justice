from langchain_groq import ChatGroq
from agents.base_agent import CourtroomAgent
from config.settings import GROQ_API_KEY, LLAMA_MODEL

WITNESS_PROMPT_TEMPLATE = """
You are witness {name}. You have been called to testify in this case.
Your testimony: {testimony}
Respond truthfully to questions from lawyers, and reference the case context and history.
"""

def create_witness_agent(name, testimony):
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=LLAMA_MODEL)
    prompt = WITNESS_PROMPT_TEMPLATE.format(name=name, testimony=testimony)
    return CourtroomAgent(llm, prompt, f"Witness: {name}")
