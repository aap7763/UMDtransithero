# UMDtransithero

UMDtransithero is an app concept to help students and other newcomers get comfortable using public transit around the University of Maryland, College Park—with a focus on understanding local bus routes.

## The problem

Existing transit apps can show routes and arrivals, but it can still be hard to tell which direction to travel, which side of the street to wait on, or what to do once you're on the bus. UMDtransithero aims to make those details easier to understand, especially for people new to the area.

## Planned features

- **Wrong-way guard:** Enter a destination and get clear guidance near your stop about which side of the street to use and which bus headsign to look for. The app can warn you when a bus with your route number is heading the wrong way.
- **Full-route visualizer:** See the route as a simple line diagram, with your location, boarding stop, and destination highlighted. If you miss your stop, see the next stops along the route.
- **Live ride companion:** After you board, compare your location and direction of travel with the route. Get an alert if the bus appears to be going the wrong way, or a reminder when it’s time to pull the cord.

## Project status

These are the intended features; the app is at an early concept stage. This project began at Hacktoberfest Hack Day College Park x GDSC UMD.

## Team setup

| Folder / file          | Owner                  |
|------------------------|------------------------|
| `frontend/`            | frontend teammate      |
| `backend/transit.py`   | backend teammate (bus logic) |
| `backend/ai.py`        | Taha (the translator)  |
| `backend/main.py`      | connects everything    |
| `data/`                | the bus files          |

## Run it
```
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
Then open `frontend/index.html` in a browser.

## Workflow
```
git checkout -b your-name     # work on your own branch
git add . && git commit -m "what you did"
git push -u origin your-name  # then open a pull request into main
git pull origin main          # grab everyone else's latest work
```
