import speech_recognition as sr
sr.get_flac_converter = lambda: "/opt/homebrew/bin/flac"

print("🎙️ EduVoice AI Microphone Test")
print("--------------------------------")

recognizer = sr.Recognizer()

try:
    with sr.Microphone() as source:

        print("Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("🎤 Listening...")
        print("Speak now!")

        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=10
        )

    print("✅ Recording completed.")
    print("Converting speech to text...")

    text = recognizer.recognize_google(audio)

    print()
    print("You said:")
    print(text)

except sr.WaitTimeoutError:
    print("❌ No speech detected within the timeout.")

except sr.UnknownValueError:
    print("❌ I could not understand the audio.")

except sr.RequestError as e:
    print("❌ Speech recognition service error:")
    print(e)

except Exception as e:
    print("❌ Error:")
    print(e)

