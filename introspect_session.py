from vertexai import agent_engines, init

# Initialise
init(project="agent-deployment-test", location="us-central1")
agent = agent_engines.get(
    "projects/487857840636/locations/us-central1/reasoningEngines/4588754603918491648"
)

# Create a session
session = agent.create_session(user_id="peter")

# Inspect it
print("Raw session object:", session)
print("Keys:", session.keys())
