# -*- coding: utf-8 -*-
"""prepare_data.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jHSDskOgxQvvGkHu3jbAZrOk-PEjp-GC
"""

pip install sentence-transformers

pip install faiss-cpu

import os
import json
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss

# Load lecture notes
lecture_notes = """
Your lecture notes text here...
"""

# Split lecture notes into segments
segments = lecture_notes.split('\n\n')

# Load pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for each segment
embeddings = model.encode(segments, convert_to_tensor=True)

# Save segments and embeddings
os.makedirs('data', exist_ok=True)
with open('data/segments.json', 'w') as f:
    json.dump(segments, f)

torch.save(embeddings, 'data/embeddings.pt')

# Example LLM architectures table
data = {
    "Model": ["GPT-3", "BERT", "T5"],
    "Paper": ["Language Models are Few-Shot Learners", "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"],
    "Year": [2020, 2019, 2020]
}

# Convert table to DataFrame
df = pd.DataFrame(data)

# Save table to JSON
df.to_json('data/llm_architectures.json', orient='records')

# Create FAISS index
embeddings_np = embeddings.numpy()
index = faiss.IndexFlatL2(embeddings_np.shape[1])
index.add(embeddings_np)

# Save FAISS index
faiss.write_index(index, 'data/faiss_index.index')