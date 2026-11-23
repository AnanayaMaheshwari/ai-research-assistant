from strands import Agent
from agents.model import get_gemini_model

PROMPT = '''
You are a research planning specialist. Turn the user's research question into
a practical plan with: research objective, 5–7 numbered sub-questions, suggested
source types, scope boundaries, and likely limitations. Do not answer the
research questions yet. Be concise and specific.
'''

def create_planner_agent():
    return Agent(model=get_gemini_model(), system_prompt=PROMPT)
