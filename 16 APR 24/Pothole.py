from flask import Flask, jsonify, render_template
from roboflow import Roboflow
import cv2
import numpy as np
import math

app = Flask(__name__)

# URL changes with WiFi
esp32cam_url = "http://192.168.61.52/cam-hi.jpg"


# Roboflow API setup
rf = Roboflow(api_key="3pr3aIfRs4KhkiRPT6w6")
project = rf.workspace().project("pothole-detection-bqu6s")
model = project.version(9).model

# Object classes
classNames = ["Pothole", "Drain Hole", "circle-drain-clean-", "drain-clean-", "drain-not-clean-", "hole", "manhole", "sewer cover"]

Dict = {}

ind = 81

for name in classNames:
    Dict[name] = ind
    ind = ind + 1

prediction_result = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['GET'])
def object_detection():
    global prediction_result
    try:
        # Capture frame from webcam
        webcam = cv2.VideoCapture(esp32cam_url)
        ret, frame = webcam.read()

        if ret:
            # Convert frame to grayscale
            print("frame captured")
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Make a prediction using the Roboflow API
            prediction_group = model.predict(frame, confidence=40, overlap=30)

            # Check if there are predictions in the group
            if prediction_group.predictions:
                # Process the API response
                print("entered in pre_grp")
                predictions = prediction_group.predictions

                # Extract information from the predictions
                objects_detected = [{'name': prediction['class'],
                                     'ind': Dict[prediction['class']],
                                     'confidence': prediction['confidence']
                                     }
                                    for prediction in predictions if prediction['confidence']>=0.5]

                prediction_result = objects_detected

                if prediction_result:
                    # Convert prediction result to text
                    prediction_text = ', '.join([f"{obj['name']} detected" for obj in prediction_result])

                    # Return the prediction as JSON
                    print(prediction_result)
                    return jsonify(prediction_result)
                else:
                    return jsonify({'error': 'No objects detected'})
            else:
                return jsonify({'error': 'No objects detected 2'})
        else:
            return jsonify({'error': 'Failed to capture frame from webcam'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
