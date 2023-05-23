import subprocess
command = "streamlit run YOUTUBE_STREAMLIT_app.py"
subprocess.Popen(['cmd', '/c', command])
subprocess.wait()
