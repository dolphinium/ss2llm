# AI Quiz Answering App

This application uses Google's Gemini 2.0 Flash model to process quiz questions from screenshots and provide answers. The app monitors for macOS screenshots, processes them with the Gemini multimodal model, and displays the answers in real-time.

## Features

- Automatic detection of macOS screenshots (using Command + Shift + 4)
- Image processing using Gemini 2.0 Flash multimodal model
- Real-time answer generation for quiz questions
- Simple and intuitive user interface
- Answer history displayed in the sidebar

## Requirements

- macOS (for the native screenshot functionality)
- Python 3.8 or higher
- Google API key with access to Gemini models

## Installation

1. Clone this repository or download the source code.

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory:
   ```
   cp .env.example .env
   ```

4. Get a Google Gemini API key from the Google AI Studio (https://makersuite.google.com/app/apikey) and add it to the `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

1. Start the application:
   ```
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000/`

3. The application will open with a simple interface showing:
   - A sidebar with status indicator and answer history
   - A main panel showing the latest processed screenshot

4. To analyze a quiz question:
   - Position the quiz question on your screen
   - Take a screenshot using macOS native screenshot tool (Command + Shift + 4)
   - Select the area containing the question
   - The application will automatically detect the new screenshot, process it, and display the answer

## Command Line Interface

For a simpler interaction, you can also use the CLI version:

```
python cli.py
```

The CLI version will monitor for screenshots and output the answers directly in the terminal.

## Customization

You can customize the model's behavior by modifying the prompt in the `process_image` function in `app.py`.

## How It Works

1. The application monitors your Desktop folder for new screenshot files
2. When a macOS screenshot is detected (files starting with "Screenshot"), it's processed
3. The Gemini 2.0 Flash model analyzes the screenshot to extract the question
4. The model generates an answer based on its understanding of the question
5. The answer is displayed in the web interface or CLI

## Limitations

- The accuracy of the answers depends on the capabilities of the Gemini 2.0 Flash model
- The application works best with clear, well-formatted quiz questions
- Processing time may vary based on your internet connection and the complexity of the image 