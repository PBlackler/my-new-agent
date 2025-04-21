import os
import json
from flask import Flask, request, jsonify, send_from_directory

# Toggle between remote Vertex AI and local stub
USE_REMOTE = os.environ.get("USE_REMOTE", "false").lower() == "true"

if USE_REMOTE:
    from vertexai import agent_engines, init
    init(project="agent-deployment-test", location="us-central1")
    agent = agent_engines.get(
        "projects/487857840636/locations/us-central1/reasoningEngines/4588754603918491648"
    )
else:
    from agent import MyAgent
    agent = MyAgent(name="local_stub_agent")

# Serve both API and React UI from one Flask app
# static_folder points at app/static, which now contains index.html + /static/
app = Flask(__name__, static_folder="static")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    query = data.get("query")
    if not query:
        return jsonify(error="Missing 'query'"), 400

    try:
        if USE_REMOTE:
            if hasattr(agent, "stream_query"):
                events = agent.stream_query(message=query, user_id="flask-user")
            else:
                events = agent.streaming_agent_run_with_events(
                    request_json=json.dumps({"message": query, "user_id": "flask-user"})
                )
        else:
            events = agent.streaming_agent_run_with_events(
                input={"query": query, "user_id": "flask-user"}
            )

        reply = "".join(
            part.get("text", "")
            for ev in events
            for part in ev.get("content", {}).get("parts", [])
        )
        return jsonify(response=reply)

    except Exception as e:
        app.logger.error("Chat error: %s", e)
        return jsonify(error=str(e)), 500

# Catch‑all to serve your React app from app/static/index.html
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    static_dir = os.path.join(app.root_path, "static")
    # if the requested file exists under app/static, serve it
    if path and os.path.exists(os.path.join(static_dir, path)):
        return send_from_directory(static_dir, path)
    # otherwise serve index.html
    return send_from_directory(static_dir, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
