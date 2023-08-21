import html
import tkinter as tk

THEME_COLOR = "#375362"
FONT = ("Arial", 20, "italic")


class Question:

    def __init__(self, q_text, q_answer):
        self.text = q_text
        self.answer = q_answer


class QuizBrain:

    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        # Return True if there are still questions in the question list,
        # otherwise return False
        return self.question_number < len(self.question_list)

    def next_question(self):
        # Display the current question text and prompts the user for an answer
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer):
        # Check if the user's answer is correct and updates the score
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = tk.Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Label
        self.score_label = tk.Label(text="SCORE: 0", bg=THEME_COLOR, fg="white")
        self.score_label.grid(column=1, row=0)

        # Canvas
        self.canvas = tk.Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150,
            125,
            text="Some question",
            fill=THEME_COLOR,
            width=280,
            font=FONT)

        self.canvas.grid(column=0, row=1, columnspan=2, pady=50)

        # Buttons
        false_img = tk.PhotoImage(file="quizzler_false.png")
        self.false_button = tk.Button(image=false_img, highlightthickness=0, command=self.question_false)
        self.false_button.grid(column=0, row=2)
        true_img = tk.PhotoImage(file="quizzler_true.png")
        self.true_button = tk.Button(image=true_img, highlightthickness=0, command=self.question_true)
        self.true_button.grid(column=1, row=2)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            # Update the score
            self.score_label.config(text=f"SCORE: {self.quiz.score}")
            # Retrieve the next question
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
            # Enable buttons
            self.true_button.config(state="normal")
            self.false_button.config(state="normal")
        else:
            self.canvas.itemconfig(self.question_text, text="The End!")

    def question_true(self):
        # Handle the "True" button click and give feedback
        self.give_feedback(self.quiz.check_answer("True"))
        # Disable buttons until next question is displayed
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")

    def question_false(self):
        # Handle the "False" button click and give feedback
        self.give_feedback(self.quiz.check_answer("False"))
        # Disable buttons until next question is displayed
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")

    def give_feedback(self, correct_answer):
        # Provide feedback based on the correctness of the answer
        if correct_answer:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        # Get a new question after 1 second
        self.window.after(1000, self.get_next_question)