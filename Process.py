import ollama
import gradio as gr
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def chunking_data(text):
    full_text = " ".join(text)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = text_splitter.split_text(full_text)

    return chunks


def find_most_relevant_chunks(user_query, chunks, top_k=3):
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')

    chunk_embeddings = embed_model.encode(chunks)


    query_embedding = embed_model.encode([user_query])


    similarities = cosine_similarity(query_embedding, chunk_embeddings)[0]

    top_indices = np.argsort(similarities)[-top_k:][::-1]

    relevant_chunks = [chunks[i] for i in top_indices]

    return relevant_chunks