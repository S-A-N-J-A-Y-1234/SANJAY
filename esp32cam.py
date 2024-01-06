import cv2
import requests
import numpy as np
from imageai.Detection import ObjectDetection

# Initialize ObjectDetection model
obj_detect = ObjectDetection()
obj_detect.setModelTypeAsYOLOv3()
obj_detect.setModelPath(r"C:/Datasets/yolo.h5")
obj_detect.loadModel()

# ESP32-CAM URL
esp32_cam_url = "http://192.168.138.52/cam-hi.jpg"

while True:
    try:
        # Fetch frame from ESP32-CAM
        response = requests.get(esp32_cam_url)
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)

        # Perform object detection
        annotated_img, preds = obj_detect.detectObjectsFromImage(input_image=img,
                                                                input_type="array",
                                                                output_type="array",
                                                                display_percentage_probability=True,
                                                                display_object_name=True)

        # Display the annotated frame
        cv2.imshow("Object Detection", annotated_img)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    except Exception as e:
        print(f"Error: {e}")

# Release resources
cv2.destroyAllWindows()
