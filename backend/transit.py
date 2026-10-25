# Bus logic — owned by the backend teammate.
# Reads the bus files in data/ and answers questions about routes and times.


def get_next_buses(stop_name):
    """Return upcoming buses for a stop. Fake data until the real logic is in."""
    return [
        {"route": "104", "stop": stop_name, "arrives_in_min": 5},
        {"route": "105", "stop": stop_name, "arrives_in_min": 12},
    ]
