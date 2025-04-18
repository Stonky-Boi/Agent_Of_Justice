from langchain_groq import ChatGroq
from config.prompts import JUDGE_PROMPT
from config.settings import GROQ_API_KEY, LLAMA_MODEL
from agents.base_agent import CourtroomAgent

def get_judge_agent():
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=LLAMA_MODEL)
    return CourtroomAgent(llm, JUDGE_PROMPT, "Judge")
