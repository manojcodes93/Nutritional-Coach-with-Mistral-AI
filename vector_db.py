import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

df = pd.read_csv("C:\\Users\\manoj\\nutrition_coach\\data\\nutrition.csv")

foods = list(df['food'])

embeddings = HuggingFaceEmbeddings()

db = FAISS.from_texts(foods, embeddings)
db.save_local("embeddings/store")
print("Vector DB created successful")