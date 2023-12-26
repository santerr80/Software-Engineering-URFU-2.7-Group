import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_summarizer():
    summarizer = pipeline("summarization", model="Falconsai/text_summarization")
    return summarizer
