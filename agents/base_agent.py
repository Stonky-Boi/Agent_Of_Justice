from langchain.prompts import PromptTemplate

class CourtroomAgent:
    def __init__(self, llm, base_prompt, role):
        self.llm = llm
        self.base_prompt = base_prompt
        self.role = role

    def build_prompt(self, context):
        # Ensure all keys used in prompt are present, provide empty string if missing
        prompt = self.base_prompt.format(
            case_summary=context.get("case_summary", ""),
            history=context.get("history", ""),
            phase=context.get("phase", ""),
            extra=context.get("extra", ""),
            name=context.get("name", ""),
            testimony=context.get("testimony", ""),
            legal_context=context.get("legal_context", "")  # <-- Fix: always provide this
        )
        return prompt

    def respond(self, context):
        prompt = self.build_prompt(context)
        return self.llm.invoke(prompt)
