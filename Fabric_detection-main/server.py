from flask import Flask,render_template, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, template_folder="templates")
CORS(app)  # Enable CORS

# Path to captured images folder
IMAGE_FOLDER = os.path.abspath("captured_images")  # Use absolute path

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")



@app.route('/get_defected_image')
def get_defected_image():
    try:
        # Get the most recent image in the folder
        images = sorted(os.listdir(IMAGE_FOLDER), key=lambda x: os.path.getmtime(os.path.join(IMAGE_FOLDER, x)), reverse=True)
        
        if not images:
            return jsonify({"error": "No images found"}), 404
        
        latest_image = images[0]  # Get the latest image
        return send_from_directory(IMAGE_FOLDER, latest_image)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
