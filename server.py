from flask import Flask, request, jsonify
import cv2
import threading
import time
import requests
import os
from checkFaces import checkFaces
from extractFaces import detectFaces

app = Flask(__name__)

output_dir = "./recordings"
sessions = {}

def set_camera_resolution(resolution_val, control_url):
    response = requests.get(f"{control_url}?var=framesize&val={resolution_val}")
    if response.status_code == 200:
        print(f"Resolution set to {resolution_val}")
    else:
        print(f"Failed to set resolution: {response.status_code}")

def set_led_intensity(intensity_val, control_url):
    response = requests.get(f"{control_url}?var=led_intensity&val={intensity_val}")
    if response.status_code == 200:
        print(f"LED intensity set to {intensity_val}")
    else:
        print(f"Failed to set LED intensity: {response.status_code}")

def set_virtical_flip(control_url):
    response = requests.get(f"{control_url}?var=vflip&val=1") #http://192.168.137.241/control?var=vflip&val=1
    if response.status_code == 200:
        print(f"image flipped vertically")
    else:
        print(f"Failed to flip image")

def measure_frame_rate(camera_url):
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

def record_video(session_id, fps, camera_url):
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        print("Error: Unable to open video stream")
        sessions[session_id]["recording"] = False
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(f"{output_dir}/{session_id}.avi", cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width, frame_height))

    sessions[session_id]["video_writer"] = out

    while sessions[session_id]["recording"]:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    sessions[session_id]["video_path"] = f"{output_dir}/{session_id}.avi"
    sessions[session_id]["recording"] = False

def faceRekon(session_id, student_id):
    video_path = sessions[session_id]["video_path"]
    output_folder = detectFaces(video_path, student_id)
    reference_image_folder = "./reference"
    os
    return checkFaces(reference_image_folder, output_folder)


@app.route('/start_session', methods=['POST'])
def start_session():
    session_id = request.json.get('session_id')
    ipAddr = request.json.get('ipAddr')
    
    camera_url = f"http://{ipAddr}:81/stream"
    control_url = f"http://{ipAddr}/control"

    if session_id in sessions and sessions[session_id]["recording"]:
        return jsonify({"error": "Session already recording"}), 400

    if session_id not in sessions:
        sessions[session_id] = {}

    sessions[session_id]["start_time"] = time.time()
    sessions[session_id]["recording"] = True
    sessions[session_id]["video_writer"] = None

    set_camera_resolution(7, control_url)  # Set camera resolution if needed
    set_led_intensity(255, control_url) # Set LED intensity if needed

    fps = measure_frame_rate(camera_url= camera_url)
    if fps == 0:
        return jsonify({"error": "Failed to measure frame rate"}), 500

    record_thread = threading.Thread(target=record_video, args=(session_id, fps, camera_url))
    record_thread.start()

    return jsonify({"message": "Session recording started", "fps": fps}), 200

@app.route('/end_session', methods=['POST'])
def end_session():
    session_id = request.json.get('session_id')
    student_id = request.json.get('student_id')

    if session_id not in sessions or not sessions[session_id]["recording"]:
        return jsonify({"error": "Session not found or not recording"}), 404

    sessions[session_id]["recording"] = False

    # Allow time for the recording thread to finish
    time.sleep(1)

    bool=faceRekon(session_id, student_id)
    return jsonify({
        "message": "Processing complete",
        "result": bool
        }), 200

if __name__ == '__main__':
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    app.run(host='0.0.0.0', port=5000)
