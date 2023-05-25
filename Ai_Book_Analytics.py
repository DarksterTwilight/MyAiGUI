# PDF Loaders. If unstructured gives you a hard time, try PyPDFLoader
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

def read_txt_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except IOError:
        print(f"Error reading file '{file_path}'.")
        return None

# Example usage
#file_path = 'openAi.txt'  # Replace with the path to your .txt file
#file_content = read_txt_file(file_path)




def load_file(file_path, query):
    OPENAI_API_KEY = read_txt_file('setup_api_and_env/openAi.txt')
    PINECONE_API_KEY = read_txt_file('setup_api_and_env/pinecone_api_key.txt')
    PINECONE_API_ENV = read_txt_file('setup_api_and_env/pinecone_env.txt')
    INDEX_NAME = read_txt_file('setup_api_and_env/index_name.txt')

    loader = PyPDFLoader(file_path)
    data = loader.load()
    print('Data Loaded :\n')
    print(data)
    # Note: If you're using PyPDFLoader then we'll be splitting for the 2nd time.
    # This is optional, test out on your own data.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    print('Splitted Text')
    print(texts)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    print('Initialized embeddings')
    # initialize pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment=PINECONE_API_ENV  # next to api key in console
    )
    index_name = INDEX_NAME
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
    llm = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)
    print('Initialized llm')
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = docsearch.similarity_search(query)
    print('Similarity Search Results: \n')
    print(docs)
    result = chain.run(input_documents=docs, question=query)
    return result


#print(load_file('PDF/book1_chapter1_1.pdf','What is the moral of the story a letter from god ?'))