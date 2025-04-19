from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from agent_die.tool.roll_die import roll_die
from agent_die.tool.check_prime import check_prime
from pydantic import BaseModel, Field

class CountryInput(BaseModel):
    country: str = Field(description="The name of the country.")

class CapitalOutput(BaseModel):
    capital: str = Field(description="The capital of the country.")

from datetime import datetime
from zoneinfo import ZoneInfo
def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (41 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }

# 時刻を取得する関数（ツール）を定義
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

root_agent = LlmAgent(
    model=LiteLlm(model="ollama_chat/mistral-small3.1"),
    name="weather_time_agent",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "I can answer your questions about the time and weather in a city."
    ),
    tools=[
        get_weather,
        get_current_time,
    ],
    input_schema=CountryInput,
    output_schema=CapitalOutput,
)
