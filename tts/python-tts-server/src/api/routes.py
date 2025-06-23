from flask import Flask, request, jsonify, Response
import asyncio
from src.services.tts_service import TTSService
from src.models.tts_models import TTSRequest

app = Flask(__name__)
tts_service = TTSService()

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io

@app.post("/tts/synthesize")
async def synthesize_speech(request: TTSRequest):
    result = await tts_service.synthesize_speech(request)
    
    if not result['success']:
        return {"error": result['error']}, result['status_code']
    
    # Create binary stream
    audio_stream = io.BytesIO(result['audio_data'])
    
    # Return binary stream with metadata in headers
    return StreamingResponse(
        audio_stream,
        media_type=result['content_type'],
        headers={
            "Content-Disposition": "attachment; filename=audio.mp3",
            "X-Duration": str(result['metadata'].duration_seconds),
            "X-Language": result['metadata'].language,
            "X-Gender": result['metadata'].gender,
            "X-Voice": result['metadata'].voice_name,
            "X-Emotion": result['metadata'].emotion
        }
    )

@app.route('/synthesize-json', methods=['POST'])
def synthesize_json():
    """TTS synthesis endpoint - returns JSON response"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        try:
            tts_request = TTSRequest(**data)
        except Exception as e:
            return jsonify({'error': f'Invalid request data: {str(e)}'}), 400
        
        # Call service method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(tts_service.synthesize_speech(tts_request))
        finally:
            loop.close()
        
        # Handle service response
        if not result['success']:
            return jsonify({'error': result['error']}), result['status_code']
        
        return jsonify(result['response'].dict()), result['status_code']
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/languages', methods=['GET'])
def get_supported_languages():
    """Get supported languages"""
    result = tts_service.get_supported_languages()
    return jsonify(result.dict())

@app.route('/voices', methods=['GET'])
def get_supported_voices():
    """Get supported voices mapping"""
    result = tts_service.get_supported_voices()
    return jsonify(result.dict())

@app.route('/emotions', methods=['GET'])
def get_supported_emotions():
    """Get supported emotions"""
    result = tts_service.get_supported_emotions()
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    result = tts_service.get_health_status()
    return jsonify(result.dict())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)