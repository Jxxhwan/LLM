import os
import json
import numpy as np
import faiss
import openai
from typing import List, Dict

# 상대 경로 사용
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

def create_faiss_index(data: List[Dict]):
    """FAISS 인덱스 생성"""
    # OpenAI 임베딩 생성
    texts = [item['text'] for item in data]
    embeddings = []
    
    for text in texts:
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-3-small"
        )
        embeddings.append(response['data'][0]['embedding'])
    
    # FAISS 인덱스 생성
    vectors = np.array(embeddings).astype('float32')
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    
    # 저장
    faiss.write_index(index, os.path.join(DATA_DIR, "faiss_index_openai.idx"))
    
    # ID 매핑 저장
    id_mapping = [item['id'] for item in data]
    with open(os.path.join(DATA_DIR, "id_mapping_openai.json"), 'w') as f:
        json.dump(id_mapping, f)

def search_law_context(query: str, k: int = 5) -> str:
    """법률 컨텍스트 검색"""
    # FAISS 인덱스 로드
    index = faiss.read_index(os.path.join(DATA_DIR, "faiss_index_openai.idx"))
    
    # ID 매핑 로드
    with open(os.path.join(DATA_DIR, "id_mapping_openai.json"), 'r') as f:
        id_mapping = json.load(f)
    
    # 원본 데이터 로드
    with open(os.path.join(DATA_DIR, "final_linked_clauses_openai.jsonl"), 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
    
    # 쿼리 임베딩 생성
    response = openai.Embedding.create(
        input=query,
        model="text-embedding-3-small"
    )
    query_embedding = np.array([response['data'][0]['embedding']]).astype('float32')
    
    # 검색
    distances, indices = index.search(query_embedding, k)
    
    # 결과 생성
    results = []
    for idx in indices[0]:
        if idx < len(data):
            results.append(data[idx])
    
    # 컨텍스트 문자열 생성
    context = "\n\n".join([f"{item['law']} {item['article']}: {item['text']}" for item in results])
    return context