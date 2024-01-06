# S.A.N.J.A.Y - Smart Automated Navigation and Journey Assistant for You

Welcome to the S.A.N.J.A.Y repository! This project is a Smart Automated Navigation and Journey Assistant designed to aid individuals with visual impairments. S.A.N.J.A.Y combines machine learning for image detection, IoT technologies, ultrasonic sensors, a rain sensor, and a buzzer to provide a comprehensive assistance system.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

S.A.N.J.A.Y aims to enhance the mobility and independence of visually impaired individuals by providing real-time environmental information and navigation assistance. The project integrates two ESP32 cameras for image detection, ultrasonic sensors for obstacle detection, a rain sensor, and a buzzer for additional alerts.

## Features

- **Automated Navigation:**
  - The top camera utilizes OpenCV and ImageAI.org for object detection with the YOLO V3 algorithm, identifying vehicles and persons.
  - The lower camera uses OpenCV1 and a Roboflow dataset for pothole and manhole detection.
  - Ultrasonic sensors assist in detecting obstacles in the vicinity.
  - A rain sensor identifies wet surfaces.
  - A buzzer provides audible alerts.

- **IoT Integration:**
  - Two ESP32 cams, one at the top and one at the bottom, serve as Internet of Things devices for real-time data collection and communication.
  - Ultrasonic sensors assist in detecting obstacles in the vicinity.
  - A rain sensor identifies wet surfaces.
  - A buzzer provides audible alerts.

- **Voice Assistance (Planned):**
  - Google Voice Assistant integration is planned for enhanced interaction and guidance.

- **Customization:**
  - Currently, no customization options have been added, but future updates may include user-configurable settings.

## Getting Started

To get started with S.A.N.J.A.Y, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/S.A.N.J.A.Y.git
   cd S.A.N.J.A.Y
Install dependencies:

bash
Copy code
pip install opencv-python requests numpy imageai roboflow
Set up ESP32 cams:

Install necessary libraries for ESP32.
Connect ESP32 cams to the system as described in ESP32 Cam Setup Guide.
Connect sensors:

Connect the ultrasonic sensor, rain sensor, and buzzer to the system as described in Sensor Setup Guide.
Installation
Install Machine Learning Dependencies:

For the top camera (YOLO V3):
Install OpenCV: pip install opencv-python
Install ImageAI: pip install imageai
For the lower camera (Pothole and Manhole Detection):
Install OpenCV1: Mention specific version if needed.
Install any additional libraries required for the Roboflow dataset.
Set Up ESP32 Cams:

Install necessary libraries for ESP32: Mention specific libraries.
Connect ESP32 cams to the system as described in ESP32 Cam Setup Guide.
Connect Sensors:

Connect the ultrasonic sensor, rain sensor, and buzzer to the system as described in Sensor Setup Guide.
Voice Assistant (Planned):

Google Voice Assistant integration is planned for future releases.
Usage
Run the application:

Mention how to start the application.
Navigation:

Follow the on-screen or voice instructions for navigation.
Contributing
We welcome contributions! If you'd like to contribute to S.A.N.J.A.Y, please follow our Contribution Guidelines.

License
This project is licensed under the MIT License.

Feel free to reach out if you have any questions or feedback. Happy coding!
