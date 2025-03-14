from flask import Flask, request, send_file
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/convert", methods=["POST"])
def convert_audio():
    if "file" not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files["file"]
    format = request.form.get("format", "wav")  # Padrão: WAV

    # Adicionando "mpga" à lista de formatos válidos
    if format not in ["wav", "aac", "mpga"]:
        return {"error": "Invalid format"}, 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(UPLOAD_FOLDER, f"{os.path.splitext(filename)[0]}.{format}")

    file.save(input_path)

    # Comando FFmpeg para conversão
    ffmpeg_command = [
        "ffmpeg", "-i", input_path, "-y", output_path
    ]

    subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not os.path.exists(output_path):
        return {"error": "Conversion failed"}, 500

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
