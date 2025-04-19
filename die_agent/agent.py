from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from omikuji_agent.tools.roll_die import roll_die

root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/mistral-small3.1"),
    name="dir_agent",
    description=("Agent that can roll a die."),
    instruction=("You can ask user to roll a die."),
    tools=[
        roll_die,
    ],
)
