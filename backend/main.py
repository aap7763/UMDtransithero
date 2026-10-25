# Connects everything: frontend -> ai.py -> transit.py -> ai.py -> frontend.
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, HTTPException

from ai import parse_question, write_answer
from transit import get_next_buses

app = Flask(__name__)
CORS(app)  # lets frontend/index.html call this server


@app.errorhandler(HTTPException)
def http_error(error):
    response = error.get_response()
    response.data = app.json.dumps({
        "error": {
            "code": error.name.upper().replace(" ", "_"),
            "message": error.description,
        }
    })
    response.content_type = "application/json"
    return response


@app.post("/api/v1/ask")
@app.post("/ask")
def ask():
    payload = request.get_json()
    if not isinstance(payload, dict):
        raise BadRequest("The request body must be a JSON object.")
    question = payload.get("question", "")
    if not isinstance(question, str):
        raise BadRequest("The question field must be a string.")
    parsed = parse_question(question)
    buses = get_next_buses(parsed["stop"])
    return jsonify({"answer": write_answer(buses), "buses": buses})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
