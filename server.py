from flask import Flask, request, send_file
import os
import uuid
import subprocess

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audios"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/api/extrair-audio', methods=['POST'])
def extrair_audio():
    if 'data' not in request.files:
        return {"error": "Nenhum arquivo recebido com a chave 'data'"}, 400

    video_file = request.files['data']
    video_id = str(uuid.uuid4())
    video_path = os.path.join(UPLOAD_FOLDER, f"{video_id}.mp4")
    audio_path = os.path.join(AUDIO_FOLDER, f"{video_id}.wav")

    video_file.save(video_path)

    try:
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
        os.remove(video_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
