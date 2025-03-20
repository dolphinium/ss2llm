# Project Brief: AI Quiz Answering App

## Core Requirements
- Develop a macOS application that automatically processes quiz questions from screenshots
- Use Google's Gemini 2.0 Flash model for multimodal processing and answer generation
- Provide real-time answers through a simple web interface
- Support native macOS screenshot functionality (Command + Shift + 4)

## Project Goals
1. Create a seamless user experience for processing quiz questions
2. Leverage advanced AI capabilities for accurate answer generation
3. Provide both web interface and CLI options for flexibility
4. Maintain high performance and reliability in real-time processing

## Project Scope
### In Scope
- Screenshot monitoring and processing
- Integration with Gemini 2.0 Flash model
- Web interface for displaying answers
- CLI alternative interface
- Answer history tracking
- Local execution environment

### Out of Scope
- Cloud deployment
- Mobile support
- Custom screenshot mechanism
- Advanced user management
- Database persistence

## Technical Requirements
- Python 3.8 or higher
- Google API key with Gemini model access
- macOS environment
- Core dependencies:
  - Flask for web interface
  - Watchdog for file monitoring
  - Google Generative AI library
  - Python-dotenv for configuration

## Success Criteria
1. Automatic detection and processing of macOS screenshots
2. Accurate question interpretation and answer generation
3. Real-time answer display in the interface
4. Stable performance under continuous use
5. Clear and intuitive user experience 