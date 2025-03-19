import os
import base64
from datetime import datetime
from PIL import Image
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load environment variables
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-001')

# Default macOS screenshot location
DEFAULT_SCREENSHOT_DIR = os.path.expanduser("~/Desktop")

# Track processed files to avoid duplicate processing
processed_files = set()
latest_processed_file = None

class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
    
    def on_created(self, event):
        # Check if the file created is a screenshot
        if not event.is_directory and event.src_path.endswith(('.png', '.jpg', '.jpeg')):
            # Check if filename follows macOS screenshot naming pattern
            filename = os.path.basename(event.src_path)
            if filename.startswith("Screenshot "):
                # If this is a new screenshot, process it
                if event.src_path not in processed_files:
                    processed_files.add(event.src_path)
                    self.callback(event.src_path)

def process_image(image_path):
    """Process the image using Gemini model to extract and answer quiz questions."""
    try:
        # Open and prepare the image
        img = Image.open(image_path)
        
        # Create a prompt for the model
        prompt = """
        You are a quiz assistant. Analyze this screenshot of a quiz question.
        Identify the question and provide the most accurate answer.
        If there are multiple choice options, indicate the correct one.
        Structure your response as:
        
        Question: [extracted question]
        Answer: [your answer]
        Explanation: [brief explanation of why this is correct]
        
        Keep your explanation concise and clear.
        """
        
        # Generate content using the model
        response = model.generate_content([prompt, img])
        
        global latest_processed_file
        latest_processed_file = {
            "success": True,
            "answer": response.text,
            "image_path": image_path
        }
        
        # Let any connected clients know there's a new result
        # (this is a placeholder - we'll implement WebSocket or polling in the frontend)
        
        return latest_processed_file
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        latest_processed_file = {
            "success": False,
            "error": str(e),
            "image_path": image_path
        }
        return latest_processed_file

def start_screenshot_monitoring():
    """Start monitoring the screenshot directory for new screenshots."""
    event_handler = ScreenshotHandler(process_image)
    observer = Observer()
    observer.schedule(event_handler, path=DEFAULT_SCREENSHOT_DIR, recursive=False)
    observer.start()
    print(f"Now monitoring {DEFAULT_SCREENSHOT_DIR} for new screenshots")
    return observer

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/poll_results', methods=['GET'])
def poll_results():
    """Endpoint to poll for the latest processed screenshot."""
    if latest_processed_file:
        result = latest_processed_file.copy()
        # Convert image to base64 for display
        with open(result["image_path"], "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
            result["image_data"] = img_data
        return jsonify(result)
    else:
        return jsonify({"success": False, "message": "No screenshots processed yet"})

if __name__ == "__main__":
    # Start monitoring for screenshots
    observer = start_screenshot_monitoring()
    
    try:
        # Run the Flask app
        app.run(debug=True)
    except KeyboardInterrupt:
        observer.stop()
    observer.join() 