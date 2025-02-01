from xrag_paillier.data_loader import DataLoader
import sys
import json
import datetime
import pickle as pkl

if len(sys.argv) != 2:
    print("Usage: python setup.py personal_data.json")
else:
    __, file_path = sys.argv
    aes_key = input("enter a key for your AES client: ")
    print("Starting to initialize embedding model and crypto clients")
    exec_context = DataLoader.init_exec_context('embd','pail','aes',aes_key)
    data_loader = DataLoader(exec_context['embd'],exec_context['pail'],exec_context['aes'])
    print("Finished")

    with open(file_path, 'r') as file:
        data = json.load(file)
    idx = 0

    index = {}
    enc_memory_db = {}

    for d in data:
        time_str = d['time']
        text_chunks = DataLoader.split_text(d['text'])
        time = datetime.datetime.fromisoformat(time_str)
        for c in text_chunks:
            index[idx] = exec_context['pail'].encrypt(exec_context['embd'].bin_embed(c))
            enc_memory_db[idx] = {"enc_text":exec_context['aes'].encrypt(c),"time":time}
            idx += 1
            
    with open('index',"wb") as f:
        pkl.dump(index,f)
    with open('db',"wb") as f:
        pkl.dump(enc_memory_db,f)