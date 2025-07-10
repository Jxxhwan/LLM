import os
import openai
from typing import List, Dict, Optional
import re

class LegalAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def build_prompt(self, question: str, choices: List[str], nshot_examples: Optional[List[Dict]] = None, context: Optional[str] = None) -> str:
        prompt = "아래는 대한민국 형법에 관한 객관식 문제입니다.\n"
        if nshot_examples:
            for ex in nshot_examples:
                prompt += f"\n[예시 문제]\nQ: {ex['question']}\n"
                for c in ex['choices']:
                    prompt += f"{c}\n"
                prompt += f"정답: {ex['answer']}\n해설: {ex.get('explanation', '')}\n"
        prompt += f"\n[문제]\n{question}\n"
        prompt += "\n[선택지]\n"
        for c in choices:
            prompt += f"{c}\n"
        prompt += f"\n[근거 자료]\n{context}\n"
        prompt += (
            "\n위 근거 자료를 참고하여, 가장 적절한 답을 선택하고 해설도 작성하세요.\n"
            "정답: (A/B/C/D)\n해설:"
        )
        return prompt

    def answer(self, question: str, choices: List[str], nshot_examples: Optional[List[Dict]] = None, context: Optional[str] = None) -> str:
        prompt = self.build_prompt(question, choices, nshot_examples, context)
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=256,
        )
        return self.extract_answer(response['choices'][0]['message']['content'])

    def extract_answer(self, output: str) -> str:
        # 다양한 정답 패턴 지원
        patterns = [
            r"정답[:：]?\s*([①-④1-4A-D])",  # 번호/알파벳
            r"정답[:：]?\s*([A-D])\.",        # 알파벳+마침표
            r"정답[:：]?\s*([가-힣]+)",        # 한글 선택지
        ]
        for pat in patterns:
            match = re.search(pat, output)
            if match:
                return match.group(1)
        # fallback: 첫 줄, 첫 단어 등
        return output.strip().split()[0] if output.strip() else ""

    def extract_answer_and_explanation(self, output: str):
        answer_match = re.search(r"정답[:：]?\s*([A-D])", output)
        explanation_match = re.search(r"해설[:：]?(.*)", output, re.DOTALL)
        answer = answer_match.group(1) if answer_match else ""
        explanation = explanation_match.group(1).strip() if explanation_match else ""
        return answer, explanation

    def answer_with_explanation(self, prompt: str):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=512,
        )
        output = response['choices'][0]['message']['content']
        return self.extract_answer_and_explanation(output) 