import whisper
import pyaudio
import wave
import json
import time
from datetime import datetime

def record_audio(output_file="recorded_audio.wav", duration=10, sample_rate=44100, channels=1, chunk_size=1024):
    """Records audio from the microphone and saves it as a .wav file."""
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=pyaudio.paInt16, channels=channels, rate=sample_rate, 
                        input=True, frames_per_buffer=chunk_size)
    
    print("🎙️ Recording...")
    frames = []

    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("✅ Recording finished.")

    # Stop & close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a file
    with wave.open(output_file, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))

    return output_file

def transcribe_audio(audio_file="recorded_audio.wav"):
    """Transcribes the recorded audio using Whisper."""
    model = whisper.load_model("small")  # Choose model size: tiny, base, small, medium, large
    result = model.transcribe(audio_file)
    return result["text"]


# 💾 Step 3: Save Output as JSON
def save_transcription(text, output_json="transcription.json"):
    """Saves the transcribed text with a timestamp as JSON."""
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text
    }

    with open(output_json, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"✅ Transcription saved to {output_json}")

# 🚀 Run Everything
if __name__ == "__main__":
    audio_file = record_audio(duration=600)  # Adjust duration as needed
    transcribed_text = transcribe_audio(audio_file)
    print(transcribed_text)
    save_transcription(transcribed_text,"test.json")


