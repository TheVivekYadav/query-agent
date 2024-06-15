# -*- coding: utf-8 -*-
"""query_agent.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/109xmBHJrJ5rovd52aW6qXzNdagG66W1Z
"""

import google.generativeai as palm
palm.configure(api_key='AIzaSyD8C0qP40JCjPLdz0VM8Wk4Yy5AJ9rWPIM')
import json
import faiss
import torch
from sentence_transformers import SentenceTransformer

# Load pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index
index = faiss.read_index('data/faiss_index.index')

# Load segments
with open('data/segments.json', 'r') as f:
    segments = json.load(f)

def query_index(query):
    # Convert query to embedding
    query_embedding = model.encode([query], convert_to_tensor=True).numpy()

    # Search in FAISS index
    _, indices = index.search(query_embedding, k=5)

    # Retrieve top segments
    retrieved_segments = [segments[i] for i in indices[0]]
    return retrieved_segments

def generate_response(query):
    retrieved_segments = query_index(query)
    context = ' '.join(retrieved_segments)

    response = palm.generate_text(
        model="models/text-bison-001",
        prompt=f"Answer the following question based on the context provided:\n\nContext: {context}\n\nQuestion: {query}\n\nAnswer:",
        max_output_tokens=200
    )
    return response.result.strip()

# Example query
query = "What are some milestone model architectures and papers in the last few years?"
response = generate_response(query)
print(response)

def generate_response_with_citations(query):
    retrieved_segments = query_index(query)
    context = ' '.join(retrieved_segments)
    
    response = palm.generate_text(
        model="models/text-bison-001",
        prompt=f"Answer the following question based on the context provided:\n\nContext: {context}\n\nQuestion: {query}\n\nAnswer with references to the context:",
        max_tokens=200
    )
    
    answer = response.result.strip()
    citations = {i: seg for i, seg in enumerate(retrieved_segments)}
    return answer, citations
    
# Example query
query = "What are the layers in a transformer block?"
answer, citations = generate_response_with_citations(query)
print(f"Answer: {answer}")
print(f"Citations: {citations}")

class ConversationalAgent:
    def _init_(self):
        self.context = []

    def query_index(self, query):
        query_embedding = model.encode([query], convert_to_tensor=True).numpy()
        _, indices = index.search(query_embedding, k=5)
        with open('data/segments.json', 'r') as f:
            segments = json.load(f)
        retrieved_segments = [segments[i] for i in indices[0]]
        return retrieved_segments

    def generate_response(self, query):
        retrieved_segments = self.query_index(query)
        self.context.extend(retrieved_segments)
        context = ' '.join(self.context[-10:])  # Use last 10 segments for context
        response = palm.generate_text(
        model="models/text-bison-001",
        prompt=f"Answer the following question based on the context provided:\n\nContext: {context}\n\nQuestion: {query}\n\nAnswer:",
        max_output_tokens=200
        )
        return response.result.strip()

agent = ConversationalAgent()

def interact_with_user():
    print("You can start asking questions. Type 'exit' to end the session.")
    while True:
        user_query = input("You: ")
        if user_query.lower() == 'exit':
            break
        response = agent.generate_response(user_query)
        print(f"Agent: {response}")

if __name__ == "__main__":
    interact_with_user()
