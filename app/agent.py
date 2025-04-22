# app/agent.py

class MyAgent:
    def __init__(self, name):
        self.name = name

    def streaming_agent_run_with_events(self, *, input):
        """
        Stub agent: immediately echo back the query.
        Input is a dict: { "query": str, "user_id": str }
        """
        query = input.get("query", "")
        user  = input.get("user_id", "user")
        # yield exactly one event with our reply
        yield {
            "content": {
                "parts": [
                    { "text": f"Hi {user}, you said: {query}" }
                ],
                "role": "model"
            }
        }
