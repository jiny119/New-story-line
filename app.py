import streamlit as st
import torch
from transformers import pipeline
from gtts import gTTS
import tempfile
import os

# Function to generate story
def generate_story(title):
    try:
        generator = pipeline("text-generation", model="facebook/opt-1.3b")
        prompt = f"ایک دلچسپ اردو کہانی جس کا عنوان '{title}' ہے:"
        story = generator(prompt, max_length=500, do_sample=True)[0]['generated_text']
        return story
    except Exception as e:
        return f"Error: {str(e)}"

# Function to convert text to speech
def text_to_speech(text):
    try:
        tts = gTTS(text, lang="ur")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        return None

# Streamlit UI
st.title("اردو کہانی جنریٹر")
title = st.text_input("کہانی کا عنوان درج کریں:", "پراسرار جنگل")

if st.button("کہانی بنائیں"):
    with st.spinner("کہانی بن رہی ہے..."):
        story = generate_story(title)
        st.write(story)

        audio_file = text_to_speech(story)
        if audio_file:
            st.audio(audio_file, format="audio/mp3")
            os.remove(audio_file)
        else:
            st.error("آواز بنانے میں مسئلہ ہوا۔")

st.write("© 2025 - اردو کہانی جنریٹر")
