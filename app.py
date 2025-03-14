from flask import Flask, request, send_file
import os
import subprocess
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/convert", methods=["POST"])
def convert_audio():
    if "file" not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files["file"]
    
    # Log detalhes do arquivo recebido
    print(f"Arquivo recebido - Nome: {file.filename}, Tipo: {file.content_type}, Tamanho: {len(file.read())} bytes")
    file.seek(0)  # Volta ao início do arquivo após ler o conteúdo

    format = request.form.get("format", "wav")
    if format not in ["wav", "aac", "mpga"]:
        return {"error": "Invalid format"}, 400

    # Gera um nome seguro ou usa um UUID se o nome estiver vazio
    if file.filename.strip() == '':
        filename = f"audio_{uuid.uuid4().hex}"
        print(f"Nome do arquivo vazio. Usando nome gerado: {filename}")
    else:
        filename = secure_filename(file.filename)
        print(f"Nome do arquivo após secure_filename: {filename}")

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_filename = f"{os.path.splitext(filename)[0]}.{format}"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)

    try:
        file.save(input_path)
        print(f"Arquivo salvo em: {input_path}")
    except Exception as e:
        return {"error": f"Erro ao salvar o arquivo: {str(e)}"}, 500

    # Executa o FFmpeg
    try:
        subprocess.run(
            ["ffmpeg", "-i", input_path, "-y", output_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Conversão concluída. Saída salva em: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Erro na conversão: {e.stderr.decode()}")
        return {"error": "Falha na conversão"}, 500

    if not os.path.exists(output_path):
        return {"error": "Arquivo de saída não gerado"}, 500

    return send_file(output_path, as_attachment=True, download_name=output_filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
