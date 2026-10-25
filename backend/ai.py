# AI translator — owned by Taha.
# Turns a plain-English question into something transit.py understands,
# and turns transit.py's answer back into plain English.


def parse_question(question):
    """Pull the stop name out of the user's question. Fake version for now."""
    return {"stop": "Stamp Student Union"}


def write_answer(buses):
    """Turn a list of buses into a friendly sentence."""
    if not buses:
        return "No buses coming up right now."
    first = buses[0]
    return f"The next bus is the {first['route']}, arriving in {first['arrives_in_min']} minutes."
