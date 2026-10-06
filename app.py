
import streamlit as st
import os
import subprocess
from dotenv import load_dotenv
from google import genai
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
import threading
def speak_with_stop(text):
    speech = subprocess.Popen(["say", text])
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        while speech.poll() is None:
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=2)
                command = recognizer.recognize_google(audio).lower()

                if "stop" in command:
                    speech.terminate()
                    break
            except:
                pass

# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Check API key
if not API_KEY:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

# Connect to Gemini
client = genai.Client(api_key=API_KEY)

# Page settings
st.set_page_config(
    page_title="EduVoice AI",
    page_icon="🎓",
    layout="centered"
)

# Title
st.title("🎓 EduVoice AI")
st.subheader("AI Voice Assistant for Students")

st.write("Ask any academic question and EduVoice AI will help you.")

# Question box
if "question_box" not in st.session_state:
    st.session_state.question_box = ""
question = st.text_area(
    "Enter your question:",
    placeholder="Example: Explain the Hall effect in simple words",
    key="question_box"
)
# Voice input
audio = mic_recorder(
    start_prompt="🎤 Speak",
    stop_prompt="⏹️ Stop",
    just_once=True,
    format="wav"
)

if audio:
    recognizer = sr.Recognizer()
    audio_data = audio["bytes"]

    with sr.AudioFile(io.BytesIO(audio_data)) as source:
        recorded_audio = recognizer.record(source)

    try:
        question = recognizer.recognize_google(recorded_audio)
        st.success("You said: " + question)
    except:
        st.error("Sorry, I could not understand your voice.")
# Ask button
if st.button("🤖 Ask EduVoice AI"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:
       response = None

       with st.spinner("Generating answer..."):
          try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=question
            )
          except Exception as e:
            st.error("Something went wrong.")

    if response is not None:
        st.success("Answer")
        st.write(response.text)
        speak_with_stop(response.text)
           
# Extra sections
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.write("📝 Notes")
    st.write("Generate simple study notes.")

with col2:
    st.write("📅 Study Plan")
    st.write("Create a personalized study plan.")

st.divider()

st.caption("EduVoice AI • Student Assistant")
