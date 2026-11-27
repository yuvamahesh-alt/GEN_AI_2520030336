
import json
import csv
import requests
from datetime import datetime

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

INPUT_FILE = "golden_set.json"
OUTPUT_FILE = "baseline_results.csv"


def evaluate_question(question_data):
    question = question_data["question"]
    expected_answer = question_data["expected_answer"]
    keywords = question_data["keywords"]

    prompt = f"""
    Answer the following question clearly and accurately.

    Question: {question}
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    try:
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        llm_answer = response.json().get("response", "").strip()
        answer_lower = llm_answer.lower()

        matched_keywords = [
            word for word in keywords
            if word.lower() in answer_lower
        ]

        missing_keywords = [
            word for word in keywords
            if word.lower() not in answer_lower
        ]

        if keywords:
            score = (len(matched_keywords) / len(keywords)) * 100
        else:
            score = 0

        status = "PASS" if score >= 60 else "REVIEW"

        return {
            "question_id": question_data["id"],
            "question": question,
            "expected_answer": expected_answer,
            "llm_answer": llm_answer,
            "matched_keywords": ", ".join(matched_keywords),
            "missing_keywords": ", ".join(missing_keywords),
            "score": round(score, 2),
            "status": status,
            "source": question_data["source"],
            "model": MODEL_NAME,
            "release": "v0.1"
        }

    except Exception as error:
        return {
            "question_id": question_data["id"],
            "question": question,
            "expected_answer": expected_answer,
            "llm_answer": f"ERROR: {error}",
            "matched_keywords": "",
            "missing_keywords": ", ".join(keywords),
            "score": 0,
            "status": "ERROR",
            "source": question_data["source"],
            "model": MODEL_NAME,
            "release": "v0.1"
        }


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        golden_set = json.load(file)

    results = []

    print("Starting baseline evaluation... - main.py:98")
    print("Model: - main.py:99", MODEL_NAME)

    for question_data in golden_set:
        print("Evaluating: - main.py:102", question_data["id"])
        result = evaluate_question(question_data)
        results.append(result)

    fieldnames = [
        "question_id",
        "question",
        "expected_answer",
        "llm_answer",
        "matched_keywords",
        "missing_keywords",
        "score",
        "status",
        "source",
        "model",
        "release"
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    successful = [r for r in results if r["status"] != "ERROR"]
    passed = sum(1 for r in results if r["status"] == "PASS")
    review = sum(1 for r in results if r["status"] == "REVIEW")
    errors = sum(1 for r in results if r["status"] == "ERROR")

    average_score = (
        sum(r["score"] for r in successful) / len(successful)
        if successful else 0
    )

    print("\n========== BASELINE EVALUATION SUMMARY ========== - main.py:135")
    print("Release Version: - main.py:136", "v0.1")
    print("Model: - main.py:137", MODEL_NAME)
    print("Total Questions: - main.py:138", len(results))
    print("Successful Responses: - main.py:139", len(successful))
    print("Passed: - main.py:140", passed)
    print("Review: - main.py:141", review)
    print("Errors: - main.py:142", errors)
    print("Average Keyword Coverage: - main.py:143", round(average_score, 2), "%")
    print("Evaluation Date: - main.py:144", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("\nBASELINE RUN COMPLETED! - main.py:145")
    print("Release v0.1 created successfully. - main.py:146")
    print("Results saved in: - main.py:147", OUTPUT_FILE)


if __name__ == "__main__":
    main()








