from fastapi import APIRouter, File, UploadFile, HTTPException
from app.utils import save_file, run_analysis_pipeline, get_processed_file_path
from fastapi import Form
from .utils import DATA_DIR
import os




router = APIRouter()

# 1. Upload Endpoint
@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file
    filepath = save_file(file)
    return {"message": "File uploaded successfully", "filename": filepath.name}

# 2. Process Endpoint
@router.post("/process/")
async def process_file(filename: str = Form(...)):
    # Ensure the file exists
    filepath = get_processed_file_path(filename)
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Run the feedback analysis pipeline on the uploaded file
    result_filepath = run_analysis_pipeline(filepath)

    return {"message": "Processing completed", "result_file": result_filepath.name}

# 3. Results Endpoint
@router.get("/results/")
async def get_results():
    # Get all files in the directory
    processed_files = list(DATA_DIR.glob("processed_*.csv"))

    # Check if there are any processed files
    if not processed_files:
        raise HTTPException(status_code=404, detail="No processed files found")

    # Sort files by modification time and pick the latest one
    latest_file = max(processed_files, key=os.path.getmtime)
    print(f"Returning the latest processed file: {latest_file}")

    # Return the file content
    return {"result_file": latest_file.name, "content": latest_file.read_text()}
