import os
import json
from flask import Flask, request, jsonify, send_from_directory

# Toggle between remote Vertex AI and local stub
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

app = Flask(
    __name__,
    static_folder="static/build",
    static_url_path=""
)

@app.route("/chat", methods=["POST"])
def chat():
    print("DEBUG: USE_REMOTE =", USE_REMOTE)

    data = request.get_json() or {}
    query = data.get("query")
    if not query:
        return jsonify(error="Missing 'query'"), 400

    try:
        reply = ""

        if USE_REMOTE:
            # Try streaming first
            if hasattr(agent, "stream_query"):
                events = list(agent.stream_query(message=query, user_id="flask-user"))
            else:
                events = list(agent.streaming_agent_run_with_events(
                    request_json=json.dumps({"message": query, "user_id": "flask-user"})
                ))
            print("RAW REMOTE EVENTS (stream):", events)

            if not events:
                # Fallback to a single-shot call
                print("FALLBACK: calling agent.run()")
                resp = agent.run(message=query, user_id="flask-user")
                # resp may be a simple object or have .text
                text = getattr(resp, "text", None) or str(resp)
                reply = text
                print("FALLBACK REPLY:", repr(reply))
            else:
                # Assemble from streamed events
                reply = "".join(
                    part.get("text", "")
                    for ev in events
                    for part in ev.get("content", {}).get("parts", [])
                )

        else:
            events = list(agent.streaming_agent_run_with_events(
                input={"query": query, "user_id": "flask-user"}
            ))
            print("RAW STUB EVENTS:", events)
            reply = "".join(
                part.get("text", "")
                for ev in events
                for part in ev.get("content", {}).get("parts", [])
            )

        print("COMPILED REPLY:", repr(reply))
        return jsonify(response=reply)

    except Exception as e:
        app.logger.error("Chat error: %s", e)
        return jsonify(error=str(e)), 500

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    full_path = os.path.join(app.static_folder, path)
    if path and os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
