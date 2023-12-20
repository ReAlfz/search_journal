import streamlit as st
import google.generativeai as ai
import PyPDF2, os, sys


def extract_abstract(pdf, language):
    abstract = ''

    with open(pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()

            if language == 'Indonesian':
                if 'abstrak' in text.lower():
                    abstract = text[text.lower().index('abstrak')]
                    break
            else:
                if 'Abstract' in text.lower():
                    abstract = text[text.lower().index('abstract')]
                    break

    return abstract


def save_uploaded_file(uploaded_file, folder="."):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return filepath


if __name__ == '__main__':
    ai.configure(api_key='AIzaSyDjgqOud4IEbcMEBSFNBDg6dZTKzO0GiMs')
    defaults = {
        'model': 'models/text-bison-001',
        'temperature': 0.25,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
    }

    st.title('Summary Journal')
    final_response = None

    # Creating a side panel for inputs
    with st.sidebar:
        st.write("## Code Generator Settings")
        programming_language = st.selectbox("Choose the language:", ["Indonesian", "English"])
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if uploaded_file is not None:
            st.success(f"You selected: {uploaded_file.name}")
            file_path = save_uploaded_file(uploaded_file, folder="uploads")
            st.info(f"File saved to: {file_path}")
        else:
            text = st.text_input("Summary text")

        if st.button('Generate'):
            # if text == '':
            #     text = extract_abstract(file_path, programming_language)

            if programming_language == 'Indonesian':
                formatted_prompt = f"Tulis rangkuman text ini: {text}"
            else:
                formatted_prompt = f"Write Summary this text: {text}"

            response = ai.generate_text(
                **defaults,
                prompt=formatted_prompt
            )
            final_response = response

    if final_response != None:
        st.write(final_response.result)