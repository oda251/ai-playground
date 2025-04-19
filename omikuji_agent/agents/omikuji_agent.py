from google.adk.agents import LlmAgent
from omikuji_agent.tools.omikuji import omikuji

omikuji_agent = LlmAgent(
    # model=LiteLlm(model="ollama_chat/mistral-small3.1"),
    model="gemini-2.0-flash",
    name="omikuji_agent",
    description=("Agent that can give a omikuji result. "),
    instruction=(
        """
		You can draw an omikuji.
		Take the number proveded in the session state key 'die_result' as a parameter.
		"""
    ),
    tools=[
        omikuji,
    ],
)
