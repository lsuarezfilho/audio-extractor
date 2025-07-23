from flask import Flask, request, send_file
import os
import uuid
import subprocess
import requests

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audios"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/api/extrair-audio', methods=['POST'])
def extrair_audio():
    video_url = request.json.get('url')
    if not video_url:
        return {"error": "Campo 'url' ausente"}, 400

    video_id = str(uuid.uuid4())
    video_path = os.path.join(UPLOAD_FOLDER, f"{video_id}.mp4")
    audio_path = os.path.join(AUDIO_FOLDER, f"{video_id}.wav")

    try:
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(video_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        subprocess.run([
            "ffmpeg", "-i", video_path,
            "-vn", "-acodec", "pcm_s16le",
            "-ar", "44100", "-ac", "2",
            audio_path
        ], check=True)

        return send_file(audio_path, mimetype="audio/wav")
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
