from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents import LlmAgent
from omikuji_agent.agents.die_agent import die_agent
from omikuji_agent.agents.omikuji_agent import omikuji_agent

root_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[die_agent, omikuji_agent],
)
