
class Quiz:
    def __init__(self, title, topic):
        self.title = title
        self.topic = topic
        self.questions = []

    def add_question(self, question, options, correct_answer):
        question_data = {
            "question": question,
            "options": options,
            "correct_answer": correct_answer
        }

        self.questions.append(question_data)

    def to_dict(self):
        return {
            "title": self.title,
            "topic": self.topic,
            "questions": self.questions
        }
