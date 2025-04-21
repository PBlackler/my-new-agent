from vertexai import agent_engines, init

# 1. Initialise Vertex AI
init(
    project="agent-deployment-test",
    location="us-central1",
)

# 2. Get your deployed AgentEngine
engine_name = "projects/487857840636/locations/us-central1/reasoningEngines/4588754603918491648"
agent = agent_engines.get(engine_name)

print("Supported methods:", [op["name"] for op in agent.operation_schemas()])

# 3. Try stream_query, else fallback
print("\nStreaming response:")
events = list(agent.stream_query(message="Hello, how are you?", user_id="peter"))
if not events:
    print("→ no events from stream_query, falling back to streaming_agent_run_with_events …")
    events = list(agent.streaming_agent_run_with_events(message="Hello, how are you?", user_id="peter"))

# 4. Print out whatever we got
for ev in events:
    text = ev["content"]["parts"][0]["text"]
    print(text.strip())

if not events:
    print("\n⚠️  Still no events—something’s off with your agent’s method schema.")
