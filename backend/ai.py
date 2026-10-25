"""
ai.py: the translator for UMDtransithero. Owned by Taha.

Turns a rider's typed sentence into structured data the transit backend can use,
and turns the backend's bus list back into a plain-English answer.

    parse_question("get me to the library before 5")
    -> {"intent": "directions", "origin": None, "destination": "library",
        "arrive_by": "17:00", "depart_at": None, "stop": "library"}

The AI only extracts what the user said. It never picks routes, stops, or buses;
that is the transit backend's job. Time math happens in Python, not in the model.
"""

import json
import os
import re
from datetime import datetime, timedelta

import ollama

# Swap models without touching code:  export TRANSIT_AI_MODEL=gemma4:e4b
MODEL = os.getenv("TRANSIT_AI_MODEL", "gemma3:4b")

INTENTS = ["directions", "next_bus", "route_info", "unknown"]

# The exact shape the model must return. Empty string means "not mentioned".
SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string", "enum": INTENTS},
        "origin": {"type": "string"},
        "destination": {"type": "string"},
        "arrive_by": {"type": "string"},
        "arrive_in_minutes": {"type": "integer"},
        "depart_at": {"type": "string"},
    },
    "required": [
        "intent",
        "origin",
        "destination",
        "arrive_by",
        "arrive_in_minutes",
        "depart_at",
    ],
}

SYSTEM_PROMPT = """You extract trip details from a bus rider's message near the
University of Maryland, College Park. Return JSON only.

Fields:
- intent: "directions" (wants to get somewhere), "next_bus" (asks when a bus
  comes), "route_info" (asks about a route), or "unknown".
- origin: where they start, only if stated. Otherwise "".
- destination: where they want to go, only if stated. Otherwise "".
- arrive_by: clock time they must arrive, 24-hour "HH:MM". Otherwise "".
- arrive_in_minutes: for relative times like "in 20 minutes", the number of
  minutes. Otherwise 0.
- depart_at: clock time they want to leave, 24-hour "HH:MM". Otherwise "".

Rules:
- Copy place names as the user wrote them. Do not guess or add places.
- Drop a leading "the" from place names.
- Never invent routes, stops, or bus numbers.
- Never do time arithmetic. For "in 20 minutes", set arrive_in_minutes to 20
  and leave arrive_by "".
- Only fill depart_at if the user says when they want to leave.
- "how do I get to X" is intent "directions", not "next_bus".
- "before 5" with no am/pm means the next 5 o'clock that makes sense today.
"""

TIME_PATTERN = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")

EMPTY_RESULT = {
    "intent": "unknown",
    "origin": None,
    "destination": None,
    "arrive_by": None,
    "depart_at": None,
}


def _clean_place(value) -> str | None:
    """Trim a place name and drop a leading 'the'."""
    text = str(value or "").strip()
    text = re.sub(r"^the\s+", "", text, flags=re.IGNORECASE)
    return text or None


def _clean(raw: dict) -> dict:
    """Validate the model's output so the backend always gets a safe shape."""
    result = dict(EMPTY_RESULT)

    intent = raw.get("intent", "unknown")
    result["intent"] = intent if intent in INTENTS else "unknown"

    result["origin"] = _clean_place(raw.get("origin"))
    result["destination"] = _clean_place(raw.get("destination"))

    for field in ("arrive_by", "depart_at"):
        value = str(raw.get(field, "")).strip()
        result[field] = value if TIME_PATTERN.match(value) else None

    # Relative time: Python does the math, never the model.
    minutes = raw.get("arrive_in_minutes", 0)
    if isinstance(minutes, int) and 0 < minutes <= 600 and not result["arrive_by"]:
        arrive = datetime.now() + timedelta(minutes=minutes)
        result["arrive_by"] = arrive.strftime("%H:%M")

    return result


def parse_request(sentence: str) -> dict:
    """Turn a rider's sentence into structured trip data."""
    sentence = (sentence or "").strip()
    if not sentence:
        return dict(EMPTY_RESULT)

    now = datetime.now().strftime("%A %H:%M")

    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": f"{SYSTEM_PROMPT}\nCurrent time: {now}"},
                {"role": "user", "content": sentence},
            ],
            format=SCHEMA,
            options={"temperature": 0},
        )
        raw = json.loads(response.message.content)
    except Exception as error:  # model not running, bad JSON, etc.
        print(f"[ai.py] parse failed: {error}")
        return dict(EMPTY_RESULT)

    return _clean(raw)


# ---- Functions the rest of the team's code calls ----


def parse_question(question):
    """Team interface: what main.py calls. Adds a 'stop' key for transit.py."""
    parsed = parse_request(question)
    parsed["stop"] = parsed["origin"] or parsed["destination"]
    return parsed


def write_answer(buses):
    """Turn a list of buses into a friendly sentence."""
    if not buses:
        return "No buses coming up right now."
    first = buses[0]
    return f"The next bus is the {first['route']}, arriving in {first['arrives_in_min']} minutes."


if __name__ == "__main__":
    tests = [
        "get me to the library before 5",
        "next bus to College Park Metro",
        "how do I get from Stamp to the Metro in 20 minutes",
        "does the 104 go to Hyattsville?",
        "I need to be at McKeldin by 9am",
        "hello",
    ]
    print(f"Model: {MODEL}  (now {datetime.now().strftime('%H:%M')})\n")
    for sentence in tests:
        print(f"> {sentence}")
        print(f"  {parse_question(sentence)}\n")

    print(write_answer([{"route": "104", "arrives_in_min": 6}]))
    print(write_answer([]))