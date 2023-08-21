# Download quiz_data.py and quiz_brain.py (located on this repository)
# And move them to same folder of this file
from quiz_data import question_data
from quiz_brain import QuizBrain, Question

# Empty list to store the question objects
question_bank = []

# Loop through the question data and create a new Question object for each question
for question in question_data:
    # Extract the question text and answer from the dictionary
    question_text = question["question"]
    question_answer = question["correct_answer"]
    # Create a new Question object
    new_question = Question(question_text, question_answer)
    # Add the new question object to the question_bank list
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    # Ask the next question and check if the user's answer is correct
    quiz.next_question()

# When the while loop is over, print final message + final score
print("You've completed the quiz!")
print(f"Your final score is: {quiz.score}/{quiz.question_number}.")
