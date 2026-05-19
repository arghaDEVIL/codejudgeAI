"""
AI Feedback Service using Google Gemini
Provides intelligent code analysis and suggestions
"""

from typing import Dict, Optional
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class AIFeedbackService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.enabled = bool(self.api_key)

        if self.enabled:
            genai.configure(api_key=self.api_key)
            # Try to find an available model
            try:
                # List available models and pick the first one that supports generateContent
                available_models = []
                for m in genai.list_models():
                    if "generateContent" in m.supported_generation_methods:
                        available_models.append(m.name)

                if available_models:
                    model_name = available_models[0].replace("models/", "")
                    self.model = genai.GenerativeModel(model_name)
                    print(f"✅ Gemini AI enabled using model: {model_name}")
                else:
                    print("❌ No Gemini models support generateContent")
                    self.enabled = False
                    self.model = None
            except Exception as e:
                print(f"❌ Failed to initialize Gemini: {e}")
                self.enabled = False
                self.model = None
        else:
            self.model = None
            print("⚠️ Gemini API key not found. AI feedback disabled.")

    def generate_feedback(
        self,
        code: str,
        language: str,
        problem_title: str,
        problem_statement: str,
        status: str,
        testcase_results: list,
        execution_time: Optional[int] = None,
    ) -> Dict:

        print(f"🤖 Generating AI feedback... Enabled: {self.enabled}")

        if not self.enabled:
            print("⚠️ AI disabled, using fallback")
            return self._get_fallback_feedback(status)

        try:
            print("📝 Building context...")
            context = self._build_context(
                code,
                language,
                problem_title,
                problem_statement,
                status,
                testcase_results,
                execution_time,
            )

            prompt = f"{self._get_system_prompt()}\n\n{context}"

            print("🚀 Calling Gemini API...")
            response = self.model.generate_content(prompt)

            print("✅ Got response from Gemini")
            feedback_text = response.text.strip()

            print(f"📄 Feedback length: {len(feedback_text)} chars")

            parsed = self._parse_feedback(feedback_text, status)
            print("✅ Feedback parsed successfully")
            return parsed

        except Exception as e:
            import traceback

            print(f"❌ AI Feedback Error: {e}")
            traceback.print_exc()
            return self._get_fallback_feedback(status)

    def _get_system_prompt(self) -> str:
        return """
You are an expert programming mentor and code reviewer.

Analyze the submitted code and respond in this exact format:

## Overall Feedback
...

## Error Analysis
...

## Optimization Hints
...

## Time Complexity
...

## Space Complexity
...

## Code Quality Score
...
"""

    def _build_context(
        self,
        code: str,
        language: str,
        problem_title: str,
        problem_statement: str,
        status: str,
        testcase_results: list,
        execution_time: Optional[int],
    ) -> str:

        passed = sum(1 for r in testcase_results if r.get("status") == "Passed")
        total = len(testcase_results)

        failures = []
        for i, result in enumerate(testcase_results):
            if result.get("status") != "Passed":
                failures.append(
                    f"Testcase {i + 1}: {result.get('status')} - {result.get('error', 'Failed')}"
                )

        return f"""
Problem: {problem_title}

Statement:
{problem_statement}

Language: {language}
Status: {status}
Passed: {passed}/{total}
Execution Time: {execution_time}ms

Code:
{code}

Failures:
{chr(10).join(failures) if failures else "All testcases passed"}
"""

    def _parse_feedback(self, feedback_text: str, status: str) -> Dict:
        sections = {
            "overall_feedback": "",
            "error_analysis": "",
            "optimization_hints": "",
            "time_complexity": "Unknown",
            "space_complexity": "Unknown",
            "code_quality_score": 50,
        }

        lines = feedback_text.split("\n")
        current = "overall_feedback"

        for line in lines:
            line = line.strip()

            if "Overall Feedback" in line:
                current = "overall_feedback"
            elif "Error Analysis" in line:
                current = "error_analysis"
            elif "Optimization Hints" in line:
                current = "optimization_hints"
            elif "Time Complexity" in line:
                current = "time_complexity"
            elif "Space Complexity" in line:
                current = "space_complexity"
            elif "Code Quality Score" in line:
                current = "code_quality_score"
            elif line and not line.startswith("#"):
                if current == "code_quality_score":
                    import re

                    m = re.search(r"\d+", line)
                    if m:
                        sections[current] = int(m.group())
                else:
                    sections[current] += line + " "

        for k in sections:
            if isinstance(sections[k], str):
                sections[k] = sections[k].strip()
                # Remove "Unknown" prefix from complexity fields
                if k in ["time_complexity", "space_complexity"]:
                    sections[k] = sections[k].replace("Unknown", "").strip()

        return sections

    def _get_fallback_feedback(self, status: str) -> Dict:
        feedback_map = {
            "Accepted": {
                "overall_feedback": "Great job! Your solution passed all testcases.",
                "error_analysis": "No errors detected.",
                "optimization_hints": "Try improving readability or optimizing further.",
                "time_complexity": "Unknown",
                "space_complexity": "Unknown",
                "code_quality_score": 80,
            },
            "Wrong Answer": {
                "overall_feedback": "Your output was incorrect.",
                "error_analysis": "Check logic and edge cases.",
                "optimization_hints": "Dry run sample inputs manually.",
                "time_complexity": "Unknown",
                "space_complexity": "Unknown",
                "code_quality_score": 40,
            },
            "Time Limit Exceeded": {
                "overall_feedback": "Your solution is too slow.",
                "error_analysis": "Inefficient algorithm.",
                "optimization_hints": "Use faster approach like O(n log n) or O(n).",
                "time_complexity": "Too High",
                "space_complexity": "Unknown",
                "code_quality_score": 30,
            },
            "Runtime Error": {
                "overall_feedback": "Your code crashed.",
                "error_analysis": "Possible index error / division by zero / null access.",
                "optimization_hints": "Validate inputs and handle errors.",
                "time_complexity": "Unknown",
                "space_complexity": "Unknown",
                "code_quality_score": 20,
            },
            "Compilation Error": {
                "overall_feedback": "Your code has syntax errors.",
                "error_analysis": "Fix compiler errors.",
                "optimization_hints": "Check syntax carefully.",
                "time_complexity": "Unknown",
                "space_complexity": "Unknown",
                "code_quality_score": 10,
            },
        }

        return feedback_map.get(status, feedback_map["Wrong Answer"])


ai_feedback_service = AIFeedbackService()
