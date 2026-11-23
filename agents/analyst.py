from strands import Agent
from agents.model import get_gemini_model

PROMPT = '''
You are an evidence analyst. Analyze the research notes supplied to you.
Identify recurring themes, important findings, disagreements between sources,
quantitative evidence, implications and knowledge gaps. Do not introduce new
facts or sources. Tie each important finding to the supplied source URLs.
'''

def create_analyst_agent():
    return Agent(
        name="ResearchAnalyst",
        model=get_gemini_model(),
        system_prompt=PROMPT,
        callback_handler=None
    )