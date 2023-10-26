title: Prototyping a PDF Chatbot from Scratch
slug: prototyping-a-pdf-chatbot-from-scratch
date: 2023-10-24
tags: python, machine learning, ai

As part of my work on [refstudio](https://github.com/refstudio/refstudio), I spent some time prototyping a chatbot that could answer questions about a corpus of PDFs. Tools like [LangChain](https://github.com/langchain-ai/langchain), [LlamaIndex](https://github.com/run-llama/llama_index), [Haystack](https://github.com/deepset-ai/haystack), and others all have built-in abstractions to simplify this task, but I find that building a simplified version from scratch helps me understand the underlying concepts better.

A basic version of the PDF Chatbot requires two phases with the following steps:

1. PDF Ingestion
    - Convert PDFs to text
    - Chunk the text into smaller pieces
    - Optional: Generate embeddings for the text chunks
    - Persist the text chunks (or embeddings) in some way so that we can query them later
2. Chatbot Interaction
    - Take a question from the user
    - Retrieve the most similar text chunks related to the question
        - If we did not create embeddings, we can use a ranking function like [BM25](https://en.wikipedia.org/wiki/Okapi_BM25) to find the most similar text chunks
        - If we did create embeddings, we can use a nearest neighbors algorithm to find the most similar text chunks
    - Include the most similar text chunks as "context" we provide to the LLM with our question (i.e. our prompt)
    - Return the LLM's response

While embeddings and a vector database are not strictly necessary for this task, I wanted to get a sense of the ergonomics in working with one, so I used this as an excuse to try out [LanceDB](https://github.com/lancedb/lancedb). LanceDB is an open-source, embedded vector database with the goal of simplifying retrieval, filtering, and management of embeddings. It's built on Apache Arrow, which I'm a big fan of. 

### Results

You can find the code for this prototype in [this github repo](https://github.com/gjreda/scratch-pdf-bot).

Here's a quick demo of the chatbot in action:

<iframe width="560" height="315" src="https://www.youtube.com/embed/r4LAQbu3sd0?si=DarJiS8PYFJrLpKK" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
