## 개요
- 이 프로젝트는 KMMULU Criminal-Law 카테고리 평가를 위한 Agent System입니다.
- 모든 코드는 도커 환경에서 실행됩니다.

## ★★★★★빠른 시작★★★★★
1. **.env 파일 확인**
   - api key가 저장된 .env 파일이 루트 디렉토리에 존재 하는지 확인.

2. **도커 이미지 빌드**
   ```sh
   docker build -t legal-agent .
   ```
3. **★★★컨테이너 통해 바로 실행★★★★**
   
   **방법 1: Docker Compose (권장)**
   ```sh
   docker-compose up --build  # 한 줄로 다 끝.
   ```
   
   **방법 2: Docker run**
   ```sh
   docker run --rm -v ${PWD}/data:/app/data --env-file .env legal-agent
   ```
   
   **PowerShell의 경우:**
   ```powershell
   docker run --rm -v ${PWD}/data:/app/data --env-file .env legal-agent
   ```
   결과 창에 성능 확인 가능 및 data/output.jsonl에서 예측/정답 확인 가능
   ```
---

## 입력/출력 파일 안내
- 입력: `data/test.jsonl` (KMMLU test셋)
- 출력: `data/output.jsonl` (예측 결과)

## 개발 환경
1. Poetry 설치
   ```sh
   pip install poetry
   ```
2. 패키지 설치
   ```sh
   poetry install
   ```
3. 환경 변수 설정
   - `.env` 파일이 이미 포함되어 있습니다.
4. 실행
   ```sh
   poetry run python scripts/run_agent.py
   ```
   - 위 명령어를 실행하면 평가가 자동으로 진행되어 output.jsonl이 생성됩니다.

---

## 디렉토리 구조
legal-agent/  
├── agent/                        # 에이전트 핵심 로직 폴더  
│   ├── agent.py                  # 입력을 받아 모델을 호출하고 결과를 생성하는 메인 코드  
│   └── __init__.py               # 파이썬 패키지 인식용 파일  
├── scripts/                      # 실행 및 데이터 처리 스크립트 폴더  
│   ├── run_agent.py              # 입력 파일을 읽고 에이전트를 실행하는 메인 스크립트  
│   └── data_preprocessing.py     # raw data를 임베딩 및 전처리하여 FAISS DB에 저장하는 스크립트 (RAG용)  
├── data/                         # 입력/출력 및 RAG용 데이터 폴더  
│   ├── test.jsonl                # 평가용 입력 데이터 (예: KMMLU test셋)  
│   ├── output.jsonl              # 예측 결과 파일  
│   /raw data ── 형사소송 등4개개.docx # RAG에 사용할 raw data (한국법령정보센터 내 형법/형사소송법 등)  
├── .env                          # 환경변수 파일 (OpenAI API 키 포함)  
├── README.md                     # 프로젝트 설명서  
└── ...                           # 기타 폴더/파일 (content/, pyproject.toml 등)  
- `agent/agent.py`: Agent 핵심 로직
- `scripts/run_agent.py`: 배치 실행 스크립트
- `data/`: 입력/출력 데이터
- `data/ raw data : 원천 데이터: 형법 및 형사소송법 및 범죄피해자 보호법 (특례법) 등

## 확장성
- RAG 검색 결과를 context로 주입하여 성능 향상 가능
- 형법 아니라 민법/세법 등 여러 agent로 확장 가능 (agent 모듈화 구조)

```bash
pip install poetry
poetry install
```
