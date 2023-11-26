import os, csv, time, atexit
import streamlit as st

from dotenv import load_dotenv
from openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain


def process_audio_file(audio_file):
    file_path = os.path.join("./", "uploaded_audio.mp3")
    with open(file_path, 'wb') as result:
        result.write(audio_file.read())
    return file_path

def delete_temp_file(file_path):
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

def get_transcript(audio_file):
    client = OpenAI()
    with open(audio_file, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
        )
    return transcript.text

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
    start = time.time()
    response = st.session_state.conversation({"question": user_question})
    end = time.time()
    
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            with st.chat_message(name="user", avatar="👦"):
                st.write(message.content)
        else:
            with st.chat_message(name="assistant", avatar="🤖"):
                st.write(message.content)

    get_responses(message.content, end-start)  

def get_responses(response, duration, model='gpt-4'):
    fpath = './data/responses.csv'
    cols = ['response', 'duration', 'model']

    if not os.path.exists(fpath):
        with open(fpath, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=cols)
            writer.writeheader()

    with open(fpath, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=cols)
        writer.writerow({"response": response, "duration": duration, "model": model})


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
    st.header(body="Virtual Meeting AI Assistant 🤖")

    user_question = st.chat_input(placeholder="Ask a question about your meeting(s).")
    if user_question:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your meeting(s)")
        audio_files = st.file_uploader("Upload your meeting audio(s) here and click 'Process'", accept_multiple_files=True, type=["mp3"])

        if audio_files:
            file_paths = []
            for audio_file in audio_files:
                file_paths.append(process_audio_file(audio_file))

            if st.button("Process"):
                with st.spinner("Processing"):

                    # get combined transcript
                    transcript = []
                    for file_path in file_paths:
                        transcript.append(get_transcript(file_path))
                    
                    # delete local copies
                    for file_path in file_paths:
                        delete_temp_file(file_path)

                    # get text chunks
                    text_chunks = get_text_chunks("".join(transcript))
                    
                    # get vector store using embeddings
                    vector_store = get_vector_store(text_chunks)

                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(vector_store)


if __name__ == "__main__":
    main()