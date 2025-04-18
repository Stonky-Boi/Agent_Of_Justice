from langchain_community.chat_models import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from config.prompts import JUDGE_PROMPT
from config.settings import GROQ_API_KEY, LLAMA_MODEL

def get_judge_agent():
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=LLAMA_MODEL)
    prompt = PromptTemplate.from_template(JUDGE_PROMPT + "\nCase:\n{case_summary}")
    return LLMChain(llm=llm, prompt=prompt)
