from flask import Flask, jsonify, render_template
from ultralytics import YOLO
import cv2
import math
import pyttsx3

app = Flask(__name__)

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

# URL will change with WiFi
esp_cam_url = "http://192.168.61.101/cam-hi.jpg"

Dict = {}

ind = 1

for name in classNames:
    Dict[name] = ind
    ind = ind + 1

engine = pyttsx3.init()

prediction_result = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['GET'])
def object_detection():
    global prediction_result
    try:
        # Capture frame from webcam
        cap = cv2.VideoCapture(esp_cam_url)
        ret, img = cap.read()

        if img is None:
            print('No image received')
            return jsonify({'error': 'No image received'}), 500
        else:
            # Perform object detection
            results = model(img, stream=True)

            # Extract information from the predictions
            objects_detected = [{'ind': Dict[classNames[int(box.cls[0])]],
                                 'confidence': math.ceil((box.conf[0] * 100)) / 100}
                                for r in results for box in r.boxes if math.ceil((box.conf[0] * 100)) / 100>=0.5]

            prediction_result = objects_detected

            if prediction_result is not None:
                # Return the prediction as JSON
                print(prediction_result)
                return jsonify(prediction_result)
            else:
                return jsonify({'error': 'No objects detected'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
