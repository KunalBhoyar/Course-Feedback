from fastapi import APIRouter, File, UploadFile, HTTPException
from app.utils import save_file, run_analysis_pipeline, get_processed_file_path, upload_file_to_gcs
from fastapi import Form
from .utils import DATA_DIR
import os
import uuid





router = APIRouter()



@router.post("/upload")
async def upload_file(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Generate a unique filename to avoid collisions
    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    # Upload file to GCS
    file_url = upload_file_to_gcs(file, unique_filename)

    return {"file_url": file_url, "filename": unique_filename}

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
