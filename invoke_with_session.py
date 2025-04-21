import time
from vertexai import agent_engines, init
from google.api_core.exceptions import ServiceUnavailable

# Initialise Vertex AI
init(project="agent-deployment-test", location="us-central1")
agent = agent_engines.get(
    "projects/487857840636/locations/us-central1/reasoningEngines/4588754603918491648"
)

# 1. Create a session and grab its ID
session = agent.create_session(user_id="peter")
session_id = session["id"]  # use 'id' per introspection

# 2. Try streaming with simple backoff
for attempt in range(3):
    try:
        events = list(agent.streaming_agent_run_with_events(
            message="Hello, how are you?",
            user_id="peter",
            session=session_id
        ))
        break
    except ServiceUnavailable:
        wait = 2 ** attempt
        print(f"Service unavailable, retrying in {wait}s…")
        time.sleep(wait)
else:
    raise RuntimeError("Engine still unavailable after retries")

# 3. Print the reply
print("Agent says:")
for ev in events:
    text = ev["content"]["parts"][0]["text"].strip()
    print(text)

# 4. Clean up
agent.delete_session(name=session_id)
