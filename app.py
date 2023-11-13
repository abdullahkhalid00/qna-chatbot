import streamlit as st

from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain


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
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store

def get_conversation_chain(vector_store):
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_user_input(user_question):
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            with st.chat_message(name="user", avatar="👦"):
                st.write(message.content)
        else:
            with st.chat_message(name="assistant", avatar="🤖"):
                st.write(message.content)


def main():
    load_dotenv()

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.set_page_config(
        page_title="Google Meet AI Assistant",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.header(body="Google Meet AI Assistant 🤖")

    user_question = st.chat_input(placeholder="Ask a question about your meeting transcript(s).")
    if user_question:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your transcript(s)")
        pdf_docs = st.file_uploader("Upload your transcript PDFs here and click 'Process'", accept_multiple_files=True)

        if pdf_docs:
            if st.button("Process"):
                with st.spinner("Processing"):

                    # get pdf text
                    raw_text = get_pdf_text(pdf_docs)

                    # get text chunks
                    text_chunks = get_text_chunks(raw_text)
                    
                    # get vector store using embeddings
                    vector_store = get_vector_store(text_chunks)

                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(vector_store)


if __name__ == "__main__":
    main()