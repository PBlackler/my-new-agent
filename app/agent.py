import os
from zoneinfo import ZoneInfo
import datetime
import google.auth
from google.adk.agents import Agent

# Set required environment variables
_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


def get_weather(query: str) -> str:
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        tz_identifier = "UTC"
    now = datetime.datetime.now(ZoneInfo(tz_identifier))
    return f"The current time is {now.strftime('%Y-%m-%d %H:%M:%S %Z')}."


class MyAgent(Agent):
    def streaming_agent_run_with_events(self, *, input: dict):
        message = input.get("query", "")
        user_id = input.get("user_id", "user")

        if "weather" in message.lower():
            reply = get_weather(message)
        elif "time" in message.lower():
            reply = get_current_time(message)
        else:
            reply = f"Hi {user_id}, you said: {message}"

        yield {
            "content": {
                "parts": [{"text": reply}],
                "role": "model"
            }
        }
