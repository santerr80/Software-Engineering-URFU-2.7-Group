import streamlit as st
from transformers import pipeline

@st.cache
def load_summarizer(text, model):
    summarizer = pipeline("summarization", model="Falconsai/text_summarization")
    return summarizer(text)
