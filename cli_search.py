# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "faiss",
# ]
# ///
import os
import faiss 
import pandas as pd
import numpy as np

from openai import OpenAI
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

index_path = "res/index.bin"
info_path = "res/combined.csv"


def init():
    if not os.path.exists(index_path):
        raise Exception("Index not found. Run json_to_vec.py first.")
    if not os.path.exists(info_path):
        raise Exception("Combined CSV not found. Run json_to_vec.py first.")
    
    df = pd.read_csv(info_path)
    index = faiss.read_index(index_path)
    return df, index


def search_index(index, query, k=50):
    query_emb = get_embedding(query)
    # df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
    query_emb = np.array(query_emb).reshape(1, -1)
    D, I = index.search(query_emb, k)
    return D, I


def main():
    df, index = init()
    while True:
        print("\n" * 50)
        query = input("Enter a query: ")
        if query == "exit":
            break
        D, I = search_index(index, query)
        for i in range(len(I[0])):
            print(f"Score: {D[0][i]}")
            info = df.iloc[I[0][i]]
            print(f"{info.book} {info.volume} {info.parva} {info.chapter} {info.shloka}")
            print(f"Link: http://rahular.com/itihasa/gen/{info.book}/{info.volume}/{info.cnum}.html#{info.shloka}")
            print(f"Shloka: {info.sn}")
            print(f"Translation: {info.en}")
            print()
    

if __name__ == "__main__":
    main()
