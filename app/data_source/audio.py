import os

from dotenv import load_dotenv
from deepgram import Deepgram


#you can get a Deepgram API key for free here: https://deepgram.com/ . After signing up, you will get 200$ free credits to use

def extract_text_from_audio(audio_file_path: str) -> str:
    """
    Function to get the transcript from audio/video file
    Args:
        audio_file_path (str): the file path of the audio/video file
    Returns:
        transcript (str): the transcript of the audio/video file
    """
    deepgram = Deepgram(os.environ.get("DEEPGRAM_API_KEY"))
    with open(audio_file_path, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = deepgram.transcription.prerecorded(source, {'punctuate': True})

    transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    return transcript

