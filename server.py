import pyaudio
import wave
import os
from flask import Flask
from threading import Thread, Event
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='server.log', level=logging.DEBUG)

# Configuration
CHUNK = 1024  # Record in chunks of 1024 samples
FORMAT = pyaudio.paInt16  # 16 bits per sample
CHANNELS = 1
RATE = 44100  # Record at 44100 samples per second
OUTPUT_DIR = "recordings"
RECORD_FILE = "recording.wav"

recording_event = Event()
stop_event = Event()
frames = []

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def record_audio():
    global frames
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    logging.info("Recording started...")
    frames = []

    while not stop_event.is_set():
        if recording_event.is_set():
            data = stream.read(CHUNK)
            frames.append(data)
            logging.debug("Recording data chunk")
        else:
            if frames:
                logging.info("Recording event cleared, saving audio")
                save_audio(frames, p)
                frames = []

    logging.info("Recording stopped.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    if frames:
        save_audio(frames, p)

def save_audio(frames, p):
    file_path = os.path.join(OUTPUT_DIR, RECORD_FILE)
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    logging.info(f"Audio saved to {file_path}")

@app.route('/start', methods=['POST'])
def start_recording():
    recording_event.set()
    logging.info("Recording event set")
    return "Recording started"

@app.route('/stop', methods=['POST'])
def stop_recording():
    recording_event.clear()
    logging.info("Recording event cleared")
    return "Recording stopped"

def start_server():
    logging.info("Starting server...")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    server_thread = Thread(target=start_server)
    server_thread.start()
    record_audio()
