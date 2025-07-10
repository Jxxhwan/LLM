import csv
import json
import os
import requests

# 자동 다운로드 URL
csv_url = "https://huggingface.co/datasets/HAERAE-HUB/KMMLU/resolve/main/data/Criminal-Law-test.csv"

# 절대경로 기반으로 수정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
input_path = os.path.join(DATA_DIR, "Criminal-Law-test.csv")
output_path = os.path.join(DATA_DIR, "test.jsonl")

# data 폴더가 없으면 생성
os.makedirs(DATA_DIR, exist_ok=True)

# 파일이 없으면 다운로드
if not os.path.exists(input_path):
    print(f"{input_path} 파일이 없어 다운로드합니다...")
    response = requests.get(csv_url)
    response.raise_for_status()
    with open(input_path, "wb") as f:
        f.write(response.content)
    print("다운로드 완료!")
else:
    print(f"{input_path} 파일이 이미 존재합니다.")

# csv → jsonl 변환
with open(input_path, encoding="utf-8") as csvfile, open(output_path, "w", encoding="utf-8") as jsonlfile:
    reader = csv.DictReader(csvfile)
    for idx, row in enumerate(reader, 1):
        choices = [f"A. {row['A']}", f"B. {row['B']}", f"C. {row['C']}", f"D. {row['D']}"]
        answer_num = int(row['answer'])
        answer = ["A", "B", "C", "D"][answer_num - 1]
        item = {
            "id": idx,
            "question": row["question"],
            "choices": choices,
            "answer": answer
        }
        jsonlfile.write(json.dumps(item, ensure_ascii=False) + "\n")
print(f"{output_path} 변환 완료!")
