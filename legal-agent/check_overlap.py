# 이 파일은 문제와 RAG 인덱스의 중복 여부를 확인하는 스크립트입니다.
# 치팅 여부를 확인하는 용도로 사용합니다.
# 
import json

# test.jsonl 문제/선택지 추출
test_questions = set()
with open("data/test.jsonl", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        test_questions.add(item["question"].strip())

# RAG 인덱스(예: final_linked_clauses_openai.jsonl)에서 텍스트 추출
rag_texts = set()
with open("data/final_linked_clauses_openai.jsonl", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        rag_texts.add(item["text"].strip())

# 중복 여부 확인
overlap = test_questions & rag_texts
print(f"중복된 문제/조문 개수: {len(overlap)}")
if overlap:
    print("중복 예시:", list(overlap)[:5])