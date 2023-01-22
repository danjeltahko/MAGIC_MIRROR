import subprocess

subprocess.run(["xrandr", "-o", "left"])
subprocess.Popen(["python3", "app.py", "server_process"])
subprocess.Popen(["chromium-browser", "--start-fullscreen", "http://localhost:1312"])

