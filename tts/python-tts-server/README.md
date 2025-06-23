# Python TTS Server with Edge TTS

A Python Flask server that provides Text-to-Speech (TTS) functionality using Microsoft Edge TTS engine. Supports multiple languages, emotions, and voice styles including Vietnamese voices.

## Features

- 🎯 **Free to use** - No API keys required
- 🌍 **Multi-language support** - English, Vietnamese, and many more
- 😊 **Emotion support** - Happy, sad, angry, excited, etc.
- 🎭 **Voice styles** - Cheerful, friendly, whispering, shouting, etc.
- 🔊 **High-quality audio** - MP3 output format
- ⚡ **Fast processing** - Lightweight and efficient

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation & Setup

### 1. Clone or download the project
```bash
cd "EdgeTTSAndYoutubeContentGenerator\tts\python-tts-server"
```

### 2. Create a virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

# You should see (venv) in your command prompt
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
python main.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "TTS Server"
}
```

### 2. Get Available Voices
```http
GET /voices
```
**Response:**
```json
[
  {
    "name": "Microsoft Aria Online (Natural) - English (United States)",
    "short_name": "en-US-AriaNeural",
    "gender": "Female",
    "locale": "en-US",
    "language": "en"
  }
]
```

### 3. Synthesize Speech
```http
POST /synthesize
Content-Type: application/json
```
**Request Body:**
```json
{
  "text": "Hello world, this is a test!",
  "voice": "en-US-AriaNeural",
  "rate": "+10%",
  "pitch": "+2Hz",
  "style": "cheerful"
}
```
**Response:** Audio file (MP3 format)

## Supported Languages & Voices

### English Voices
- `en-US-AriaNeural` (Female) - Supports emotions
- `en-US-JennyNeural` (Female) - Supports emotions  
- `en-US-GuyNeural` (Male) - Supports emotions
- `en-GB-SoniaNeural` (Female)
- `en-AU-NatashaNeural` (Female)

### Vietnamese Voices
- `vi-VN-HoaiMyNeural` (Female) - Default Vietnamese voice
- `vi-VN-NamMinhNeural` (Male)

## Supported Emotions & Styles

- `neutral` (default)
- `cheerful`
- `sad`
- `angry`
- `excited`
- `friendly`
- `hopeful`
- `shouting`
- `terrified`
- `unfriendly`
- `whispering`

## Usage Examples

### Using cURL

#### Basic synthesis:
```bash
curl -X POST http://localhost:5000/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}' \
  --output hello.mp3
```

#### With emotion (English):
```bash
curl -X POST http://localhost:5000/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "I am so happy today!", "voice": "en-US-AriaNeural", "style": "cheerful"}' \
  --output happy.mp3
```

#### Vietnamese voice:
```bash
curl -X POST http://localhost:5000/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Xin chào thế giới!", "voice": "vi-VN-HoaiMyNeural"}' \
  --output vietnamese.mp3
```

#### With speed and pitch adjustment:
```bash
curl -X POST http://localhost:5000/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Fast and high pitch", "rate": "+50%", "pitch": "+5Hz"}' \
  --output fast.mp3
```

### Using Python requests

```python
import requests

# Basic request
response = requests.post('http://localhost:5000/synthesize', 
    json={
        'text': 'Hello from Python!',
        'voice': 'en-US-AriaNeural',
        'style': 'friendly'
    }
)

# Save audio file
with open('output.mp3', 'wb') as f:
    f.write(response.content)
```

### Using JavaScript (fetch)

```javascript
fetch('http://localhost:5000/synthesize', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: 'Hello from JavaScript!',
        voice: 'en-US-AriaNeural',
        style: 'excited'
    })
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'output.mp3';
    a.click();
});
```

## Configuration

Edit `config.py` to customize:

- Server port and host
- Default voice settings
- Maximum text length
- Supported voice styles
- Default Vietnamese voice

## Integration with Java Spring

From your Java Spring application, you can call this TTS server:

```java
// Example Java code
RestTemplate restTemplate = new RestTemplate();
HttpHeaders headers = new HttpHeaders();
headers.setContentType(MediaType.APPLICATION_JSON);

Map<String, Object> request = new HashMap<>();
request.put("text", "Hello from Java Spring!");
request.put("voice", "en-US-AriaNeural");
request.put("style", "friendly");

HttpEntity<Map<String, Object>> entity = new HttpEntity<>(request, headers);
byte[] audioData = restTemplate.postForObject(
    "http://localhost:5000/synthesize", 
    entity, 
    byte[].class
);
```

## Troubleshooting

### Virtual Environment Issues
Make sure to activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# You should see (venv) in your prompt
```

### Port Already in Use
Change the port in `config.py`:
```python
SERVER_PORT = 5001  # Change to available port
```

### Missing Dependencies
Reinstall requirements:
```bash
pip install -r requirements.txt --force-reinstall
```

## Development

To run in development mode:
```bash
# Make sure virtual environment is activated
```

To deactivate virtual environment:
```bash
deactivate
```

## License

This project uses the Edge TTS library which is free to use. Please check Microsoft's terms of service for Edge TTS usage.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify your Python version (3.7+)
3. Ensure all dependencies are installed
4. Check server logs for error messages