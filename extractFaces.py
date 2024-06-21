import cv2
import os

# Load pre-trained face detector


def detectFaces(video_path, studentId):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open video file
    cap = cv2.VideoCapture(video_path)

    # Directory to save detected face images
    output_dir = './detected_faces/student_'+studentId
    os.makedirs(output_dir, exist_ok=True)

    frame_count = 0
    face_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            w_margin_percentage=0.18
            h_margin_percentage=0.25
            face_count += 1
            margin_x = int(w * w_margin_percentage)
            margin_y = int(h * h_margin_percentage)
            
            # Adjust coordinates with margin
            x_start = max(0, x - margin_x)
            y_start = max(0, y - margin_y)
            x_end = min(frame.shape[1], x + w + margin_x)
            y_end = min(frame.shape[0], y + h + margin_y)
            
            # Extract face with margin
            face_img = frame[y_start:y_end, x_start:x_end]
            face_filename = os.path.join(output_dir, f'face_{face_count}.jpg')
            cv2.imwrite(face_filename, face_img)
            
        frame_count += 1
        if face_count > 10:
                break
    cap.release()
    cv2.destroyAllWindows()

    print(f"Processed {frame_count} frames and detected {face_count} faces.")
    return output_dir