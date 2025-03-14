from flask import Flask, request, send_file
import os
import subprocess
from werkzeug.utils import secure_filename

# Inicializa o app Flask
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/convert", methods=["POST"])
def convert_audio():
    if "file" not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files["file"]
    
    # Verifique o nome do arquivo e o tipo
    if file.filename == '':
        return {"error": "No selected file"}, 400

    # Verifique se o arquivo tem conteúdo
    if file:
        print(f"Arquivo recebido: {file.filename}, tipo: {file.content_type}")

    format = request.form.get("format", "wav")  # Padrão: WAV

    if format not in ["wav", "aac", "mpga"]:
        return {"error": "Invalid format"}, 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(UPLOAD_FOLDER, f"{os.pat
