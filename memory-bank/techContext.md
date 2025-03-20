# Technical Context: AI Quiz Answering App

## Technology Stack

### Core Technologies
1. **Python 3.8+**
   - Primary development language
   - Extensive library support
   - Cross-platform compatibility

2. **Google Gemini 2.0 Flash**
   - Multimodal AI model
   - Direct image processing
   - Natural language generation

3. **Flask**
   - Web framework
   - Route handling
   - Template rendering

4. **Watchdog**
   - File system monitoring
   - Event handling
   - Real-time detection

### Dependencies
```
google-generativeai==0.3.2
Flask==3.0.2
Pillow==10.2.0
python-dotenv==1.0.1
watchdog==4.0.0
```

## Development Setup

### Environment Setup
1. **Python Virtual Environment**
   ```bash
   # Using venv
   python3 -m venv venv
   source venv/bin/activate
   
   # Using conda
   conda create -n quiz-app python=3.8
   conda activate quiz-app
   ```

2. **Dependencies Installation**
   ```bash
   pip install -r requirements.txt
   ```

3. **API Configuration**
   ```bash
   # .env file
   GOOGLE_API_KEY=your_api_key_here
   ```

### macOS Configuration
1. **Screenshot Settings**
   - Command + Shift + 5 to access
   - Save to Desktop
   - Disable floating thumbnail

## Technical Constraints

### System Requirements
- macOS operating system
- Python 3.8 or higher
- Internet connection for API
- Desktop write permissions

### Performance Constraints
- API rate limits
- Image processing speed
- Network latency
- Memory usage for history

### Security Considerations
- API key protection
- Local file access
- No data persistence
- User input validation

## Development Tools

### Required Tools
- Python IDE/Editor
- Terminal access
- Git for version control
- Web browser for testing

### Optional Tools
- API testing tools
- Image editing software
- Performance monitoring
- Debug tools

## File Structure
```
.
├── app.py              # Main web application
├── cli.py              # Command line interface
├── requirements.txt    # Dependencies
├── .env               # Configuration
├── .gitignore        # Git ignore rules
├── README.md         # Documentation
├── templates/        # Web templates
└── screenshots/      # Example screenshots
```

## Testing Environment

### Local Testing
- Development server
- Screenshot simulation
- API response testing
- Interface validation

### Debug Tools
- Flask debug mode
- Python debugger
- Console logging
- Error tracking

## Deployment

### Local Deployment
1. Clone repository
2. Set up environment
3. Configure API key
4. Run application

### Maintenance
- Dependency updates
- API key rotation
- Error monitoring
- Performance optimization 