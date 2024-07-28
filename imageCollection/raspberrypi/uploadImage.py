import os.path as op
import sys
path  = op.dirname(op.dirname(op.realpath(__file__)))
sys.path.append(path)

from firebase import storage
import constants

import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify
from picamera2 import Picamera2

app = Flask(__name__)
picam2 = Picamera2()

@app.route('/take_photo', methods=['GET'])
def take_photo():

	picam2.start_and_capture_file(constants.LOCAL_FILE_PATH)
	storage.child(constants.PATH_ON_CLOUD).put(constants.LOCAL_FILE_PATH)
	return jsonify({"status": "success", "message": "Photo taken"}), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.getenv("FLASK_PORT"))
