import pyaudio
import wave

# def record_audio(rate=44100, chunk=1024):
#     # Initialize PyAudio
#     p = pyaudio.PyAudio()

#     # Open the stream
#     stream = p.open(format=pyaudio.paInt16,
#                     channels=1,
#                     rate=rate,
#                     input=True,
#                     frames_per_buffer=chunk)

#     print("Recording...")

#     frames = []

#     # Record the audio
#     for _ in range(0, int(rate / chunk * duration)):
#         data = stream.read(chunk)
#         frames.append(data)

#     print("Recording finished.")

#     # Stop and close the stream
#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     # Save to WAV
#     with wave.open(output_wav, "wb") as wf:
#         wf.setnchannels(1)
#         wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
#         wf.setframerate(rate)
#         wf.writeframes(b"".join(frames))

#     print(f"Saved WAV file as {output_wav}.")


# OLD -----------


import speech_recognition as sr
import soundManager as sm

# Initialize recognizer
recognizer = sr.Recognizer()

def adjust_bg_noise():
    print("Adjusting to noise...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

def call_for_voice_input(stt_abbreviation):
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        sm.play_sfx('Start recording')
        
        # Adjust parameters to optimize recognition of full sentences
        recognizer.pause_threshold = 2  # Allow natural pauses of up to 1 second
        recognizer.dynamic_energy_threshold = True  # Dynamically adjust for ambient noise

        try:
            # Listen for a phrase with a timeout of 5 seconds (change as needed)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Use Google's API to recognize the speech
            recognition = recognizer.recognize_google(audio, language=stt_abbreviation)
            print('API call made (Speech Recognition)')
            return recognition
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out")
            return None
