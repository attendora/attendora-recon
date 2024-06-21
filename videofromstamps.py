import cv2

video_path = 'video.mp4'
time_stamp = 10 # seconds in video

def get_frame_at_timestamp(video_path, timestamp):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = int(timestamp * fps)
    for i in range(int(5 * fps)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number+i)
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Frame at timestamp', frame)
    cap.release()

get_frame_at_timestamp(video_path, time_stamp)