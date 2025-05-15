from flask import Flask, jsonify, send_from_directory, request, render_template
import os

app = Flask(__name__)

# Caminho da pasta da rede
MIDIA_FOLDER = r"//192.168.30.80/gerinfo/SUPORTE/midia"

# Extensões aceitas
VIDEO_EXTENSIONS = ('.mp4', '.webm', '.mov')
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif')

# Página inicial - TV ou interface comum
@app.route("/")
def index():
    if request.args.get("tv") == "true":
        return render_template("tv.html")  # Exibe reprodutor na TV
    return render_template("index.html")   # Tela padrão com login ou outra

# API para listar os arquivos da pasta de mídia
@app.route("/api/midias")
def listar_midias():
    midias = []
    for filename in os.listdir(MIDIA_FOLDER):
        path = os.path.join(MIDIA_FOLDER, filename)
        if not os.path.isfile(path):
            continue
        ext = os.path.splitext(filename)[1].lower()
        if ext in VIDEO_EXTENSIONS:
            midias.append({"url": f"/midias/{filename}", "type": "video"})
        elif ext in IMAGE_EXTENSIONS:
            midias.append({"url": f"/midias/{filename}", "type": "image"})
    return jsonify(midias)

# Rota para servir os arquivos da pasta de mídia
@app.route("/midias/<path:filename>")
def servir_midia(filename):
    return send_from_directory(MIDIA_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
