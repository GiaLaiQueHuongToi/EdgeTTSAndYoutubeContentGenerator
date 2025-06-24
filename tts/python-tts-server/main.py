from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import asyncio
from src.services.tts_service import TTSService
from src.models.tts_models import TTSRequest

app = Flask(__name__)

# Cấu hình CORS
CORS(app, 
     origins=['*'],  # Cho phép tất cả domains (hoặc chỉ định cụ thể)
     methods=['GET', 'POST', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'Accept'],
     supports_credentials=True
)

tts_service = TTSService()

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.json
    text = data.get('text', '')
    language = data.get('language', 'en-US')
    gender = data.get('gender', 'female')
    emotion = data.get('emotion', 'neutral')
    
    if not text:
        return jsonify({'error': 'Text required'}), 400
    
    try:
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ttsRequest = TTSRequest(
            text=text,
            language=language,
            gender=gender,
            emotion=emotion
        )
        
        # Get the result dictionary
        result = loop.run_until_complete(
            tts_service.synthesize_speech(ttsRequest)
        )
        loop.close()
        
        # Check if synthesis was successful
        if not result['success']:
            return jsonify({'error': result['error']}), result['status_code']
        
        # Return raw binary data
        return Response(
            result['audio_data'],  # This is the raw bytes
            mimetype=result['content_type'],  # 'audio/mpeg'
            headers={
                'Content-Disposition': 'attachment; filename=tts.mp3',
                'X-Duration': str(result['metadata'].duration_seconds),
                'X-Language': result['metadata'].language,
                'X-Gender': result['metadata'].gender,
                'X-Voice': result['metadata'].voice_name,
                'X-Emotion': result['metadata'].emotion
            }
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)