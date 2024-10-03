import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from opensoundscape.preprocess.preprocessors import AudioToSpectrogramPreprocessor
from opensoundscape.torch.models.cnn import Resnet18Binary
from app.utils import format_gps_data
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Load environment variables from the .env file
load_dotenv()

# Retrieve the bot token and group chat ID from environment variables
bot_token = os.environ.get("TELEGRAM_SAJE_BOT_TOKEN")
group_chat_id = os.environ.get("TELEGRAM_ANTI_POACHING_GROUP_CHAT_ID")

# Raise an error if the bot token or chat ID are not found in the environment variables
if not bot_token or not group_chat_id:
    raise EnvironmentError("Bot token or chat ID not found in environment variables.")

class GunshotDetector:
    """A class responsible for detecting gunshots and notifying a Telegram group."""

    # Static variables for the model and the Telegram bot
    model = None
    bot = Bot(token=bot_token)  # Initialize the bot with the token from the environment
    group_chat_id = group_chat_id  # Set the group chat ID from the environment

    @staticmethod
    def load_model(model_path):
        """Load the gunshot detection model.

        Args:
            model_path (str or Path): Path to the pre-trained model file.
        
        Raises:
            FileNotFoundError: If the model file does not exist.
        """
        model_path = Path(model_path)  # Convert the model path to a Path object

        # Check if the model file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load the Resnet18Binary model with 'negative' and 'positive' classes for gunshot detection
        GunshotDetector.model = Resnet18Binary(classes=['negative', 'positive'])
        GunshotDetector.model.load(path=model_path)  # Load the pre-trained model

    @staticmethod
    def preprocess_audio(file_path):
        """Preprocess audio file to spectrogram format for prediction.

        Args:
            file_path (str or Path): Path to the audio file to be processed.
        
        Returns:
            Preprocessed audio file in spectrogram format.
        
        Raises:
            FileNotFoundError: If the audio file does not exist.
        """
        file_path = Path(file_path)  # Convert the file path to a Path object

        # Check if the audio file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        # Create a DataFrame with the audio file path as the index (required for preprocessing)
        audio_file_df = pd.DataFrame(index=[file_path])
        
        # Define the preprocessing steps for converting audio to spectrogram
        preprocessor = AudioToSpectrogramPreprocessor(audio_file_df, return_labels=False)
        preprocessor.actions.load_audio.set(sample_rate=8000)  # Set audio sample rate to 8000 Hz
        preprocessor.actions.bandpass.set(min_f=0, max_f=2000)  # Apply bandpass filter (0 to 2000 Hz)
        preprocessor.actions.bandpass.on()  # Enable bandpass filtering
        preprocessor.actions.to_spec.set(window_samples=256, overlap_samples=128)  # Set spectrogram window and overlap

        return preprocessor

    @staticmethod
    async def predict_gunshot(file_path, gpsData):
        """Perform gunshot prediction and send notification to a Telegram group if detected.

        Args:
            file_path (str or Path): Path to the audio file to be analyzed.
        
        Returns:
            str: A message indicating whether a gunshot was detected.
        
        Raises:
            ValueError: If the model has not been loaded.
        """
        # Ensure the model is loaded before making predictions
        if GunshotDetector.model is None:
            raise ValueError("Model is not loaded. Call `load_model()` first.")
    
        # Preprocess the audio file into a spectrogram format
        prediction_dataset = GunshotDetector.preprocess_audio(file_path=file_path)

        # Run the model prediction on the preprocessed audio
        scores, _, _ = GunshotDetector.model.predict(
            prediction_dataset,
            batch_size=1,
            num_workers=0,
            activation_layer="softmax",
            binary_preds='multi_target',
            threshold=0.808802  # Prediction threshold for positive detection
        )

        # Extract the 'positive' prediction score from the result
        positive_score = float(scores.iloc[0]['positive'])
        SajeBot = GunshotDetector.bot  # Telegram bot instance
        group_chat_id = GunshotDetector.group_chat_id  # Chat ID for the Telegram group
        GPS_data = format_gps_data(gpsData)

        # If the score indicates a positive gunshot detection, send a message and the audio file
        if positive_score > 0.808802:
            message = f"Wildlife Rescue Team! I detected a Gunshot.\nProbability: {round(positive_score * 100, 2)}%\nDate, Time: {GPS_data['date'], GPS_data['time']}"
            
            # Send a message to the Telegram group
            await SajeBot.send_message(chat_id=group_chat_id, text=message)
            
            # Send the audio file to the Telegram group
            with open(file_path, 'rb') as audio_file:
                await SajeBot.send_audio(chat_id=group_chat_id, audio=audio_file)
            
            await SajeBot.send_location(chat_id = group_chat_id, 
                                        latitude= GPS_data['lat'], 
                                        longitude = GPS_data['lng'], 
                                        horizontal_accuracy= 30, 
                                        )
            
            return message  # Return the message that was sent
        else:
            # If no gunshot is detected, return a message indicating low probability
            
            # Doing this for presentation purpose.
            message = f"No Gunshot detected. Probability: {round(positive_score * 100, 2)}%"

            # # Send a message to the Telegram group
            await SajeBot.send_message(chat_id=group_chat_id, text=message)
            
            # Send the audio file to the Telegram group
            with open(file_path, 'rb') as audio_file:
                await SajeBot.send_audio(chat_id=group_chat_id, audio=audio_file)
            
            await SajeBot.send_location(chat_id = group_chat_id, 
                                        latitude= GPS_data['lat'], 
                                        longitude = GPS_data['lng'], 
                                        horizontal_accuracy= 30, 
                                        )
            return message
