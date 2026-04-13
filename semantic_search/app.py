from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from .search import embed_texts, label_batch

app = FastAPI(title='Semantic Search API')

class TextsRequest(BaseModel):
    texts: List[str]

@app.post('/embed')
async def embed(req: TextsRequest):
    try:
        vectors = embed_texts(req.texts)
        return {'embeddings': vectors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/label')
async def label(req: TextsRequest):
    try:
        labels = label_batch(req.texts)
        return {'labels': labels}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
