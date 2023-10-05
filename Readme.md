# Liveness Detection 

This project implements liveness detection  techniques. It utilizes PyQt5 for the graphical user interface, OpenCV for camera input and image processing, and MediaPipe for face mesh detection.

## Prerequisites

Make sure you have the following libraries installed before running the application:

- PyQt5
- OpenCV (`cv2`)
- mediapipe
- numpy

You can install these libraries using `pip`:

```bash
pip install -r requirements.txt
```

## How to Run

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ioptime-official/face_liveness_detection.git
   cd liveness-detection-with-face-recognition
   ```

2. **Run the Application:**
   ```bash
   python main.py
   ```

## Project Structure

- `app_pages/`: Contains the UI files for the application.
- `images/`: Contains images used in the application.
- `modules/`: Contains helper modules and functions used in the project.

## File Descriptions

- **main.py:** The main entry point of the application. Run this file to start the liveness detection application.
- **app_pages/liveness_start.ui:** UI file for the start page of the application.
- **app_pages/liveness_tryagain.ui:** UI file for the retry page displayed when liveness detection fails or success.
- **app_pages/liveness_main.ui:** UI file for the main liveness detection page.
- **modules/list_random.py:** Helper function to generate random lists of actions for liveness detection.
- **README.md:** Project documentation.

## How to Use

1. **Start Page:**
   - The application starts with the start page displaying an image related to the liveness detection process.
   - Click the "Start" button to begin liveness detection.

2. **Liveness Detection Page:**
   - The camera feed will be displayed on this page.
   - Follow the on-screen instructions to perform specific actions (e.g., look left, look right).
   - The application detects your facial movements and prompts you to perform different actions.
   - If you successfully complete the required actions, you will be redirected to the success page.

3. **Success Page:**
   - Displays a success message when liveness detection is successful.
   - Click the "Return" button to go back to the start page and perform liveness detection again.

## Additional Information

- The application uses the MediaPipe library for face mesh detection to analyze facial movements.
- Ensure good lighting conditions and a clear view of your face for accurate detection.
