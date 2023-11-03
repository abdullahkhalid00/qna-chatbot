import streamlit as st

from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon="books")

    st.header("Chat with multiple PDFs :books:")
    st.text_input("Ask a question about your document(s).")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click 'Process'", accept_multiple_files=True)
        
        if st.button("Process"):
            with st.spinner("Processing"):

                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get text chunks
                text_chunks = get_text_chunks(raw_text)
                
                # get vector store using embeddings
                vector_store = get_vector_store(text_chunks)


if __name__ == "__main__":
    main()