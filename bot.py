import streamlit as st
import google.generativeai as genai
import google.api_core.exceptions

def generate_response(prompt, api_key):
    """Generates a response from the Gemini API."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-2.0')
    try:
        response = model.generate_content(prompt)
        return response.text
    except google.api_core.exceptions.NotFound as e:
        return f"Error: API resource not found. Please check your API key and project settings. {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    st.title("Career Chatbot")

    api_key = "AIzaSyDE8ewEM5liBYkooT5kKmIis2ZwQ4pHMOU"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to ask?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if api_key:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response = generate_response(prompt, api_key)

                #Stream the response.
                for chunk in str(assistant_response).split(): #Added str() to handle possible error messages.
                    full_response += chunk + " "
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.warning("Please enter your API Key to get a response.")

if __name__ == "__main__":
    main()
