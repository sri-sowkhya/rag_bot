import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import google.generativeai as genai

# Streamlit Secrets (Recommended)
genai.configure(api_key=st.secrets["AIzaSyDE8ewEM5liBYkooT5kKmIis2ZwQ4pHMOU"])


st.title("CSV RAG System")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    column_names = df.columns.tolist()
    text_column = st.selectbox("Select the text column:", column_names)

    if text_column:
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

        query = st.text_input("Enter your query:")

        if query:
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

            retrieved_chunks, retrieved_data = retrieve(query)
            context = "\n".join(retrieved_chunks)
            response = generate(query, context)

            st.write("Retrieved Context:")
            st.write(context)
            st.write("LLM Response:")
            st.write(response)
            st.write("Retrieved Data:")
            st.dataframe(retrieved_data)
