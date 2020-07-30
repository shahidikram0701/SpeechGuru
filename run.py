import subprocess


print("Record Input")
print("-" * 100)
subprocess.call("python videoRecorder.py", shell=True)
print("\n")

print("Process video")
print("-" * 100)
subprocess.call("python detect_track_face.py", shell=True)
subprocess.call("python video_audio_merge.py", shell=True)
print("\n\n Check final_cut.avi \n")

print("Process audio")
print("-" * 100)
subprocess.call("python process.py > report.txt", shell=True)
print("\n\n Check report.txt \n")