import os
import json
from flask import Flask, render_template, request
from flask import jsonify
from audio import converter
from asr import recognizer

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/voice', methods=['POST'])
def voice():
    if request.method == 'POST':
        f = request.files['voice']

        wf = converter.convert_to_wav(f.stream)
        results = recognizer.recognize(wf)
        print('RESULTS', results)
        return jsonify(data=results)
    return jsonify(error="no data")


if __name__ == '__main__':
    if not os.path.exists("model"):
        print("Please download the model from https://alphacephei.com/vosk/models.")
        exit(1)
    # app.run(host='0.0.0.0')
    app.run()
