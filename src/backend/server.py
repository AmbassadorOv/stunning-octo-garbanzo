from flask import Flask, request, send_file
import subprocess
import os
import tempfile

app = Flask(__name__, static_folder='../../ui/build', static_url_path='/')

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/run-agent", methods=["POST"])
def run_agent():
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".tsv") as temp_input:
        file.save(temp_input.name)
        input_path = temp_input.name

    output_path = tempfile.mktemp(suffix=".tsv")

    try:
        subprocess.run(
            [
                "python",
                "src/digital_agent/main.py",
                input_path,
                output_path,
            ],
            check=True,
        )
        return send_file(output_path, mimetype="text/tab-separated-values")
    except subprocess.CalledProcessError as e:
        return f"Error running agent: {e}", 500
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    app.run(port=5001)