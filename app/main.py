import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.routes import router as api_router  # Now try this import
from fastapi import FastAPI

app = FastAPI()
app.include_router(api_router)
