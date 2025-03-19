# AI Quiz Answering App Development Plan

## Objective
- Develop an AI app that processes quiz questions from screenshots and provides answers using a multimodal LLM.

## Development Stages

### 1. Research and Planning
- [x] Research the capabilities and requirements of the Gemini 2.0 flash model.
- [x] Determine the best way to integrate the Gemini 2.0 model into the app.
- [x] Identify libraries and tools needed for capturing screenshots and displaying answers.

### 2. Environment Setup
- [x] Set up a development environment on your MacBook Air.
- [x] Install necessary libraries and dependencies (e.g., Python, Flask, watchdog, etc.).

### 3. Screenshot Integration
- [x] Implement functionality to monitor and detect macOS screenshots (using Command + Shift + 4).
- [x] Ensure screenshots are processed in a format compatible with the Gemini 2.0 model.

### 4. Image Processing
- [x] Integrate the Gemini 2.0 model to process screenshots directly (no explicit OCR needed).
- [x] Develop a method to extract text and context from the screenshots using the model.

### 5. Answer Generation
- [x] Use the processed text to query the Gemini 2.0 model for answers.
- [x] Implement logic to handle different types of questions (e.g., multiple choice, true/false).

### 6. User Interface
- [x] Design a simple UI to display answers on the left screen.
- [x] Implement automatic UI updates when new screenshots are detected and processed.

### 7. Integration
- [x] Integrate all components to ensure seamless operation.
- [ ] Test the app to ensure it functions as expected.

### 8. Documentation
- [x] Document the code and development process for future reference.
- [x] Create a user guide for operating the app.

## Notes
- Focus on local execution; no need for cloud deployment.
- The app now uses native macOS screenshot capabilities (Command + Shift + 4) rather than an in-app screenshot mechanism.
- File monitoring implemented using watchdog library to detect new screenshots.
- Testing, optimization, and deployment phases are not included in this plan.
