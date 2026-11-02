# WasteWise

Intelligent Waste Management & EcoRewards - Final Year Project.

## Folders
- `backend/`  - Python FastAPI server (the rules + database access)
- `frontend/` - React app (the screens) - added in a later step

## Run the backend (Step 1)
```
cd backend
python -m venv venv
venv\Scripts\activate          (Windows)
source venv/bin/activate       (Mac/Linux)
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Then open http://127.0.0.1:8000/docs
