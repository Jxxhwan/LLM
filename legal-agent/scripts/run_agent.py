import os
import json
from agent.agent import LegalAgent
from agent.faiss_search import search_law_context

# n-shot 예시 (직접 입력하거나 파일로 관리)
nshot_examples = [
    {
        "question": "다음 중 형법상 범죄가 아닌 것은?",
        "choices": ["A. 절도", "B. 사기", "C. 민사상 채무불이행", "D. 강도"],
        "answer": "C"
    },
    {
        "question": "다음 중 형법상 처벌 대상이 아닌 것은?",
        "choices": ["A. 절도", "B. 사기", "C. 민사상 채무불이행", "D. 강도"],
        "answer": "C",
        "explanation": "민사상 채무불이행은 형사처벌 대상이 아닙니다."
    }
]

def main():
    agent = LegalAgent(model_name="gpt-4o")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "..", "data")
    test_path = os.path.join(DATA_DIR, "test.jsonl")
    output_path = os.path.join(DATA_DIR, "output.jsonl")
    with open(test_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            item = json.loads(line)
            question = item["question"]
            choices = item["choices"]
            # RAG context 생성
            context = search_law_context(question, k=5)
            answer = agent.answer(question, choices, nshot_examples=nshot_examples, context=context)
            result = {"id": item["id"], "answer": answer}
            outfile.write(json.dumps(result, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main() 