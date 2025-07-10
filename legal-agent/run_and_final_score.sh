#!/bin/bash
set -e

# 1. 에이전트 실행 (output.jsonl 생성)
poetry run python scripts/run_agent.py

# 2. 점수 계산 (정답률만 출력, 오답 목록은 생략)
poetry run python scripts/score.py --no-detail