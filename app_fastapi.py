from fastapi import FastAPI
from contextlib import asynccontextmanager
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import streamlit as st

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    https://fastapi.tiangolo.com/advanced/events/#alternative-events-deprecated
    """
    # Load the summarization model
    ml_models['summarizer'] = pipeline('summarization', model='Falconsai/text_summarization')

    # Load the translation model
    ml_models['translator'] = pipeline('translation_ru_to_en', model='Helsinki-NLP/opus-mt-en-ru')
    yield

    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)


@app.get("/summarize")
async def summarize(video_id: str, translate: bool = False):
    # Load the transcription of a video
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = ' '.join([dictionary['text'] for dictionary in transcript])

    # Summarize the transcription
    summarized = ml_models['summarizer'](transcript_text,
                                        max_length=130,
                                        min_length=30,
                                        do_sample=False)
    summarized = summarized[0]['summary_text']

    if translate:
        # Translate to russian
        summarized = ml_models['translator'](summarized)
        summarized = summarized[0]["translation_text"]

    return summarized
