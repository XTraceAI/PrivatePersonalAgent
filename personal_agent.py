from xrag_paillier.inference.ollama import ollama_client
from xrag_paillier.retriever import ContextRetriever
from xrag_paillier.data_loader import DataLoader
from xrag_paillier.utils.config import *

#initialization...
deepseek_inference = ollama_client(OLLAMA_URL,"deepseek-r1:1.5b")
exec_context = DataLoader.load_exec_context('embd','pail','aes')

#hybrid retriever
retriever = ContextRetriever(exec_context['pail'], exec_context['aes'], exec_context['embd'],INDEX_URL,DB_URL)

Prompt= """
Role:
You are a Personal Life Assistant AI Agent with access to:
- Screenshots from the user’s device (converted to text)
- Audio transcripts (converted to text)
- A RAG system for data retrieval

Your goal is to provide accurate, context-aware responses based on this data.

Capabilities:
Assist with:
- Shopping: Track purchases, find receipts, recommend items
- Traveling: Retrieve itineraries, reservations, flight, and hotel details
- Research: Summarize notes, retrieve documents, answer related questions
- Invoices: Locate invoices, summarize billing, track due payments

Response Guidelines:
- Use retrieved data for specific, accurate answers
- Keep responses concise and clear
- Ensure privacy, referencing only relevant data
- Ask clarifying questions if needed

"""

while True:
    # user_input = input("enter time stan")
    user_input = input("Enter a query: ")
    if not user_input:
        exit()
    contexts = retriever.search_and_retrieve(user_input,k=2)
    context = ContextRetriever.format_context(contexts)
    print("LLM Answer: \n")
    # print("RAG Prompt Temp:", RAG_PROMPT_TEMP(context,user_input))

    # result = deepseek_inference.query(My_prompt)
    result = deepseek_inference.query(RAG_PROMPT_TEMP(context,user_input))

    print("\n\n")











