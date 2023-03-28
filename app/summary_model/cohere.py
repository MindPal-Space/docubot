import cohere 

COHERE_API_KEY = "QTojHkqZdAQydK5TNLqlD99tvsaBRbyU6TaDFG35"
#you can get a free API key here: https://cohere.ai/ . After signing up, you can use the trial API key for free 

co = cohere.Client(COHERE_API_KEY) 

def summarize_short(text):
    """
    Function to summarize the text to bullet points (short version)
    Args:
        text (str): the text to summarize
    Returns:
        response.summary (str): the summary of the text
    """
    response = co.summarize( 
    text=text,
    length='short',
    format='bullets',
    model='summarize-xlarge',
    additional_command='',
    temperature=0.2,
    ) 
    return response.summary

def summarize_medium(text):
    """
    Function to summarize the text to bullet points (medium version)
    Args:
        text (str): the text to summarize
    Returns:
        response.summary (str): the summary of the text
    """
    response = co.summarize( 
    text=text,
    length='medium',
    format='bullets',
    model='summarize-xlarge',
    additional_command='',
    temperature=0.2,
    ) 
    return response.summary

def summarize_long(text):
    """
    Function to summarize the text to bullet points (long version)
    Args:
        text (str): the text to summarize
    Returns:
        response.summary (str): the summary of the text
    """
    response = co.summarize( 
    text=text,
    length='long',
    format='bullets',
    model='summarize-xlarge',
    additional_command='',
    temperature=0.2,
    ) 
    return response.summary

def cohere_summarize(text):
    words = text.split(" ")
    if len(words) < 1500:
        summary = summarize_short(text)
    elif len(words) < 8000:
        summary = summarize_medium(text)
    else:
        summary = summarize_long(text)
    return summary
