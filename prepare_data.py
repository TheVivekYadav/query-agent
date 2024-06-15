# -*- coding: utf-8 -*-
"""prepare_data.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jHSDskOgxQvvGkHu3jbAZrOk-PEjp-GC
"""
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
data ={ 
    {
    "_descriptorVersion": "0.0.1",  
    "datePublished": "2024-02-21T16:54:57.000Z",
    "name": "Google's Gemma 2B Instruct",
    "description": "Gemma is a family of lightweight LLMs built from the same research and technology Google used to create the Gemini models. Gemma models are available in two sizes, 2 billion and 7 billion parameters. These models are trained on up to 6T tokens of primarily English web documents, mathematics, and code, using a transformer architecture with enhancements like Multi-Query Attention, RoPE Embeddings, GeGLU Activations, and advanced normalization techniques.",
    "author": {
      "name": "Google DeepMind",
      "url": "https://deepmind.google",
      "blurb": "We’re a team of scientists, engineers, ethicists and more, working to build the next generation of AI systems safely and responsibly."
    },
    "numParameters": "2B",
    "resources": {
      "canonicalUrl": "https://huggingface.co/google/gemma-2b-it",
      "paperUrl": "https://blog.google/technology/developers/gemma-open-models/",
      "downloadUrl": "https://huggingface.co/lmstudio-ai/gemma-2b-it-GGUF"
    },
    "trainedFor": "chat",
    "arch": "gemma",
    "files": {
      "highlighted": {
        "economical": {
          "name": "gemma-2b-it-q8_0.gguf"
        }
      },
      "all": [
        {
          "name": "gemma-2b-it-q8_0.gguf",
          "url": "https://huggingface.co/lmstudio-ai/gemma-2b-it-GGUF/resolve/main/gemma-2b-it-q8_0.gguf",
          "sizeBytes": 2669351840,
          "quantization": "Q8_0",
          "format": "gguf",
          "sha256checksum": "ec68b50d23469882716782da8b680402246356c3f984e9a3b9bcc5bc15273140",
          "publisher": {
            "name": "LM Studio",
            "socialUrl": "https://twitter.com/LMStudioAI"
          },
          "respository": "lmstudio-ai/gemma-2b-it-GGUF",
          "repositoryUrl": "https://huggingface.co/lmstudio-ai/gemma-2b-it-GGUF"
        }
      ]
    }
  },
    {
  "_descriptorVersion": "0.0.1",  
  "datePublished": "2024-03-19T11:04:50.000Z",
  "name": "Starling LM 7B Beta",
  "description": "Starling-LM-7B-beta is a language model fine-tuned through Reinforcement Learning with Human Feedback (RLHF) and AI Feedback (RLAIF), developed by Banghua Zhu, Evan Frick, Tianhao Wu, Hanlin Zhu, Karthik Ganesan, Wei-Lin Chiang, Jian Zhang, and Jiantao Jiao. It is available under an Apache-2.0 license, provided it's not used in competition against OpenAI. Originating from Openchat-3.5-0106, which is based on Mistral-7B-v0.1, Starling-LM-7B-beta employs a new reward model, Nexusflow/Starling-RM-34B, and a policy optimization method, Fine-Tuning Language Models from Human Preferences (PPO). Utilizing the berkeley-nest/Nectar ranking dataset, the enhanced Starling-RM-34B reward model, and a novel reward training and policy tuning pipeline, Starling-LM-7B-beta achieves a score of 8.12 in MT Bench, with GPT-4 serving as the evaluator.",
  "author": {
    "name": "Nexusflow",
    "url": "https://nexusflow.ai/",
    "blurb": "Democratize GenAI Agents for Enterprise Workflows."
  },
  "numParameters": "7B",
  "resources": {
    "canonicalUrl": "https://huggingface.co/Nexusflow/Starling-LM-7B-beta",
    "downloadUrl": "https://huggingface.co/bartowski/Starling-LM-7B-beta-GGUF",
    "paperUrl": "https://starling.cs.berkeley.edu/"
  },
  "trainedFor": "instruct",
  "arch": "mistral",
  "files": {
    "highlighted": {
      "economical": {
        "name": "Starling-LM-7B-beta-IQ4_XS.gguf"
      }
    },
    "all": [
      {
        "name": "Starling-LM-7B-beta-IQ4_XS.gguf",
        "url": "https://huggingface.co/bartowski/Starling-LM-7B-beta-GGUF/resolve/main/Starling-LM-7B-beta-IQ4_XS.gguf",
        "sizeBytes": 3944399776,
        "quantization": "IQ4_XS",
        "format": "gguf",
        "sha256checksum": "8320f28768b95e42240c079a265550cb52975002a3cc48616d1eac1b25ecb666",
        "publisher": {
          "name": "Bartowski",
          "socialUrl": "https://huggingface.co/bartowski"
        },
        "respository": "bartowski/Starling-LM-7B-beta-GGUF",
        "repositoryUrl": "https://huggingface.co/bartowski/Starling-LM-7B-beta-GGUF"
      }
    ]
  }
},
    {
  "_descriptorVersion": "0.0.1",  
  "datePublished": "2024-03-19T11:04:50.000Z",
  "name": "Starling LM 7B Beta",
  "description": "Starling-LM-7B-beta is a language model fine-tuned through Reinforcement Learning with Human Feedback (RLHF) and AI Feedback (RLAIF), developed by Banghua Zhu, Evan Frick, Tianhao Wu, Hanlin Zhu, Karthik Ganesan, Wei-Lin Chiang, Jian Zhang, and Jiantao Jiao. It is available under an Apache-2.0 license, provided it's not used in competition against OpenAI. Originating from Openchat-3.5-0106, which is based on Mistral-7B-v0.1, Starling-LM-7B-beta employs a new reward model, Nexusflow/Starling-RM-34B, and a policy optimization method, Fine-Tuning Language Models from Human Preferences (PPO). Utilizing the berkeley-nest/Nectar ranking dataset, the enhanced Starling-RM-34B reward model, and a novel reward training and policy tuning pipeline, Starling-LM-7B-beta achieves a score of 8.12 in MT Bench, with GPT-4 serving as the evaluator.",
  "author": {
    "name": "Nexusflow",
    "url": "https://nexusflow.ai/",
    "blurb": "Democratize GenAI Agents for Enterprise Workflows."
  },
  "numParameters": "7B",
  "resources": {
    "canonicalUrl": "https://huggingface.co/Nexusflow/Starling-LM-7B-beta",
    "downloadUrl": "https://huggingface.co/bartowski/Starling-LM-7B-beta-GGUF",
    "paperUrl": "https://starling.cs.berkeley.edu/"
  },
  "trainedFor": "instruct",
  "arch": "mistral",
  "files": {
    "highlighted": {
      "economical": {
        "name": "Starling-LM-7B-beta-IQ4_XS.gguf"
      }
    },
    "all": [
      {
        "name": "Starling-LM-7B-beta-IQ4_XS.gguf",
        "url": "https://huggingface.co/bartowski/Starling-LM-7B-beta-GGUF/resolve/main/Starling-LM-7B-beta-IQ4_XS.gguf",
        "sizeBytes": 3944399776,
        "quantization": "IQ4_XS",
        "format": "gguf",
        "sha256checksum": "8320f28768b95e42240c079a265550cb52975002a3cc48616d1eac1b25ecb666",
        "publisher": {
          "name": "Bartowski",
          "socialUrl": "https://huggingface.co/bartowski"
        },
        "respository": "bartowski/Starling-LM-7B-beta-GGUF",
        "repositoryUrl": "https://huggingface.co/bartowski/Starling-LM-7B-beta-GGUF"
      }
    ]
  }
},
    {
  "_descriptorVersion": "0.0.1",  
  "datePublished": "2023-10-29T21:27:30",
  "name": "OpenHermes 2.5 Mistral 7B",
  "description": "OpenHermes 2.5 Mistral 7B is an advanced iteration of the OpenHermes 2 language model, enhanced by training on a significant proportion of code datasets. This additional training improved performance across several benchmarks, notably TruthfulQA, AGIEval, and the GPT4All suite, while slightly decreasing the BigBench score. Notably, the model's ability to handle code-related tasks, measured by the humaneval score, increased from 43% to 50.7%. The training data consisted of one million entries, primarily sourced from GPT-4 outputs and other high-quality open datasets. This data was rigorously filtered and standardized to the ShareGPT format and subsequently processed using ChatML by the axolotl tool.",
  "author": {
    "name": "Teknium",
    "url": "https://twitter.com/Teknium1",
    "blurb": "Creator of numerous chart topping fine-tunes and a Co-founder of NousResearch"
  },
  "numParameters": "7B",
  "resources": {
    "canonicalUrl": "https://huggingface.co/teknium/OpenHermes-2.5-Mistral-7B",
    "downloadUrl": "https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF"
  },
  "trainedFor": "chat",
  "arch": "mistral",
  "files": {
    "highlighted": {
      "economical": {
        "name": "openhermes-2.5-mistral-7b.Q4_K_S.gguf"
      },
      "most_capable": {
        "name": "openhermes-2.5-mistral-7b.Q6_K.gguf"
      }
    },
    "all": [
      {
        "name": "openhermes-2.5-mistral-7b.Q4_K_S.gguf",
        "url": "https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF/resolve/main/openhermes-2.5-mistral-7b.Q4_K_S.gguf",
        "sizeBytes": 4140385024,
        "quantization": "Q4_K_S",
        "format": "gguf",
        "sha256checksum": "5ae9c3c11ce520a2360dcfca1f4e38392dc0b7a49413ce6695857a5148a71d35",
        "publisher": {
          "name": "TheBloke",
          "socialUrl": "https://twitter.com/TheBlokeAI"
        },
        "respository": "TheBloke/OpenHermes-2.5-Mistral-7B-GGUF",
        "repositoryUrl": "https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF"
      },
      {
        "name": "openhermes-2.5-mistral-7b.Q6_K.gguf",
        "url": "https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF/resolve/main/openhermes-2.5-mistral-7b.Q6_K.gguf",
        "sizeBytes": 5942078272,
        "quantization": "Q6_K",
        "format": "gguf",
        "sha256checksum": "cd4caa42229e973636e9d4c8db50a89593353c521e0342ca615756ded2b977a2",
        "publisher": {
          "name": "TheBloke",
          "socialUrl": "https://twitter.com/TheBlokeAI"
        },
        "respository": "TheBloke/OpenHermes-2.5-Mistral-7B-GGUF",
        "repositoryUrl": "https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF"
      }
    ]
  }
},
    {
    "_descriptorVersion": "0.0.1",  
    "datePublished": "2023-12-11T06:26:58",
    "name": "NexusRaven-V2-13B",
    "description": "NexusRaven-V2 accepts a list of python functions. These python functions can do anything (e.g. sending GET/POST requests to external APIs). The two requirements include the python function signature and the appropriate docstring to generate the function call. *** Follow NexusRaven's prompting guide found on the model's Hugging Face page. ***",
    "author": {
      "name": "Nexusflow",
      "url": "https://nexusflow.ai",
      "blurb": "Nexusflow is democratizing Cyber Intelligence with Generative AI, fully on top of open-source large language models (LLMs)"
    },
    "numParameters": "13B",
    "resources": {
      "canonicalUrl": "https://huggingface.co/Nexusflow/NexusRaven-V2-13B",
      "downloadUrl": "https://huggingface.co/TheBloke/NexusRaven-V2-13B-GGUF"
    },
    "trainedFor": "other",
    "arch": "llama",
    "files": {
      "highlighted": {
        "economical": {
          "name": "nexusraven-v2-13b.Q4_K_S.gguf"
        },
        "most_capable": {
          "name": "nexusraven-v2-13b.Q6_K.gguf"
        }
      },
      "all": [
        {
          "name": "nexusraven-v2-13b.Q4_K_S.gguf",
          "url": "https://huggingface.co/TheBloke/NexusRaven-V2-13B-GGUF/resolve/main/nexusraven-v2-13b.Q4_K_S.gguf",
          "sizeBytes": 7414501952,
          "quantization": "Q4_K_S",
          "format": "gguf",
          "sha256checksum": "bc2e1ce9fa064e675690d4c6f2c441d922f24241764241aa013d0ca8a87ecbfe",
          "publisher": {
            "name": "TheBloke",
            "socialUrl": "https://twitter.com/TheBlokeAI"
          },
          "respository": "TheBloke/NexusRaven-V2-13B-GGUF",
          "repositoryUrl": "https://huggingface.co/TheBloke/NexusRaven-V2-13B-GGUF"
        },
        {
          "name": "nexusraven-v2-13b.Q6_K.gguf",
          "url": "https://huggingface.co/TheBloke/NexusRaven-V2-13B-GGUF/resolve/main/nexusraven-v2-13b.Q6_K.gguf",
          "sizeBytes": 10679342592,
          "quantization": "Q6_K",
          "format": "gguf",
          "sha256checksum": "556ae244f4c69c603b7cda762d003d09f68058c671f304c2e011214ce754acb4",
          "publisher": {
            "name": "TheBloke",
            "socialUrl": "https://twitter.com/TheBlokeAI"
          },
          "respository": "TheBloke/NexusRaven-V2-13B-GGUF",
          "repositoryUrl": "https://huggingface.co/TheBloke/NexusRaven-V2-13B-GGUF"
        }
      ]
    }
  },
    {
    "_descriptorVersion": "0.0.1",  
    "datePublished": "2023-12-12T10:12:59",
    "name": "Mistral 7B Instruct v0.2",
    "description": "The Mistral-7B-Instruct-v0.2 Large Language Model (LLM) is an improved instruct fine-tuned version of Mistral-7B-Instruct-v0.1. For full details of this model read MistralAI's blog post and paper.",
    "author": {
      "name": "Mistral AI",
      "url": "https://mistral.ai/",
      "blurb": "Mistral AI's mission is to spearhead the revolution of open models."
    },
    "numParameters": "7B",
    "resources": {
      "canonicalUrl": "https://mistral.ai/news/la-plateforme/",
      "paperUrl": "https://arxiv.org/abs/2310.06825",
      "downloadUrl": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
    },
    "trainedFor": "chat",
    "arch": "mistral",
    "files": {
      "highlighted": {
        "economical": {
          "name": "mistral-7b-instruct-v0.2.Q4_K_S.gguf"
        },
        "most_capable": {
          "name": "mistral-7b-instruct-v0.2.Q6_K.gguf"
        }
      },
      "all": [
        {
          "name": "mistral-7b-instruct-v0.2.Q4_K_S.gguf",
          "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_S.gguf",
          "sizeBytes": 4140374304,
          "quantization": "Q4_K_S",
          "format": "gguf",
          "sha256checksum": "1213e19b3e103932fdfdc82e3b6dee765f57ad5756e0f673e7d36514a5b60d0a",
          "publisher": {
            "name": "TheBloke",
            "socialUrl": "https://twitter.com/TheBlokeAI"
          },
          "respository": "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
          "repositoryUrl": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
        },
        {
          "name": "mistral-7b-instruct-v0.2.Q6_K.gguf",
          "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q6_K.gguf",
          "sizeBytes": 5942065440,
          "quantization": "Q6_K",
          "format": "gguf",
          "sha256checksum": "a4643671c92f47eb6027d0eff50b9875562e8e172128a4b10b2be250bb4264de",
          "publisher": {
            "name": "TheBloke",
            "socialUrl": "https://twitter.com/TheBlokeAI"
          },
          "respository": "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
          "repositoryUrl": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
        }
      ]
    }
  },
    {
  "_descriptorVersion": "0.0.1",  
  "datePublished": "2023-09-27T16:12:57",
  "name": "Mistral 7B Instruct v0.1",
  "description": "The Mistral-7B-Instruct-v0.1 is a Large Language Model (LLM) developed by Mistral AI. This LLM is an instruct fine-tuned version of a generative text model, leveraging a variety of publicly available conversation datasets. The model's architecture is based on a transformer model, featuring Grouped-Query Attention, Sliding-Window Attention, and a Byte-fallback BPE tokenizer. To utilize the instruction fine-tuning capabilities, prompts should be enclosed within [INST] and [/INST] tokens. The initial instruction should commence with a beginning-of-sentence id, whereas subsequent instructions should not. The generation process by the assistant will terminate with the end-of-sentence token id. For detailed information about this model, refer to the release blog posts by Mistral AI.",
  "author": {
    "name": "Mistral AI",
    "url": "https://mistral.ai/",
    "blurb": "Mistral AI's mission is to spearhead the revolution of open models."
  },
  "numParameters": "7B",
  "resources": {
    "canonicalUrl": "https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1",
    "paperUrl": "https://mistral.ai/news/announcing-mistral-7b/",
    "downloadUrl": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
  },
  "trainedFor": "chat",
  "arch": "mistral",
  "files": {
    "highlighted": {
      "economical": {
        "name": "mistral-7b-instruct-v0.1.Q4_K_S.gguf"
      },
      "most_capable": {
        "name": "mistral-7b-instruct-v0.1.Q6_K.gguf"
      }
    },
    "all": [
      {
        "name": "mistral-7b-instruct-v0.1.Q4_K_S.gguf",
        "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_S.gguf",
        "sizeBytes": 4140373664,
        "quantization": "Q4_K_S",
        "format": "gguf",
        "sha256checksum": "f1b7f1885029080be49aff49c83f87333449ef727089546e0d887e2f17f0d02e",
        "publisher": {
          "name": "TheBloke",
          "socialUrl": "https://twitter.com/TheBlokeAI"
        },
        "respository": "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        "repositoryUrl": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
      },
      {
        "name": "mistral-7b-instruct-v0.1.Q6_K.gguf",
        "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q6_K.gguf",
        "sizeBytes": 5942064800,
        "quantization": "Q6_K",
        "format": "gguf",
        "sha256checksum": "dfb053cb8d5f56abde8f56899ffe0d23e1285a423df0b65ea3f3adbb263b22c2",
        "publisher": {
          "name": "TheBloke",
          "socialUrl": "https://twitter.com/TheBlokeAI"
        },
        "respository": "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        "repositoryUrl": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
      }
    ]
  }
},
    {
  "_descriptorVersion": "0.0.1",  
  "datePublished": "2024-04-19T01:00:31.000Z",
  "name": "Llama 3 - 8B Instruct",
  "description": "MetaAI's latest Llama model is here. Llama 3 comes in two sizes: 8B and 70B. Llama 3 is pretrained on over 15T tokens that were all collected from publicly available sources. Meta's training dataset is seven times larger than that used for Llama 2, and it includes four times more code.",
  "author": {
    "name": "Meta AI",
    "url": "https://ai.meta.com",
    "blurb": "Pushing the boundaries of AI through research, infrastructure and product innovation."
  },
  "numParameters": "7B",
  "resources": {
    "canonicalUrl": "https://llama.meta.com/llama3/",
    "paperUrl": "https://ai.meta.com/blog/meta-llama-3/",
    "downloadUrl": "https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF"
  },
  "trainedFor": "chat",
  "arch": "llama",
  "files": {
    "highlighted": {
      "economical": {
        "name": "Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"
      }
    },
    "all": [
      {
        "name": "Meta-Llama-3-8B-Instruct-Q4_K_M.gguf",
        "url": "https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf",
        "sizeBytes": 4920733888,
        "quantization": "Q4_K_S",
        "format": "gguf",
        "sha256checksum": "ab9e4eec7e80892fd78f74d9a15d0299f1e22121cea44efd68a7a02a3fe9a1da",
        "publisher": {
          "name": "LM Studio Community",
          "socialUrl": "https://huggingface.co/lmstudio-community"
        },
        "respository": "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        "repositoryUrl": "https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF"
      }
    ]
  }
},
{ "_descriptorVersion": "0.0.1",  
  "datePublished": "2024-03-12T06:52:19.000Z",
  "name": "Hermes 2 Pro Mistral 7B",
  "description": "Hermes 2 Pro, an updated version of Nous Hermes 2, incorporates an enhanced and cleaned OpenHermes 2.5 Dataset alongside a new in-house developed dataset for Function Calling and JSON Mode. This version retains its robust performance in general tasks and conversations while showing notable improvements in Function Calling, JSON Structured Outputs, achieving a 90% score in function calling evaluation conducted with Fireworks.AI, and 84% in structured JSON Output evaluation. It introduces a special system prompt and a multi-turn function calling structure, incorporating a chatml role to streamline and simplify function calling.",
  "author": {
    "name": "NousResearch",
    "url": "https://twitter.com/NousResearch",
    "blurb": "We are dedicated to advancing the field of natural language processing, in collaboration with the open-source community, through bleeding-edge research and a commitment to symbiotic development."
  },
  "numParameters": "7B",
  "resources": {
    "canonicalUrl": "https://huggingface.co/NousResearch/Hermes-2-Pro-Mistral-7B",
    "downloadUrl": "https://huggingface.co/NousResearch/Hermes-2-Pro-Mistral-7B-GGUF"
  },
  "trainedFor": "chat",
  "arch": "mistral",
  "files": {
    "highlighted": {
      "economical": {
        "name": "Hermes-2-Pro-Mistral-7B.Q4_0.gguf"
      }
    },
    "all": [
      {
        "name": "Hermes-2-Pro-Mistral-7B.Q4_0.gguf",
        "url": "https://huggingface.co/NousResearch/Hermes-2-Pro-Mistral-7B-GGUF/resolve/main/Hermes-2-Pro-Mistral-7B.Q4_0.gguf",
        "sizeBytes": 4109098752,
        "quantization": "q4_0",
        "format": "gguf",
        "sha256checksum": "f446c3125026f7af6757dd097dda02280adc85e908c058bd6f1c41a118354745",
        "publisher": {
          "name": "NousResearch",
          "socialUrl": "https://twitter.com/NousResearch"
        },
        "respository": "NousResearch/Hermes-2-Pro-Mistral-7B-GGUF",
        "repositoryUrl": "https://huggingface.co/NousResearch/Hermes-2-Pro-Mistral-7B-GGUF"
      }
    ]
  }
},
   {
  "_descriptorVersion": "0.0.1",  
  "datePublished": "2023-08-24T21:39:59",
  "name": "CodeLlama 7B Instruct",
  "description": "MetaAI has released Code Llama, a comprehensive family of large language models for code. These models are based on Llama 2 and exhibit state-of-the-art performance among openly available models. They offer advanced infilling capabilities, can accommodate large input contexts, and have the ability to follow instructions for programming tasks without prior training. There are various versions available to cater to a wide array of applications: foundation models (Code Llama), Python-specific models (Code Llama - Python), and models for following instructions (Code Llama - Instruct). These versions come with 7B, 13B, and 34B parameters respectively. All models are trained on 16k token sequences and show improvements even on inputs with up to 100k tokens. The 7B and 13B models of Code Llama and Code Llama - Instruct have the ability to infill based on surrounding content. In terms of performance, Code Llama has set new standards among open models on several code benchmarks, achieving scores of up to 53% on HumanEval and 55% on MBPP. Notably, the Python version of Code Llama 7B surpasses the performance of Llama 2 70B on HumanEval and MBPP. All of MetaAI's models outperform every other publicly available model on MultiPL-E. Code Llama has been released under a permissive license that enables both research and commercial use.",
  "author": {
    "name": "Meta AI",
    "url": "https://ai.meta.com",
    "blurb": "Pushing the boundaries of AI through research, infrastructure and product innovation."
  },
  "numParameters": "7B",
  "resources": {
    "canonicalUrl": "https://ai.meta.com/blog/code-llama-large-language-model-coding/",
    "paperUrl": "https://ai.meta.com/research/publications/code-llama-open-foundation-models-for-code/",
    "downloadUrl": "https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF"
  },
  "trainedFor": "chat",
  "arch": "llama",
  "files": {
    "highlighted": {
      "economical": {
        "name": "codellama-7b-instruct.Q4_K_S.gguf"
      },
      "most_capable": {
        "name": "codellama-7b-instruct.Q6_K.gguf"
      }
    },
    "all": [
      {
        "name": "codellama-7b-instruct.Q4_K_S.gguf",
        "url": "https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q4_K_S.gguf",
        "sizeBytes": 3856831168,
        "quantization": "Q4_K_S",
        "format": "gguf",
        "sha256checksum": "2e44d2b7ae28bbe3a2ed698e259cbd3a6bf7fe8f9d351e14b2be17fb690d7f95",
        "publisher": {
          "name": "TheBloke",
          "socialUrl": "https://twitter.com/TheBlokeAI"
        },
        "respository": "TheBloke/CodeLlama-7B-Instruct-GGUF",
        "repositoryUrl": "https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF"
      },
      {
        "name": "codellama-7b-instruct.Q6_K.gguf",
        "url": "https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.Q6_K.gguf",
        "sizeBytes": 5529302208,
        "quantization": "Q6_K",
        "format": "gguf",
        "sha256checksum": "2f516cd9c16181832ffceaf94b13e8600d88c9bc8d7f75717d25d8c9cf9aa973",
        "publisher": {
          "name": "TheBloke",
          "socialUrl": "https://twitter.com/TheBlokeAI"
        },
        "respository": "TheBloke/CodeLlama-7B-Instruct-GGUF",
        "repositoryUrl": "https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF"
      }
    ]
  }
}
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
