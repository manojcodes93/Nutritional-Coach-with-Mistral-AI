import os
import pandas as pd
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from mistralai import Mistral

# Load environment variables from .env file
load_dotenv()

# Mistral API key from env variable
api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("Please set your MISTRAL_API_KEY in the .env file")

# Initialize Mistral client with new API
client = Mistral(api_key=api_key)

embedding_path = "embeddings/store"

# Use explicit model_name to avoid deprecation warnings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

if not os.path.exists(embedding_path):
    # Build FAISS DB from CSV data if missing
    df = pd.read_csv("data/nutrition.csv")
    foods = list(df['food'])
    db = FAISS.from_texts(foods, embeddings)
    db.save_local(embedding_path)
else:
    # Load FAISS index with explicit deserialization permission
    db = FAISS.load_local(
        embedding_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

# Example function to query vector DB and get Mistral response
def ask_nutrition_coach(question: str):
    # Retrieve relevant docs from vector DB
    docs = db.similarity_search(question, k=5)

    # Combine retrieved docs as context
    context = "\n".join([doc.page_content for doc in docs])

    # Build chat messages with context + user question
    messages = [
        {"role": "system", "content": "You are a helpful nutritional coach."},
        {"role": "system", "content": f"Context: {context}"},
        {"role": "user", "content": question}
    ]

    # Call Mistral chat completion
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=messages
    )

    return response.choices[0].message.content