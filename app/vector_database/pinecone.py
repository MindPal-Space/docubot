import pinecone 

def init_pinecone_index(PINECONE_API_KEY: str, environment: str, index_name: str, dimension: int, metric: str):
    pinecone.init(
        api_key = PINECONE_API_KEY,  
        environment = environment 
    )

    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            index_name,
            dimension = dimension,
            metric = metric
        )

    index = pinecone.Index(index_name)
    return index

def upload_document(embedding, index: pinecone.Index, documents: list, document_id: str, batch_size: int = 64):
        for i in range(0, len(documents), batch_size):
            i_end = min(i+batch_size, len(documents))
            batch = documents[i:i_end]

            emb = embedding.embed_documents(batch)
            meta = [{"document_id": document_id,
                    "text": documents[i]} for i in range(i, i_end)]
            ids = [f"{idx}" for idx in range(i, i_end)]
            to_upsert = list(zip(ids, emb, meta))
            _ = index.upsert(vectors=to_upsert)
        return {"status": "success"}


def get_context(embedding, document_id: str, index: pinecone.Index, query: str, top_k: int = 5) -> str:
    xq = embedding.embed_query(query)
    xc = index.query(xq, 
                     top_k=top_k, 
                     include_metadata=True,
                     filter={"document_id": document_id})
    context = " ".join([x["metadata"]['text'] for x in xc["matches"]])
    return context
