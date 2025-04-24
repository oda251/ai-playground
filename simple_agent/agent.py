# @title Import necessary libraries
import os
import asyncio
from google.adk.agents import Agent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

def build_agent():
    """Builds the agent with the specified model and parameters."""
    return LlmAgent(
        model=LiteLlm(model="ollama_chat/gemma3"),
        name="simple_agent",
        description=("Agent that can roll a die."),
        instruction=("You can ask user to roll a die."),
    )

# @title Create Runner
def build_runnner(agent: Agent, app_name: str, session_service: InMemorySessionService):
    """Builds the runner with the specified agent and session service."""
    return Runner(agent=agent, app_name=app_name, session_service=session_service)

# @title Define Agent Interaction Function

from google.genai import types # For creating message Content/Parts

def main():
    APP_NAME = "simple_agent"
    USER_ID = "example_user"
    SESSION_ID = "example_session"
    agent = build_agent()
    session_service = InMemorySessionService()
    runner = build_runnner(agent, APP_NAME, session_service)
    # Create a session
    session = session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    query = "hello"
    request = types.Content(
        role='user',
        parts=[types.Part(text=query)]
    )
    response = runner.run(
        user_id=session.user_id,
        session_id=session.session_id,
        new_message=request
    )
    print("Response:", response[0])

if __name__ == "__main__":
    main()