import time
from vertexai import agent_engines, init
from google.api_core.exceptions import ServiceUnavailable

init(project="agent-deployment-test", location="us-central1")
agent = agent_engines.get(
    "projects/487857840636/locations/us-central1/reasoningEngines/4588754603918491648"
)

# Create session once
session = agent.create_session(user_id="peter")
session_id = session["id"]

# Try up to 6 times, exponential backoff up to 32s
for attempt in range(6):
    try:
        events = list(agent.streaming_agent_run_with_events(
            message="Hello, how are you?",
            user_id="peter",
            session=session_id
        ))
        break
    except ServiceUnavailable as e:
        wait = min(2 ** attempt, 32)
        print(f"[Attempt {attempt+1}] Service unavailable, retrying in {wait}s…")
        time.sleep(wait)
else:
    raise RuntimeError("Engine still unavailable after extended retries")

print("Agent says:")
for ev in events:
    print(ev["content"]["parts"][0]["text"].strip())

agent.delete_session(name=session_id)
