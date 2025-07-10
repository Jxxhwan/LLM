#!/bin/bash
set -e

echo "==== 1. 데이터 전처리 및 임베딩 시작 ===="
poetry run python scripts/data_preprocessing_to_faiss.py

echo "==== 2. 평가(문제풀이) 시작 ===="
poetry run python scripts/run_agent.py

echo "==== 3. 성능 평가(채점) 시작 ===="
poetry run python scripts/score.py --no-detail

echo "==== 4. 모든 작업 완료! ===="