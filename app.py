import os
from flask import Flask, send_file

app = Flask(__name__)


@app.route("/")
def serve_json():
    return send_file("current_results.json", mimetype="application/json")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
