import cohere 
from langchain.embeddings import CohereEmbeddings


def init_cohere_embedding(COHERE_API_KEY: str):
    embedding = CohereEmbeddings(model="small", cohere_api_key=COHERE_API_KEY)
    return embedding
