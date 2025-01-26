import pyaudio
import wave

def record_audio(output_wav="output.wav", duration=10, rate=44100, chunk=1024):
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open the stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print(f"Recording for {duration} seconds...")

    frames = []

    # Record the audio
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save to WAV
    with wave.open(output_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b"".join(frames))

    print(f"Saved WAV file as {output_wav}.")

record_audio(duration=5)