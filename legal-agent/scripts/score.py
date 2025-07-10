import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
gt_path = os.path.join(DATA_DIR, "test.jsonl")
pred_path = os.path.join(DATA_DIR, "output.jsonl")

gt = {}
with open(gt_path, encoding="utf-8") as f:
    for item in map(json.loads, f):
        gt[item["id"]] = item["answer"]

pred = {}
with open(pred_path, encoding="utf-8") as f:
    for item in map(json.loads, f):
        pred[item["id"]] = item["answer"]

total = len(gt)
correct = sum(1 for k in gt if gt[k] == pred.get(k))
print(f"정답률: {correct}/{total} = {correct/total:.2%}")

