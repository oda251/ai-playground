from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService, Session

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

temp_service = InMemorySessionService()
example_session: Session = temp_service.create_session(
    app_name="my_app",
    user_id="example_user",
    state={"initial_key": "initial_value"} # State can be initialized
)
