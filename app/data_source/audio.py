from deepgram import Deepgram

DEEPGRAM_API_KEY = "API_KEY" 
#you can get a Deepgram API key for free here: https://deepgram.com/ . After signing up, you will get 150$ free credits to use

def extract_text_from_audio(audio_file_path: str) -> str:
    """
    Function to get the transcript from audio/video file
    Args:
        audio_file_path (str): the file path of the audio/video file
    Returns:
        transcript (str): the transcript of the audio/video file
    """
    # Initializes the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    # Open the audio file
    with open(audio_file_path, 'rb') as audio:
        # ...or replace mimetype as appropriate
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = deepgram.transcription.prerecorded(source, {'punctuate': True})

    transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    return transcript

