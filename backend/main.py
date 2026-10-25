# Connects everything: frontend -> ai.py -> transit.py -> ai.py -> frontend.
from flask import Flask, jsonify, request
from flask_cors import CORS

from ai import parse_question, write_answer
from transit import get_next_buses

app = Flask(__name__)
CORS(app)  # lets frontend/index.html call this server


@app.post("/ask")
def ask():
    question = request.json.get("question", "")
    parsed = parse_question(question)
    buses = get_next_buses(parsed["stop"])
    return jsonify({"answer": write_answer(buses), "buses": buses})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
