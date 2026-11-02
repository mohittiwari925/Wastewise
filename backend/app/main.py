# WasteWise backend - main file
# This is the entry point of our server. Everything starts here.

from fastapi import FastAPI

# Create the app. The title shows up on the automatic API test page.
app = FastAPI(
    title="WasteWise API",
    description="Backend for the WasteWise waste management system",
)


# A "route" connects a URL to a Python function.
# When someone opens http://127.0.0.1:8000/ this function runs.
@app.get("/")
def home():
    return {"message": "Welcome to WasteWise API"}


# A health check: lets us (and later the frontend) test if the server is alive.
@app.get("/health")
def health():
    return {"status": "ok"}
