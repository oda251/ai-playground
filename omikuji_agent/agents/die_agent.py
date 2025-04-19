from google.adk.agents import LlmAgent
from omikuji_agent.tools.roll_die import roll_die


die_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="die_agent",
    description=("Agent that can roll a die."),
    instruction=("You can ask user to roll a die."),
    tools=[
        roll_die,
    ],
    output_key="die_result",
)
