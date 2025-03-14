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
