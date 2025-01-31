from flask import Flask, jsonify, request, Response
from xrag_paillier.crypto_clients.paillier_client import client
import pickle as pkl
import json
import io


app = Flask(__name__)



"""
Needs DB and Index

DB: {idx: {enc_text:aes_cipher,time:time_stamp}}
Index {idx: encrpted_embd_repr}
"""

with open("db","rb") as f:
    db = pkl.load(f)

with open("index", "rb") as f:
    index = pkl.load(f)


@app.route('/')
def hello():
    return "hello"

@app.route('/api/hamming',methods=['POST'])
def get_hamming():
    data = pkl.loads(request.get_data())
    query = data['query']
    print('[LOG] USER query:',query) #a curious server logs user query
    res = []
    for v in index.values():
        res.append(v+query)
    res_bytes = io.BytesIO(pkl.dumps(res))
    return Response(res_bytes,mimetype='application/zip')

@app.route('/api/chunk/<chunk_id>',methods=['GET'])
def get_chunk(chunk_id):
    #TODO: better id system for chunks, should work for now
    print('[LOG] Returned Data:',db[int(chunk_id)]['enc_text'])
    return db[int(chunk_id)]['enc_text'] #returns aes cipher String


if __name__ == '__main__':
   app.run(debug=True,port=8080)