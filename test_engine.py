import vertexai
from vertexai.agent_engines import AgentEngine

# Initialise Vertex AI
vertexai.init(
    project="agent-deployment-test",
    location="us-central1"
)

# Reference your deployed AgentEngine
engine = AgentEngine.from_name(
    name="projects/487857840636/locations/us-central1/reasoningEngines/4588754603918491648"
)

# Run a quick test
response = engine.run(input="Hello, how are you?")
print(response)
