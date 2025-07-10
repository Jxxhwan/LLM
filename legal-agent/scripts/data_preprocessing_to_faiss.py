import json
import os
from pathlib import Path
from agent.faiss_search import create_faiss_index

def main():
    # 상대 경로 사용
    data_dir = Path("data")
    raw_data_dir = data_dir / "raw data"
    output_file = data_dir / "final_linked_clauses_openai.jsonl"
    
    # 원본 데이터 로드
    with open(output_file, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]
    
    # FAISS 인덱스 생성
    create_faiss_index(data)

if __name__ == "__main__":
    main()