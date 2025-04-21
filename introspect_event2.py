from vertexai import agent_engines, init

init(project="agent-deployment-test", location="us-central1")
agent = agent_engines.get(
    "projects/487857840636/locations/us-central1/reasoningEngines/4588754603918491648"
)

# Call with the required args
for event in agent.stream_query(
    message="Hello, how are you?",
    user_id="peter"
):
    print("Raw event dict:", event)
    print("Keys:", list(event.keys()))
    break
