import streamlit as st
from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from pydub import AudioSegment
import io


translator = Translator()

st.title("Text Translation & Transcription App")
st.write("built using Streamlit")

activity = st.sidebar.radio("Select Activity", ("Text Translation📄", "Audio Transcription🎤"))

if activity == "Text Translation📄":
    st.write("Enter text to translate:")
    
    input_text = st.text_area("Input Text", "")
    
    language_options = list(LANGUAGES.keys())
    language_names = [f"{LANGUAGES[lang]} ({lang})" for lang in language_options]
    target_language = st.selectbox("Select Target Language", language_names)
    
    selected_language_code = language_options[language_names.index(target_language)]
    
    if st.button("Translate"):
        if input_text:
            
            translated = translator.translate(input_text, dest=selected_language_code)
            st.write("Translated Text:")
            st.success(translated.text)
        else:
            st.warning("Please enter some text to translate.")

elif activity == "Audio Transcription🎤":
    st.write("Transcription methods:")
    
    transcription_method = st.radio("Choose method",("Real-Time Transcription", "Upload Audio File"))

    if transcription_method == "Real-Time Transcription":
        st.write("Press the button below and start speaking:")
        
        if st.button("Start Transcription"):
            recognizer = sr.Recognizer()
            mic = sr.Microphone()

            with mic as source:
                recognizer.adjust_for_ambient_noise(source) 
                st.info("Listening...")
                audio_data = recognizer.listen(source)  

                try:
                    transcription = recognizer.recognize_google(audio_data)
                    st.write("Transcribed Text:")
                    st.success(transcription)
                except sr.UnknownValueError:
                    st.error("Google Speech Recognition could not understand the audio.")
                except sr.RequestError as e:
                    st.error(f"Could not request results from Google Speech Recognition service; {e}")

    elif transcription_method == "Upload Audio File":
        st.write("Upload an audio file for transcription:")
        
        audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])
        
        if audio_file is not None:
        
            audio_bytes = io.BytesIO(audio_file.read())
            audio_segment = AudioSegment.from_file(audio_bytes)
            
            wav_audio_path = "temp_audio.wav"
            audio_segment.export(wav_audio_path, format="wav")

            recognizer = sr.Recognizer()

            with sr.AudioFile(wav_audio_path) as source:
                audio_data = recognizer.record(source) 
                
                try:
                    transcription = recognizer.recognize_google(audio_data)
                    st.write("Transcribed Text:")
                    st.success(transcription)
                except sr.UnknownValueError:
                    st.error("Google Speech Recognition could not understand the audio.")
                except sr.RequestError as e:
                    st.error(f"Could not request results from Google Speech Recognition service; {e}")