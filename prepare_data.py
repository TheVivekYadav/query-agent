# -*- coding: utf-8 -*-
"""prepare_data.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jHSDskOgxQvvGkHu3jbAZrOk-PEjp-GC
"""
import requests
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
import json
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss

# Load lecture notes
lecture_notes = """
What are Large Language Models(LLMs)?
A large language model is a type of artificial intelligence algorithm that applies neural network techniques with lots of parameters to process and understand human languages or text using self-supervised learning techniques. Tasks like text generation, machine translation, summary writing, image generation from texts, machine coding, chat-bots, or Conversational AI are applications of the Large Languag.e Model. Examples of such LLM models are Chat GPT by open AI, BERT (Bidirectional Encoder Representations from Transformers) by Google, etc.

There are many techniques that were tried to perform natural language-related tasks but the LLM is purely based on the deep learning methodologies. LLM (Large language model) models are highly efficient in capturing the complex entity relationships in the text at hand and can generate the text using the semantic and syntactic of that particular language in which we wish to do so.
How do Large Language Models work?
Large Language Models (LLMs) operate on the principles of deep learning, leveraging neural network architectures to process and understand human languages.

These models, are trained on vast datasets using self-supervised learning techniques. The core of their functionality lies in the intricate patterns and relationships they learn from diverse language data during training. LLMs consist of multiple layers, including feedforward layers, embedding layers, and attention layers. They employ attention mechanisms, like self-attention, to weigh the importance of different tokens in a sequence, allowing the model to capture dependencies and relationships.
LLM Models
If we talk about the size of the advancements in the GPT (Generative Pre-trained Transformer) model only then:

GPT-1 which was released in 2018 contains 117 million parameters having 985 million words.
GPT-2 which was released in 2019 contains 1.5 billion parameters.
GPT-3 which was released in 2020 contains 175 billion parameters. Chat GPT is also based on this model as well.
GPT-4 model is expected to be released in the year 2023 and it is likely to contain trillions of parameters.
Architecture of LLM
A Large Language Model’s (LLM) architecture is determined by a number of factors, like the objective of the specific model design, the available computational resources, and the kind of language processing tasks that are to be carried out by the LLM. The general architecture of LLM consists of many layers such as the feed forward layers, embedding layers, attention layers. A text which is embedded inside is collaborated together to generate predictions.

Important components to influence Large Language Model architecture  – 
Model Size and Parameter Count
input representations
Self-Attention Mechanisms
Training Objectives
Computational Efficiency
Decoding and Output Generation
Input Embeddings: The input text is tokenized into smaller units, such as words or sub-words, and each token is embedded into a continuous vector representation. This embedding step captures the semantic and syntactic information of the input.
Positional Encoding: Positional encoding is added to the input embeddings to provide information about the positions of the tokens because transformers do not naturally encode the order of the tokens. This enables the model to process the tokens while taking their sequential order into account.
Encoder: Based on a neural network technique, the encoder analyses the input text and creates a number of hidden states that protect the context and meaning of text data. Multiple encoder layers make up the core of the transformer architecture. Self-attention mechanism and feed-forward neural network are the two fundamental sub-components of each encoder layer.
Self-Attention Mechanism: Self-attention enables the model to weigh the importance of different tokens in the input sequence by computing attention scores. It allows the model to consider the dependencies and relationships between different tokens in a context-aware manner.
Feed-Forward Neural Network: After the self-attention step, a feed-forward neural network is applied to each token independently. This network includes fully connected layers with non-linear activation functions, allowing the model to capture complex interactions between tokens.
Decoder Layers: In some transformer-based models, a decoder component is included in addition to the encoder. The decoder layers enable autoregressive generation, where the model can generate sequential outputs by attending to the previously generated tokens.
Multi-Head Attention: Transformers often employ multi-head attention, where self-attention is performed simultaneously with different learned attention weights. This allows the model to capture different types of relationships and attend to various parts of the input sequence simultaneously.
Layer Normalization: Layer normalization is applied after each sub-component or layer in the transformer architecture. It helps stabilize the learning process and improves the model’s ability to generalize across different inputs.
Output Layers: The output layers of the transformer model can vary depending on the specific task. For example, in language modeling, a linear projection followed by SoftMax activation is commonly used to generate the probability distribution over the next token.
It’s important to keep in mind that the actual architecture of transformer-based models can change and be enhanced based on particular research and model creations. To fulfill different tasks and objectives, several models like GPT, BERT, and T5 may integrate more components or modifications.

Large Language Models Examples
Now let’s look at some of the famous LLMs which has been developed and are up for inference.

GPT – 3: The full form for GPT is a Generative pre-trained Transformer and this is the third version of such a model hence it is numbered as 3. This is developed by Open AI and you must have heard about Chat GPT which is launched by Open AI and is nothing but the GPT-3 model.
BERT – The full form for this is Bidirectional Encoder Representations from Transformers. This large language model has been developed by Google and is generally used for a variety of tasks related to natural language. Also, it can be used to generate embeddings for a particular text may be to train some other model.
RoBERTa – The full form for this is the Robustly Optimized BERT Pretraining Approach. In the series of attempts to improve the performance of the transformer architecture, RoBERTa is an enhanced version of the BERT model which is developed by Facebook AI Research.
BLOOM – It is the first multilingual LLM generated by the association of the different organizations and researchers who combined their expertise to develop this model which is similar to the GPT-3 architecture.
To explore further these models you can click on the particular model to get to know how you can use them by using the open source platforms like Hugging Face of Open AI. These articles cover the implementation part for each of these models in Python.
Large Language Models Use Cases
The main reason behind such a craze about the LLMs is their efficiency in the variety of tasks they can accomplish. From the above introductions and technical information about the LLMs you must have understood that the Chat GPT is also an LLM so, let’s use it to describe the use cases of Large Language Models.

Code Generation – One of the craziest use cases of this service is that it can generate quite an accurate code for a specific task that is described by the user to the model.
Debugging and Documentation of Code – If you are struggling with some piece of code regarding how to debug it then ChatGPT is your savior because it can tell you the line of code which are creating issues along with the remedy to correct the same. Also now you don’t have to spend hours writing the documentation of your project you can ask ChatGPT to do this for you.
Question Answering – As you must have seen that when AI-powered personal assistants were released people used to ask crazy questions to them well you can do that here as well along with the genuine questions.
Language Transfer – It can convert a piece of text from one language to another as it supports more than 50 native languages. It can also help you correct the grammatical mistakes in your content.
Use cases of LLM are not limited to the above-mentioned one has to be just creative enough to write better prompts and you can make these models do a variety of tasks as they are trained to perform tasks on one-shot learning and zero-shot learning methodologies as well. Due to this only Prompt Engineering is a totally new and hot topic in academics for people who are looking forward to using ChatGPT-type models extensively.

Large Language Models Applications
LLMs, such as GPT-3, have a wide range of applications across various domains. Few of them are:

Natural Language Understanding (NLU)

Large language models power advanced chatbots capable of engaging in natural conversations.
They can be used to create intelligent virtual assistants for tasks like scheduling, reminders, and information retrieval.
Content Generation

Creating human-like text for various purposes, including content creation, creative writing, and storytelling.
Writing code snippets based on natural language descriptions or commands.
Language Translation

Large language models can aid in translating text between different languages with improved accuracy and fluency.

Text Summarization

Generating concise summaries of longer texts or articles.

Sentiment Analysis

Analyzing and understanding sentiments expressed in social media posts, reviews, and comments.

Difference Between NLP and LLM 
NLP is Natural Language Processing, a field of artificial intelligence (AI). It consists of the development of the algorithms. NLP is a broader field than LLM, which consists of algorithms and techniques. NLP rules two approaches i.e. Machine learning and the analyze language data. Applications of NLP are-

Automotive routine task
Improve search 
Search engine optimization
Analyzing and organizing large documents
Social Media Analytics.
while on the other hand, LLM is a Large Language Model, and is more specific to human- like text, providing content generation, and personalized recommendations. 

What are the Advantages of Large Language Models?
Large Language Models (LLMs) come with several advantages that contribute to their widespread adoption and success in various applications:

LLMs can perform zero-shot learning, meaning they can generalize to tasks for which they were not explicitly trained. This capability allows for adaptability to new applications and scenarios without additional training.
LLMs efficiently handle vast amounts of data, making them suitable for tasks that require a deep understanding of extensive text corpora, such as language translation and document summarization.
LLMs can be fine-tuned on specific datasets or domains, allowing for continuous learning and adaptation to specific use cases or industries.
LLMs enable the automation of various language-related tasks, from code generation to content creation, freeing up human resources for more strategic and complex aspects of a project.
Challenges in Training of Large Language Models
There has been no doubt in the abilities of the LLMs in the future and this technology is part of most of the AI-powered applications which will be used by multiple users on a daily basis. But there are some drawbacks as well of LLMs.

For the successful training of a large language model, millions of dollars are required to set up that big computing power that can train the model utilizing parallel performance.
It requires months of training and then humans in the loop for the fine-tuning of models to achieve better performance.
Requiring a large amount of text corpus getting can be a challenging task because ChatGPT only is being accused of being trained on the data which has been scraped illegally and building an application for commercial purposes.
In the era of global warming and climate change, we cannot forget the carbon footprint of an LLM it is said that training a single AI model from scratch have carbon footprints equal to the carbon footprint of five cars in their whole lifetime which is a really serious concern.
Conclusion
Due to the challenges faced in training LLM transfer learning is promoted heavily to get rid of all of the challenges discussed above. LLM has the capability to bring revolution in the AI-powered application but the advancements in this field seem a bit difficult because just increasing the size of the model may increase its performance but after a particular time a saturation in the performance will come and the challenges to handle these models will be bigger than the performance boost achieved by further increasing the size of the models.

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
data = []
urls = [
    'https://raw.githubusercontent.com/vishalmaurya850/query-agent/master/phi-2.json',
    'https://raw.githubusercontent.com/vishalmaurya850/query-agent/master/google-gemma-2b.json',
    'https://raw.githubusercontent.com/vishalmaurya850/query-agent/master/deepseek-coder-6.7b-instruct.json',
    'https://raw.githubusercontent.com/vishalmaurya850/query-agent/master/OpenHermes-2.5-Mistral-7B.json',
    'https://raw.githubusercontent.com/vishalmaurya850/query-agent/master/Mistral-7B-Instruct-v0.2.json',
    'https://raw.githubusercontent.com/vishalmaurya850/query-agent/master/Mistral-7B-Instruct-v0.1.json',
    'https://raw.githubusercontent.com/vishalmaurya850/query-agent/master/Llama-3-8B-Instruct.json',
    'https://raw.githubusercontent.com/vishalmaurya850/query-agent/master/Hermes-2-Pro-Mistral-7B.json',
    'https://raw.githubusercontent.com/vishalmaurya850/query-agent/master/CodeLlama-7B-Instruct.json'
]
for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        data.append(json.loads(response.text))

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
