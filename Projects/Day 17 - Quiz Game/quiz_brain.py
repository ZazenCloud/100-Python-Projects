class Question:

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer


class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.question_list = q_list
        self.score = 0

    def still_has_questions(self):
        # Returns True if there are still questions in the question list,
        # otherwise returns False
        return self.question_number < len(self.question_list)

    def next_question(self):
        # Displays the current question text, prompts the user for an answer
        current_question = self.question_list[self.question_number]
        self.question_number += 1
        # Prompts the user for an answer
        user_answer = input(
            f'Q.{self.question_number}: {current_question.text}'
            '\nTrue or False? '
        ).lower()
        # Convert "t" to "true" and "f" to "false"
        if user_answer == "t":
            user_answer = "true"
        elif user_answer == "f":
            user_answer = "false"
        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer, correct_answer):
        # Checks if the user's answer is correct and updates the score
        if user_answer == correct_answer.lower():
            self.score += 1
            print("You got it right!")
        else:
            print("Wrong!")
            print(f"The correct answer was: {correct_answer}.")
        # Displays the current score and the total number of questions answered
        print(f"Your current score is: {self.score}/{self.question_number}")
        print("")
