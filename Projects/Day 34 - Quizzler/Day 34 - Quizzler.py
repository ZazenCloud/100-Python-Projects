from quizzler_brain import QuizBrain, QuizInterface, Question
from quizzler_data import question_data

# Empty list to store the question objects
question_bank = []

# Loop through the question data and create
# a new Question object for each question
for question in question_data:
    # Extract the question text and answer from the dictionary
    question_text = question["question"]
    question_answer = question["correct_answer"]
    # Create a new Question object
    new_question = Question(question_text, question_answer)
    # Add the new question object to the question_bank list
    question_bank.append(new_question)

# Create a QuizBrain object with the question_bank list
quiz = QuizBrain(question_bank)
# Create a QuizInterface object with the quiz
quiz_ui = QuizInterface(quiz)
