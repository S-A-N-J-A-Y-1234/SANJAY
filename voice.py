from flask import Flask, jsonify, render_template
from ultralytics import YOLO
import cv2
import math
import pyttsx3

app = Flask(__name__)

# Replace with the actual URL of your ESP32-CAM stream
esp32cam_url = "http://10.24.38.251/cam-hi.jpg"

# model
model = YOLO("yolo-Weights/yolov8n.pt")

# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

engine = pyttsx3.init()

prediction_result = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['GET'])
def object_detection():
    global prediction_result
    try:
        # Capture frame from ESP32-CAM
        cap = cv2.VideoCapture(esp32cam_url)
        ret, img = cap.read()

        if img is None:
            print('No image received')
            return jsonify({'error': 'No image received'}), 500
        else:
            # Perform object detection
            results = model(img, stream=True)

            # Extract information from the predictions
            objects_detected = [{'name': classNames[int(box.cls[0])],
                                 'confidence': math.ceil((box.conf[0] * 100)) / 100,
                                 'bounding_box': list(map(int, box.xyxy[0]))}
                                for r in results for box in r.boxes]

            prediction_result = objects_detected

            if prediction_result is not None:
                # Convert prediction result to text
                prediction_text = ', '.join([f"{obj['name']} detected" for obj in prediction_result])

                # Use pyttsx3 to directly speak the text
                engine.say(prediction_text)
                engine.runAndWait()

                # Return the prediction as JSON
                return jsonify(prediction_result)
            else:
                return jsonify({'error': 'No objects detected'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
