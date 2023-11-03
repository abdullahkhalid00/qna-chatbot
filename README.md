# Google Meet AI Assistant

This repository contains a Streamlit web application that allows users to chat with multiple PDF documents. The application enables users to ask questions about their uploaded PDFs and provides answers based on the content of those documents.

## Installation

To run this application, you need to install the required dependencies. You can do this using `pip` and the provided `requirements.txt` file.
```
pip install -r requirements.txt
```

## Usage

To launch the application, use the following command:
```
streamlit run main.py
```
This will start the Streamlit web app, which you can access in your web browser.

## Working

### PDF Processing

The application takes one or more PDF documents as input. It extracts text from these PDFs using the PyPDF2 library. The extracted text is then split into smaller chunks for further processing.

### Text Chunking

The text is split into smaller chunks using the CharacterTextSplitter from the langchain library. This splitting is done to create more manageable units for analysis. Chunks are defined with specific sizes and an overlap to ensure that no important information is missed.

### Text Embeddings

The langchain library is used to obtain text embeddings. In this application, Hugging Face's Instruct model is used for text embeddings. The embeddings capture the semantic information in the text chunks.

### Vector Store

The application creates a vector store using the obtained embeddings. The vector store enables efficient similarity search and retrieval of relevant information.

### User Interaction

Users can interact with the application by asking questions about the uploaded PDFs. The application then searches for relevant answers within the vector store based on the embeddings of the questions and the PDF content.

### Configuration

The application uses environment variables to configure settings. You can set these variables in a .env file. You may need to customize the settings to suit your specific use case.

## Contributing

If you'd like to contribute to this project, please follow the standard open-source guidelines. You can fork the repository, make changes, and create a pull request.

## License

This project is licensed under the MIT License. You can find the full license details in the [LICENSE](LICENSE) file.

## Acknowledgments
- Streamlit: https://streamlit.io/
- PyPDF2: https://github.com/mstamy2/PyPDF2
- Hugging Face Transformers: https://huggingface.co/transformers/
- Langchain: [GitHub Repository](https://github.com/langchain-ai)

## Contact

If you have any questions or issues related to this project, please feel free to contact the author(s).

- [Abdullah Khalid](iabdulahk@gmail.com)
- [Dawood Ahmad Khan](dawoodk0007@gmail.com)
- [Zeeshan Ahmed](zeeshanahmed8064@outlook.com)