from langchain_groq import ChatGroq
from config.prompts import PLAINTIFF_PROMPT
from config.settings import GROQ_API_KEY, LLAMA_MODEL
from agents.base_agent import CourtroomAgent

def get_plaintiff_agent():
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=LLAMA_MODEL)
    return CourtroomAgent(llm, PLAINTIFF_PROMPT, "Plaintiff")
