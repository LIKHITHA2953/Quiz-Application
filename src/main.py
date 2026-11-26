
from pathlib import Path

from quiz import Quiz
from utils import load_json, save_json, search_quizzes


# Project folder paths
BASE_DIR = Path(__file__).resolve().parent.parent

QUIZZES_FILE = BASE_DIR / "data" / "quizzes.json"
USERS_FILE = BASE_DIR / "data" / "users.json"


# Load data
def get_quizzes():
    return load_json(QUIZZES_FILE)


def get_users():
    return load_json(USERS_FILE)


# Save data
def save_quizzes(quizzes):
    save_json(QUIZZES_FILE, quizzes)


def save_users(users):
    save_json(USERS_FILE, users)


# 1. Create Quiz
def create_quiz():
    print("\n--- Create New Quiz ---")

    title = input("Enter quiz title: ").strip()
    topic = input("Enter quiz topic: ").strip()

    if not title or not topic:
        print("Title and topic cannot be empty.")
        return

    quizzes = get_quizzes()

    for quiz in quizzes:
        if quiz["title"].lower() == title.lower():
            print("A quiz with this title already exists.")
            return

    new_quiz = Quiz(title, topic)

    while True:
        question = input("\nEnter question: ").strip()

        if not question:
            print("Question cannot be empty.")
            continue

        options = []

        for i in range(4):
            option = input(f"Enter option {i + 1}: ").strip()

            if not option:
                print("Option cannot be empty.")
                return

            options.append(option)

        correct_answer = input("Enter correct answer: ").strip()

        if correct_answer not in options:
            print("Correct answer must match one of the options.")
            continue

        new_quiz.add_question(question, options, correct_answer)

        choice = input("Add another question? (yes/no): ").strip().lower()

        if choice != "yes":
            break

    if not new_quiz.questions:
        print("Quiz has no questions.")
        return

    quizzes.append(new_quiz.to_dict())
    save_quizzes(quizzes)

    print("\nQuiz created successfully!")


# 2. View All Quizzes
def view_all_quizzes():
    print("\n--- All Available Quizzes ---")

    quizzes = get_quizzes()

    if not quizzes:
        print("No quizzes available.")
        return

    for index, quiz in enumerate(quizzes, start=1):
        print(f"\n{index}. {quiz['title']}")
        print(f"Topic: {quiz['topic']}")
        print(f"Number of Questions: {len(quiz['questions'])}")


# 3. Search Quiz
def search_quiz():
    print("\n--- Search Quiz ---")

    keyword = input("Enter quiz title or topic: ").strip()

    if not keyword:
        print("Please enter a search keyword.")
        return

    quizzes = get_quizzes()
    results = search_quizzes(quizzes, keyword)

    if not results:
        print("No matching quizzes found.")
        return

    print("\n--- Search Results ---")

    for index, quiz in enumerate(results, start=1):
        print(f"\n{index}. {quiz['title']}")
        print(f"Topic: {quiz['topic']}")
        print(f"Questions: {len(quiz['questions'])}")


# 4. Take Quiz
def take_quiz():
    print("\n--- Take Quiz ---")

    quizzes = get_quizzes()

    if not quizzes:
        print("No quizzes available. Create a quiz first.")
        return

    for index, quiz in enumerate(quizzes, start=1):
        print(f"{index}. {quiz['title']}")

    try:
        choice = int(input("\nSelect a quiz number: "))

        if choice < 1 or choice > len(quizzes):
            print("Invalid quiz number.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    selected_quiz = quizzes[choice - 1]
    score = 0

    print(f"\nStarting Quiz: {selected_quiz['title']}")

    for index, question in enumerate(
        selected_quiz["questions"], start=1
    ):
        print(f"\nQ{index}. {question['question']}")

        for option_number, option in enumerate(
            question["options"], start=1
        ):
            print(f"{option_number}. {option}")

        try:
            answer = int(input("Enter your answer (1-4): "))

            if answer < 1 or answer > len(question["options"]):
                print("Invalid option. Question skipped.")
                continue

            selected_answer = question["options"][answer - 1]

            if selected_answer == question["correct_answer"]:
                print("Correct answer!")
                score += 1
            else:
                print("Incorrect answer.")
                print(
                    f"Correct answer: {question['correct_answer']}"
                )

        except ValueError:
            print("Invalid input. Question skipped.")

    total = len(selected_quiz["questions"])

    print("\n--- Quiz Completed ---")
    print(f"Your Score: {score}/{total}")

    username = input("Enter your name to save the result: ").strip()

    if username:
        save_quiz_result(
            username,
            selected_quiz["title"],
            score,
            total
        )
    else:
        print("Name cannot be empty. Result was not saved.")


# Save Quiz Results
def save_quiz_result(username, quiz_title, score, total):
    users = get_users()

    user_result = {
        "username": username,
        "quiz_title": quiz_title,
        "score": score,
        "total_questions": total
    }

    users.append(user_result)
    save_users(users)

    print("Quiz result saved successfully!")


# 5. View Quiz Results
def view_results():
    print("\n--- Quiz Results ---")

    results = get_users()

    if not results:
        print("No quiz results available.")
        return

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print(f"Username: {result['username']}")
        print(f"Quiz: {result['quiz_title']}")
        print(
            f"Score: {result['score']}/"
            f"{result['total_questions']}"
        )


# 6. Main Menu
def main():
    while True:
        print("\n========== QUIZ APPLICATION ==========")
        print("1. Create Quiz")
        print("2. View All Quizzes")
        print("3. Search Quiz")
        print("4. Take Quiz")
        print("5. View Quiz Results")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            create_quiz()

        elif choice == "2":
            view_all_quizzes()

        elif choice == "3":
            search_quiz()

        elif choice == "4":
            take_quiz()

        elif choice == "5":
            view_results()

        elif choice == "6":
            print("Thank you for using Quiz Application!")
            break

        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
