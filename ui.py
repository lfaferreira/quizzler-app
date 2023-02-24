from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
ACTIVE = "active"
DISABLED = "disabled"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=25, pady=25, bg=THEME_COLOR)

        self.label_score = Label(text='Score: 0', fg='white', background=THEME_COLOR)
        self.label_score.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, bg='white', highlightthickness=0)
        self.canvas_question = self.canvas.create_text(
            150,
            125,
            width=200,
            text='Quizzler Sensation',
            fill=THEME_COLOR,
            font=("Arial", 15, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        self.image_true = PhotoImage(file='./images/true.png')
        self.image_false = PhotoImage(file='./images/false.png')

        self.button_true = Button(
            image=self.image_true,
            bg=THEME_COLOR,
            highlightthickness=0,
            command=self.button_true_clicked
        )
        self.button_false = Button(
            image=self.image_false,
            bg=THEME_COLOR,
            highlightthickness=0,
            command=self.button_false_clicked
        )

        self.button_false.grid(row=2, column=0)
        self.button_true.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg='white')
        self.score_update()
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.canvas_question, text=q_text)
            self.buttons_state(ACTIVE)
        else:
            self.end_game()

    def button_false_clicked(self):
        is_right = self.quiz.check_answer('False')
        self.give_feedback(is_right)

    def button_true_clicked(self):
        is_right = self.quiz.check_answer('True')
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        self.buttons_state(DISABLED)
        if is_right:
            self.canvas.config(bg='green')
        else:
            self.canvas.config(bg='red')
        self.window.after(1000, self.get_next_question)

    def buttons_state(self, state: str):
        self.button_true.config(state=state)
        self.button_false.config(state=state)

    def score_update(self):
        self.label_score.config(text=f'Score: {self.quiz.score}')

    def end_game(self):
        self.canvas.itemconfig(self.canvas_question, text="You've reached the end of the quiz.")
        self.buttons_state(DISABLED)
