#!/usr/bin/env python3
import sys
from vertexai import agent_engines, init
from app.agent import MyAgent

# 1. Initialise the Vertex AI SDK
init(project="agent-deployment-test", location="us-central1")

# 2. Create (deploy) your ADK agent
remote_agent = agent_engines.create(
    MyAgent(name="my_agent"),                              # your ADK Agent subclass
    requirements=["google-cloud-aiplatform[agent_engines,adk]"],  # include ADK deps
    display_name="my-new-agent"
)

# 3. Print out the fully qualified resource name
print("✅ Deployed as:", remote_agent.resource_name)
