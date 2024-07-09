from langchain_cohere import CohereEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def get_embedding():
    embeddings = CohereEmbeddings(cohere_api_key=os.environ.get("API_KEY"),model="embed-english-light-v3.0")
    return embeddings