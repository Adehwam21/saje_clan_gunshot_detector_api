import shutil
from pathlib import Path

# Utility function to save uploaded files temporarily
def save_temp_file(upload_file):
    """
    Stores the uploaded file in a temporary directory for processing.

    Args:
        upload_file (UploadFile): The uploaded file received in a request.
    
    Returns:
        list: A list containing the directory path and the full path to the saved file.
    """
    # Define the path for the temporary directory
    temp_dir = Path("app/temp")
    
    # Create the temporary directory if it doesn't exist, including any parent directories
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Construct the full path for the temporary file
    temp_file_path = temp_dir / upload_file.filename

    # Open the temporary file in write-binary mode and save the uploaded content
    with temp_file_path.open("wb") as temp_file:
        shutil.copyfileobj(upload_file.file, temp_file)  # Copy the uploaded file to the temp location

    # Return the path of the temporary directory and the saved file
    return [str(temp_dir), str(temp_file_path)]
