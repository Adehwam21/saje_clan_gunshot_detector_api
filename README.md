# Sajeclan Gunshot Detection API

This API detects gunshots in uploaded audio files using machine learning and sends alerts via Telegram when a gunshot is detected. The model is based on the `opensoundscape` library and utilizes a pre-trained ResNet18 binary classification model to predict the presence of gunshots.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

This project uses Python 3.8+ (specifically Python 3.10) and Poetry for dependency management.

### Clone the repository:

```bash
git clone https://github.com/yourusername/sajeclan-gunshot-detection-api.git
cd sajeclan-gunshot-detection-api
```

### Install dependencies:

First, ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed on your system. Then, run:

```bash
poetry install
```

This will install all the dependencies specified in the `pyproject.toml` file, including the machine learning libraries, FastAPI, and Telegram bot integration.

## Setup

### Pre-trained Model

Before you can start detecting gunshots, you need to have the pre-trained model saved in `app/model/best.model`. Place your model file in this directory.

Credits: @lydiakatsis (GitHub)

### Environment Variables

Create a `.env` file in the root of your project and add the following environment variables:

```bash
TELEGRAM_SAJE_BOT_TOKEN=<your_telegram_bot_token>
TELEGRAM_ANTI_POACHING_GROUP_CHAT_ID=<your_group_chat_id>
```

These variables are required for the Telegram bot integration to send alerts.

## Usage

### Running the API

To start the FastAPI server, run the following command:

```bash
uvicorn app.main:app --reload
```

This will start the API server on `http://127.0.0.1:8000`.

Or run in virtual environment with Poetry:

```bash
poetry shell
poetry run uvicorn app.main:app --reload
```

## Endpoints

### `GET /`

Returns a simple health check response to ensure the API is running.

- **Response:**
  ```json
  {
    "200": "OK"
  }
  ```

### `POST /detect`

Uploads an audio file and runs it through the gunshot detection model.

- **Request:** A file upload (`multipart/form-data`)
  - `file`: The audio file to be analyzed.
- **Response:** JSON response indicating the result of the detection.

  - If a gunshot is detected, a message is sent to the configured Telegram group.

- Example:
  ```json
  {
    "results": "Wildlife Rescue Team! I detected a Gunshot. Probability: 82.45%"
  }
  ```

## Environment Variables

The project relies on the following environment variables:

- **TELEGRAM_SAJE_BOT_TOKEN**: Your Telegram bot's API token for sending messages.
- **TELEGRAM_ANTI_POACHING_GROUP_CHAT_ID**: The chat ID of the group to which gunshot alerts will be sent.

Make sure these variables are set correctly in the `.env` file.

## Project Structure

```bash
sajeclan-gunshot-detection-api/
├── app/
│   ├── main.py               # FastAPI application
│   ├── model/
│   │   ├── gunshotPredictor.py  # Gunshot detection logic
│   │   ├── best.model         # Pre-trained gunshot detection model
│   ├── utils.py               # Utility functions (e.g., file saving)
├── temp/                      # Temporary file storage
├── .env                       # Environment variables
├── README.md                  # Project documentation
└── pyproject.toml             # Poetry dependency manager configuration
```

## Contributing

Contributions to this project are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
