import os
import io
import base64
import time
import glob
from datetime import datetime
from PIL import Image
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import concurrent.futures
import threading
from functools import partial
import queue
import google.generativeai.types as types

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
model = genai.GenerativeModel('gemini-2.0-flash-lite', generation_config=types.GenerationConfig(temperature=0.0))

# Default macOS screenshot location
DEFAULT_SCREENSHOT_DIR = os.path.expanduser("~/Desktop")

# Track processed files to avoid duplicate processing
processed_files = set()
latest_processed_file = None
processing_lock = threading.Lock()
processing_queue = queue.Queue()

# Maximum retries for model generation
MAX_RETRIES = 2
# Timeout for model generation (in seconds)
MODEL_TIMEOUT = 10  # Increased timeout for better reliability

class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.png', '.jpg', '.jpeg')):
            filename = os.path.basename(event.src_path)
            if filename.startswith("Screenshot "):
                if event.src_path not in processed_files:
                    processed_files.add(event.src_path)
                    processing_queue.put(event.src_path)

def process_with_model(img):
    """Process the image with the model."""
    try:
        # Set a shorter, more focused prompt for faster processing
        safety_prompt = """Analyze this quiz question and provide a concise answer.
Question format: Q:[question text]
Answer format: A:[your answer]
Explanation format: E:[brief explanation]"""
        
        response = model.generate_content([safety_prompt, img])
        return response.text
    except Exception as e:
        raise Exception(f"Model generation failed: {str(e)}")

def process_image(image_path):
    """Process the image using Gemini model with retries and timeout."""
    try:
        img = Image.open(image_path)
        
        # Optimize image size if needed (reduce if too large)
        max_size = 1600
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            img = img.resize((int(img.size[0] * ratio), int(img.size[1] * ratio)), Image.Resampling.LANCZOS)
        
        for attempt in range(MAX_RETRIES):
            try:
                # Use ThreadPoolExecutor for timeout handling
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(process_with_model, img)
                    try:
                        response_text = future.result(timeout=MODEL_TIMEOUT)
                        
                        # Format the response if it's not in the expected format
                        if not any(marker in response_text for marker in ["Q:", "A:", "E:"]):
                            lines = response_text.split('\n')
                            formatted_response = []
                            for line in lines:
                                if "question" in line.lower():
                                    formatted_response.append(f"Q: {line.split(':', 1)[1].strip() if ':' in line else line}")
                                elif "answer" in line.lower():
                                    formatted_response.append(f"A: {line.split(':', 1)[1].strip() if ':' in line else line}")
                                elif "explanation" in line.lower():
                                    formatted_response.append(f"E: {line.split(':', 1)[1].strip() if ':' in line else line}")
                            response_text = '\n'.join(formatted_response) if formatted_response else response_text
                        
                        global latest_processed_file
                        latest_processed_file = {
                            "success": True,
                            "answer": response_text,
                            "image_path": image_path
                        }
                        return latest_processed_file
                        
                    except concurrent.futures.TimeoutError:
                        if attempt < MAX_RETRIES - 1:
                            print(f"Attempt {attempt + 1} timed out, retrying...")
                            time.sleep(2)  # Slightly longer delay between retries
                            continue
                        raise TimeoutError(f"Processing timed out after {MODEL_TIMEOUT} seconds")
                    
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"Attempt {attempt + 1} failed: {str(e)}, retrying...")
                    time.sleep(2)
                else:
                    raise Exception(f"All attempts failed: {str(e)}")
                    
    except Exception as e:
        error_msg = f"Error processing image: {str(e)}"
        print(error_msg)
        latest_processed_file = {
            "success": False,
            "error": error_msg,
            "image_path": image_path
        }
        return latest_processed_file

def process_queue():
    """Process images in the queue."""
    while True:
        try:
            image_path = processing_queue.get(timeout=1)
            with processing_lock:
                process_image(image_path)
        except queue.Empty:
            time.sleep(0.1)  # Short sleep when queue is empty
        except Exception as e:
            print(f"Error in queue processing: {str(e)}")

def start_screenshot_monitoring():
    """Start monitoring the screenshot directory and processing queue."""
    event_handler = ScreenshotHandler(lambda x: processing_queue.put(x))
    observer = Observer()
    observer.schedule(event_handler, path=DEFAULT_SCREENSHOT_DIR, recursive=False)
    observer.start()
    
    # Start the processing queue in a separate thread
    processing_thread = threading.Thread(target=process_queue, daemon=True)
    processing_thread.start()
    
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
        try:
            result = latest_processed_file.copy()
            with open(result["image_path"], "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                result["image_data"] = img_data
            return jsonify(result)
        except Exception as e:
            return jsonify({"success": False, "error": f"Error reading image: {str(e)}"})
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