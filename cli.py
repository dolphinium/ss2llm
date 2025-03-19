#!/usr/bin/env python3
"""
Command-line interface for the AI Quiz Assistant.
This script provides a simple CLI alternative to the web interface.
"""

import os
import time
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load environment variables
load_dotenv()

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY found in environment variables. Please create a .env file with your API key.")

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-001')

# Default macOS screenshot location
DEFAULT_SCREENSHOT_DIR = os.path.expanduser("~/Desktop")

# Track processed files to avoid duplicate processing
processed_files = set()

class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Check if the file created is a screenshot
        if not event.is_directory and event.src_path.endswith(('.png', '.jpg', '.jpeg')):
            # Check if filename follows macOS screenshot naming pattern
            filename = os.path.basename(event.src_path)
            if filename.startswith("Screenshot "):
                # If this is a new screenshot, process it
                if event.src_path not in processed_files:
                    processed_files.add(event.src_path)
                    print(f"\nNew screenshot detected: {filename}")
                    print("Processing...")
                    result = process_image(event.src_path)
                    
                    print("\n=== AI Response ===")
                    print(result)
                    print("===================")
                    print("\nMonitoring for new screenshots... (Press Ctrl+C to exit)")

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
        
        return response.text
    except Exception as e:
        return f"Error processing image: {str(e)}"

def main():
    """Main function to run the CLI application."""
    print("=== AI Quiz Assistant CLI ===")
    print("This tool automatically processes screenshots of quiz questions.")
    print("\nInstructions:")
    print("1. Position your quiz question on screen")
    print("2. Take a screenshot with Command (⌘) + Shift + 4")
    print("3. Select the area containing the question")
    print("4. The answer will appear here automatically")
    print("\nMonitoring for new screenshots... (Press Ctrl+C to exit)")
    
    # Start monitoring for screenshots
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, path=DEFAULT_SCREENSHOT_DIR, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nExiting. Goodbye!")
    
    observer.join()

if __name__ == "__main__":
    main() 