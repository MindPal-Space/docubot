#write code that input is a long string, return a list of its chunk 
def split_text(text: str, chunk_size: int = 200, chunk_overlap: int = 50) -> list:
    
    """
    Splits a long string into chunks with a specified size and overlap.
    
    Args:
    text (str): The long string to be split.
    chunk_size (int): The desired size of each chunk.
    chunk_overlap (int): The desired overlap between adjacent chunks.
    
    Returns:
    A list of string chunks.
    """
    words = text.split(" ")
    chunks = []
    start = 0
    end = chunk_size
    
    while end <= len(words):
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - chunk_overlap
        end += chunk_size - chunk_overlap
    
    if end > len(words) and start < len(words):
        chunks.append(" ".join(words[start:]))
    
    return chunks

