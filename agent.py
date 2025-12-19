import os
from mistralai import Mistral
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from tools import calculate_bmr, calculate_macros

load_dotenv()

# Mistral client setup
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def ask_mistral(prompt):
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Load vector DB for nutrition search
embeddings = HuggingFaceEmbeddings()
db = FAISS.load_local(
    "embeddings/store",
    embeddings,
    allow_dangerous_deserialization=True  # <-- This flag is required
)

def search_food(query):
    results = db.similarity_search(query)
    return results

# Main agent logic
def nutritional_agent(user_query):
    if "bmr" in user_query.lower():
        return "Please provide weight, height, age, gender."
    elif "food" in user_query.lower():
        foods = search_food(user_query)
        return str(foods)
    else:
        return ask_mistral(user_query)
