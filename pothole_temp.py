import requests
import tempfile
import time
import os
import cv2
from roboflow import Roboflow

# ESP32-CAM URL
esp32_cam_url = "http://192.168.138.52/cam-hi.jpg"

# Roboflow API setup
rf = Roboflow(api_key="sdAMSW7jW177i5NBk4ra")
project = rf.workspace().project("pothole-detection-bqu6s")
model = project.version(9).model

try:
    while True:
        # Fetch frame from ESP32-CAM
        response = requests.get(esp32_cam_url)
        image_bytes = response.content

        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name

        # Make a prediction using the Roboflow API
        response = model.predict(temp_file_path, confidence=40, overlap=30)

        # Process the API response
        api_response = response.json()
        predictions = api_response.get('predictions', [])

        # Print predictions
        print(predictions)

        img = cv2.imread(temp_file_path)

        # Draw bounding boxes based on predictions
        for prediction in predictions:


        # Display the annotated frame
            imageRectangle = img.copy()
            x = prediction['x']
            y = prediction['y']
            w = prediction['width']
            h = prediction['height']
            # define the starting and end points of the rectangle
            start_point = (x,y)
            end_point = (x+w,y+h)

            print(f"{prediction['class']} detected")
            # draw the rectangle
            cv2.rectangle(imageRectangle, start_point, end_point, (0, 0, 255), thickness=3, lineType=cv2.LINE_8)
            # display the output
            # let's write the text you want to put on the image
            class_name = prediction['class']
            confidence = prediction['confidence']
            text = f"{class_name}: {confidence:.2f}"
            # org: Where you want to put the text
            org = (x, y)
            # write the text on the input image
            cv2.putText(imageRectangle, text, org, fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1.5, color=(250, 225, 100))
            # display the output image with text over it

            cv2.imshow('imageRectangle', imageRectangle)
        #
        cv2.imshow("", img)

        if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
            break

        # Wait for a short duration before fetching the next frame
        # time.sleep(1)

finally:
    # Delete the temporary file
    if 'temp_file_path' in locals():
        os.remove(temp_file_path)
