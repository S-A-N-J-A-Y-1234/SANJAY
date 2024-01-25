from flask import Flask, jsonify, render_template
from roboflow import Roboflow
import cv2
import math
import pyttsx3
import requests
import numpy as np
from io import BytesIO

app = Flask(__name__)

# Replace with the actual URL of your ESP32-CAM stream
esp32cam_url = "http://10.24.38.251/cam-hi.jpg"

# Roboflow API setup
rf = Roboflow(api_key="3pr3aIfRs4KhkiRPT6w6")
project = rf.workspace().project("pothole-detection-bqu6s")
model = project.version(9).model

# object classes
classNames = ["pothole","Drain Hole","circle-drain-clean-","drain-clean-","drain-not-clean-","hole","manhole","sewer cover"]

prediction_result = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['GET'])
def object_detection():
    global prediction_result
    try:
        # Capture frame from ESP32-CAM
        response = requests.get(esp32cam_url)

        # Check if the request was successful
        if response.status_code == 200:
            image_bytes = response.content

            # Convert image bytes to numpy array
            image_np = np.frombuffer(image_bytes, dtype=np.uint8)
            img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

            # Make a prediction using the Roboflow API
            prediction_group = model.predict(img, confidence=40, overlap=30)

            # Check if there are predictions in the group
            if prediction_group.predictions:
                # Process the API response
                predictions = prediction_group.predictions

                # Extract information from the predictions
                objects_detected = [{'name': prediction['class'],
                                     'confidence': prediction['confidence'],
                                     'bounding_box': [prediction['x'], prediction['y'], prediction['width'], prediction['height']]}
                                    for prediction in predictions]

                prediction_result = objects_detected

                if prediction_result:
                    # Convert prediction result to text
                    prediction_text = ', '.join([f"{obj['name']} detected" for obj in prediction_result])

                    # Use pyttsx3 to directly speak the text
                    engine = pyttsx3.init()
                    engine.say(prediction_text)
                    engine.runAndWait()

                    # Return the prediction as JSON
                    print(prediction_result)
                    return prediction_result
                else:
                    return jsonify({'error': 'No objects detected'})

            else:
                return jsonify({'error': 'No objects detected'})

        else:
            return jsonify({'error': 'Failed to fetch image from ESP32-CAM'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
