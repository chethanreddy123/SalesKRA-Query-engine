from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.llms import GooglePalm
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
recurSplitter = RecursiveCharacterTextSplitter(chunk_size=100,
                                               chunk_overlap=20,
                                               length_function=len)
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings 


with open('linux_play.txt') as lin:
  txt_lin = lin.read()
linux_docs = recurSplitter.create_documents([txt_lin])
hfEmbed = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

lin_chroma = Chroma.from_documents(documents=linux_docs, embedding=hfEmbed)


llm = GooglePalm(
    model='models/chat-bison-001',
    temperature=0,
    # The maximum length of the response
    max_output_tokens=800,
    google_api_key='AIzaSyA1fu-ob27CzsJozdr6pHd96t5ziaD87wM'
)


lin_retriever =RetrievalQA.from_chain_type(llm=llm, 
                                           chain_type="stuff", 
                                           retriever=lin_chroma.as_retriever())



print(lin_retriever("Give short summary about chethan and his experiences?")['result'])