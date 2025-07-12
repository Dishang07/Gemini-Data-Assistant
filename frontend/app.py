import streamlit as st
import requests

st.title("DOCX + Dataset Query Assistant")

query = st.text_input("Ask a question about the dataset or doc...")

if st.button("Submit"):
    try:
        response = requests.post("http://localhost:8000/query", json={"query": query})
        response.raise_for_status()  # Raises error for 4xx/5xx responses
        st.json(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        st.text(response.text)  # show raw error text (useful for debugging)
    except ValueError as ve:
        st.error("Invalid JSON returned by API")
        st.text(response.text)
