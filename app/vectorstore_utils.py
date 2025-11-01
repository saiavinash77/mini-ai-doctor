from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List

#storing the data in the vector store(faiss)
def create_faiss_index(texts):
    embeddings  = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_texts(texts,embeddings)


#retrieving the data 
def retrieve_similar_documents(vectorstore:FAISS,query:str,k:int = 4):
    docs = vectorstore.similarity_search(query,k=k)
    return [doc.page_content for doc in docs]
