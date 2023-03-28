import pytube 
from youtube_transcript_api import YouTubeTranscriptApi

def extract_text_from_youtube(youtube_url: str) -> str:
    """
    Function to get the Youtube transcript from Youtube video URL
    Args:
        youtube_url (str): the url of the Youtube video
    Returns:
        result (str): the transcipt of the Youtube video
    """
    video_id = pytube.YouTube(youtube_url).video_id
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    for transcript in transcript_list:
        result = transcript.fetch()
        if result:
            break
    transcript = format_transcript(result)
    return transcript

  


def format_transcript(result: list) -> str:
    transcript = ""
  
    for sentence in result:
        transcript += sentence["text"] + " "
    
    return transcript
