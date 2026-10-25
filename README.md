# UMD Transit Hero

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
