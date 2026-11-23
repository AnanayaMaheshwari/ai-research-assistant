from strands import Agent
from agents.model import get_gemini_model

PROMPT = '''
You are a professional research report writer. Produce a clear Markdown report
with: title, executive summary, research question and scope, methodology,
key findings, detailed analysis, limitations, conclusion, and references.
Use only the supplied research and review notes. Attach source URLs to relevant
claims. Distinguish evidence from interpretation. Never invent facts, numbers,
quotes or references. If evidence is weak, say so explicitly.
'''

def create_report_writer_agent():
    return Agent(
        name="ReportWriter",
        model=get_gemini_model(),
        system_prompt=PROMPT,
        callback_handler=None
    )