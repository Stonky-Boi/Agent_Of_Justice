from langchain.prompts import PromptTemplate

class CourtroomAgent:
    def __init__(self, llm, base_prompt, role):
        self.llm = llm
        self.base_prompt = base_prompt
        self.role = role

    def build_prompt(self, context):
        # context: dict with keys like 'case_summary', 'history', 'phase', etc.
        prompt_text = self.base_prompt
        if 'phase' in context:
            prompt_text += f"\n[Phase: {context['phase']}]"
        if 'history' in context and context['history']:
            prompt_text += f"\n[History so far:]\n{context['history']}\n"
        prompt_text += f"\n[Case Summary:]\n{context['case_summary']}\n"
        if 'extra' in context and context['extra']:
            prompt_text += f"\n{context['extra']}\n"
        return PromptTemplate.from_template(prompt_text)

    def respond(self, context):
        prompt = self.build_prompt(context)
        return self.llm.invoke({"case_summary": context["case_summary"], "history": context.get("history", ""), "phase": context.get("phase", ""), "extra": context.get("extra", "")})
