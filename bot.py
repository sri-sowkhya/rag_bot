import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import google.generativeai as genai
import os

# Streamlit Secrets (Recommended)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

try:
    df = pd.read_csv("job_recommendation_dataset.csv")
    column_names = df.columns.tolist()
    text_column = st.selectbox("Select the text column:", column_names)

    chunks = []
    data_index = {}
    model = SentenceTransformer("all-mpnet-base-v2")

    for index, row in df.iterrows():
        text = row[text_column]
        sentences = text.split(". ")
        for sentence in sentences:
            chunks.append(sentence)
            data_index[len(chunks) - 1] = index

    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    def retrieve(query, k=3):
        query_embedding = model.encode([query])
        distances, indices = index.search(query_embedding, k)
        retrieved_chunks = [chunks[i] for i in indices[0]]
        retrieved_data = [df.iloc[data_index[i]] for i in indices[0]]
        return retrieved_chunks, retrieved_data

    def generate(query, context):
        prompt = f"Answer the question: {query}\nContext: {context}"
        model = genai.GenerativeModel('gemini-pro')
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating response: {e}"

    st.title("CSV RAG System")
    query = st.text_input("Enter your query:")

    if query:
        retrieved_chunks, retrieved_data = retrieve(query)
        context = "\n".join(retrieved_chunks)
        response = generate(query, context)
        st.write("Retrieved Context:")
        st.write(context)
        st.write("LLM Response:")
        st.write(response)

except FileNotFoundError:
    st.error("job_recommendation_dataset.csv not found. Make sure it's in the same directory as the script.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
