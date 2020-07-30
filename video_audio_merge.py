import cv2
import time
import subprocess


INPUT_VIDEO_FILE = "output.avi"
INPUT_AUDIO_FILE = "temp_audio.wav"

OUTPUT_FILE = "final_output"

with open("FPS.txt", 'r') as f:
    FPS = float(f.read())

video_cap = cv2.VideoCapture(INPUT_VIDEO_FILE)
timer_start = time.time()

frame_counts = 0

print("Camera_FPS: ", FPS)

while True:
    ret, video_frame = video_cap.read()
    if ret:
        frame_counts += 1
        time.sleep(1/(FPS + 2))
    else:
        break

video_cap.release()
cv2.destroyAllWindows()

elapsed_time = time.time() - timer_start
recorded_fps = frame_counts / elapsed_time
print("total frames " + str(frame_counts))
print("elapsed time " + str(elapsed_time))
print("recorded fps " + str(recorded_fps))


# Merging audio and video signal
if abs(recorded_fps - 6) >= 0.01:    # If the fps rate was higher/lower than expected, re-encode it to the expected
    print("Re-encoding")
    cmd = "ffmpeg -r " + str(recorded_fps) + " -i " + INPUT_VIDEO_FILE + " -pix_fmt yuv420p -r 6 re_encoded_output.avi"
    subprocess.call(cmd, shell=True)
    print("Muxing")
    cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i " + INPUT_AUDIO_FILE + " -i re_encoded_output.avi -pix_fmt yuv420p " + OUTPUT_FILE + ".avi"
    subprocess.call(cmd, shell=True)
else:
    print("Normal recording\nMuxing")
    cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i " + INPUT_AUDIO_FILE + " -i " + INPUT_VIDEO_FILE + " -pix_fmt yuv420p " + OUTPUT_FILE + ".avi"
    subprocess.call(cmd, shell=True)
    print("..")
