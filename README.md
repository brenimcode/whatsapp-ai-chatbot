# Conversational AI Agent for WhatsApp Barber Shops

This conversational agent leverages **Artificial Intelligence (AI)**, **RAG (Retrieval-Augmented Generation)**, and **Prompt Engineering** to revolutionize customer service for barber shops. It operates **24/7 autonomously**, ensuring **fast, natural, and personalized responses** to WhatsApp users.

## Technologies Used

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-%23000000.svg?style=for-the-badge&logo=LangChain&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white&style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF0000?style=for-the-badge&logo=chroma&logoColor=FFFFFF)
![Groq](https://img.shields.io/badge/Groq-FF6347?logo=groq&logoColor=white&style=for-the-badge)
![DeepSeek](https://img.shields.io/badge/DeepSeek-4b6bfc?style=for-the-badge&logoColor=FFFFFF)

## System Overview

![Diagram](https://github.com/user-attachments/assets/010a0461-7b5c-4239-a492-9037ea33e792)

This system employs **RAG (Retrieval-Augmented Generation)** to generate responses from various document formats (PDF, images, text, etc.), utilizing a **vector database** to fetch relevant information dynamically. This ensures responses that are more **coherent, concise, and less prone to hallucinations**—a common issue in LLMs.

For efficient data storage, I use **ChromaDB**, a vector database that stores high-dimensional embeddings and efficiently handles retrieval and deletion operations.

Embeddings are generated using **HuggingFace Embeddings**, an open-source, high-performance solution.

To maintain conversational context, the agent stores the last five WhatsApp messages, preserving a history that allows for **more accurate and context-aware responses**.

The LLM receives input structured as follows:
- **User Message (WhatsApp input)**
- **Relevant Documents (retrieved from the vector database)**
- **Optimized Prompt (Few-Shot Prompting with instructions, persona, and context)**

Incoming WhatsApp messages are processed through **WAHA API**, which acts as a middleware between the user and the LLM.

A **FastAPI**-based API exposes a `/webhook` route, which is consumed by the WAHA API. When a message arrives, it is sent to the webhook, processed by the LLM, and a response is generated.

## Requirements

Ensure you have the following installed on your system:

- Python (recommended version: 3.10 or higher)
- Docker & Docker Compose
- Other dependencies listed in `requirements.txt`

## Installing Dependencies

With the virtual environment activated, install project dependencies using:

```bash
pip install -r requirements.txt
```

## Running the Project

Once dependencies are installed, start the services using Docker Compose:

```bash
docker-compose up --build
```
