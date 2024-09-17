from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.model.gunshotPredictor import GunshotDetector
from app.utils import save_temp_file
import os

# Initialize FastAPI app
app = FastAPI()

# Try to load the pre-trained gunshot detection model at startup
try:
    GunshotDetector.load_model("app/model/best.model")
except Exception as e:
    # If the model fails to load, print the error message to the console
    print(f"Failed to load model: {e}")

# Root route for checking if the API is up
@app.get("/")
async def root():
    """Root endpoint to check if the server is running.

    Returns:
        dict: A simple dictionary with a status code message.
    """
    return {"200": "OK"}


# Endpoint for gunshot detection
@app.post("/detect")
async def detect_gunshot(file: UploadFile = File(...)):
    """Endpoint to detect gunshots in an uploaded audio file.

    Args:
        file (UploadFile): The uploaded audio file for detection.
    
    Returns:
        dict: A dictionary containing the detection results or an error message.
    
    Raises:
        HTTPException: If no gunshot is detected or an error occurs during processing.
    """
    try:
        # Save the uploaded file temporarily to disk
        _, sound_file_path = save_temp_file(file)
        
        # Run gunshot detection on the saved file
        results = await GunshotDetector.predict_gunshot(sound_file_path)
        
        # Remove the temporary file after prediction is done
        os.remove(sound_file_path)  

        # If no results are returned, raise a 404 HTTP exception
        if not results:
            raise HTTPException(status_code=404, detail="No gunshot detected.")
        
        # Return the detection results as a response
        return {"results": results}

    except Exception as e:
        # Return a JSON response with an error message and a 500 status code in case of an exception
        return JSONResponse(content={"error": str(e)}, status_code=500)
