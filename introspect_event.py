from vertexai import agent_engines, init

init(project="agent-deployment-test", location="us-central1")
agent = agent_engines.get(
    "projects/487857840636/locations/us-central1/reasoningEngines/4588754603918491648"
)

# grab just the first event so we can inspect it
for event in agent.stream_query(input={"query": "Hello, how are you?"}):
    print("Raw event repr:", event)
    print("Available attributes:", dir(event))
    break
