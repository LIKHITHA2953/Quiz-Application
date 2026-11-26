import json


def load_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def search_quizzes(quizzes, keyword):
    results = []

    for quiz in quizzes:
        if keyword.lower() in quiz["title"].lower():
            results.append(quiz)

        elif keyword.lower() in quiz.get("topic", "").lower():
            results.append(quiz)

    return results