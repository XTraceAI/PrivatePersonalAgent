from xrag_paillier.inference.ollama import ollama_client
from xrag_paillier.retriever import ContextRetriever
from xrag_paillier.data_loader import DataLoader
from xrag_paillier.utils.config import *

#init stuff...
deepseek_inference = ollama_client(OLLAMA_URL,"deepseek-r1:1.5b")
exec_context = DataLoader.load_exec_context('embd','pail','aes')

#hybrid retriever
retriever = ContextRetriever(exec_context['pail'], exec_context['aes'], exec_context['embd'],INDEX_URL,DB_URL)

while True:
    user_input = input("Enter a query: ")
    if not user_input:
        exit()
    contexts = retriever.search_and_retrieve(user_input)
    context = ContextRetriever.format_context(contexts)
    print("LLM Answer: \n")
    result = deepseek_inference.query(RAG_PROMPT_TEMP(context,user_input))
    print("\n\n")











