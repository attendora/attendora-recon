import cv2
import requests
import time

camera_url = "http://192.168.137.43:81/stream"
control_url = "http://192.168.137.43/control"

def set_camera_resolution(resolution_val):
    response = requests.get(f"{control_url}?var=framesize&val={resolution_val}")
    if response.status_code == 200:
        print(f"Resolution set to {resolution_val}")
    else:
        print(f"Failed to set resolution: {response.status_code}")
        
        
def measure_frame_rate():
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        print("Error: Unable to open video stream")
        return 0

    frame_count = 0
    start_time = time.time()

    while frame_count < 100:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

    end_time = time.time()
    cap.release()
    duration = end_time - start_time
    if duration > 0:
        return frame_count / duration
    else:
        return 0

for resolution in range(5, 11):
    set_camera_resolution(resolution)
    fps = measure_frame_rate()
    print(f"Resolution {resolution}: {fps} FPS")