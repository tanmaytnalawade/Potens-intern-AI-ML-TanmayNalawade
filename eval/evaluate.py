import json
import requests


API_URL = "http://127.0.0.1:8000/ask"


with open(
    "eval/questions.json",
    "r",
    encoding="utf-8"
) as file:

    evaluation_data = json.load(file)


total_questions = len(
    evaluation_data
)

successful_answers = 0


print("\nSTARTING EVALUATION...\n")


for index, item in enumerate(
    evaluation_data
):

    question = item["question"]

    expected_answer = item[
        "expected_answer"
    ]

    response = requests.post(
        API_URL,
        json={
            "question": question
        }
    )

    result = response.json()

    generated_answer = result[
        "answer"
    ]

    confidence = result.get(
        "confidence"
    )

    print(
        "\n============================================================"
    )

    print(
        f"\nQUESTION {index + 1}\n"
    )

    print(
        f"Q: {question}"
    )

    print(
        "\nPREDICTED ANSWER:\n"
    )

    print(
        generated_answer
    )

    print(
        "\nGROUND TRUTH:\n"
    )

    print(
        expected_answer
    )

    print(
        f"\nCONFIDENCE SCORE: {confidence}"
    )

    # Simple evaluation logic
    if (
        "I could not find the answer"
        not in generated_answer
    ):

        successful_answers += 1

        print(
            "\nSTATUS: SUCCESS"
        )

    else:

        print(
            "\nSTATUS: FAILED"
        )

    print(
        "\n============================================================"
    )


accuracy = (
    successful_answers /
    total_questions
) * 100


print(
    "\nFINAL EVALUATION RESULTS\n"
)

print(
    f"Total Questions: {total_questions}"
)

print(
    f"\nSuccessful Answers: {successful_answers}"
)

print(
    f"\nApprox Accuracy: {accuracy:.2f}%"
)