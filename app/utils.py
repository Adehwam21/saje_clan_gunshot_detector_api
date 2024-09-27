import shutil
from pathlib import Path
from datetime import datetime

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



def format_gps_data(gpsData: str):
    # Split the GPS data string into components
    gpsData = gpsData.split(",")
    
    # Extract latitude, longitude, and timestamp
    latitude, longitude, timestamp = gpsData[0].strip(), gpsData[1].strip(), gpsData[2].strip()

    # Convert latitude and longitude to floats
    latitude = float(latitude)
    longitude = float(longitude)
    
    # Convert timestamp (milliseconds) to seconds and format the time
    timestamp_seconds = int(timestamp) / 1000
    time_str = datetime.utcfromtimestamp(timestamp_seconds).strftime('%H:%M:%S')
    
    # Get the current date
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    
    # Return the data in a dictionary
    return {
        "lat": latitude,
        "lng": longitude,
        "date": current_date,
        "time": time_str
    }

