from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/gemma3"),
    name="chat_agent",
    description=(
        "chat agent that can chat with users and answer questions."
    ),
    instruction="""
        You are a chat agent that can answer questions and have conversations
        with users. You can also perform calculations and provide information
        about various topics.
    """,
)
