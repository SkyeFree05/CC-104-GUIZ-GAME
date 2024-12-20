import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import random
import pygame
from playsound import playsound


# File to store scores
SCORES_FILE = "scores.json"

# Questions and answers
questions = [
    {"question": "The Earth is flat.", "answer": "False"},
    {"question": "Python is a programming language.", "answer": "True"},
    {"question": "The sun revolves around the Earth.", "answer": "False"},
    {"question": "2 + 2 equals 4.", "answer": "True"},
    {"question": "The Eiffel Tower is located in Berlin.", "answer": "False"},
    {"question": "Venus is the closest planet to the Sun.", "answer": "False"},
    {"question": "The first man to walk on the Moon was Neil Armstrong.", "answer": "True"},
    {"question": "Water freezes at 0 degrees Celsius under normal conditions.",
     "answer": "True"},
    {"question": "The capital of Australia is Sydney.",
     "answer": "False"},
    {"question": "Albert Einstein developed the theory of relativity.",
     "answer": "True"},
    {"question": "Shakespeare wrote 'To be, or not to be'.",
     "answer": "True"},
    {
        "question": "H2O is the chemical formula for oxygen.",
        "answer": "False"},
    {
        "question": "The Eiffel Tower is in Berlin.",
        "answer": "False"},
    {
        "question": "The piano has 88 keys.",
        "answer": "True"},
    {
        "question": "The human body has 206 bones.",
        "answer": "True"},
    {
        "question": "Venus is the hottest planet in the Solar System.",
        "answer": "True"},
    {
        "question": "The chemical symbol for gold is Au.",
        "answer": "True"},
    {
        "question": "The Atlantic Ocean is the largest ocean on Earth.",
        "answer": "False"},
    {
        "question": "The Mona Lisa was painted by Vincent van Gogh.",
        "answer": "False"},
    {
        "question": "A leap year has 366 days.",
        "answer": "True"},
    {
        "question": "Mount Everest is over 9,000 meters tall.",
        "answer": "True"},
    {
        "question": "The capital city of Japan is Kyoto.",
        "answer": "False"},
    {
        "question": "Honey never spoils.",
        "answer": "True"},
    {
        "question": "The speed of sound is faster in water than in air.",
        "answer": "True"},
    {
        "question": "Rome was founded in 753 BCE.",
        "answer": "True"},
    {
        "question": "The Sahara is the largest desert in the world.",
        "answer": "False"},
    {"question": "A stack is a LIFO data structure.", "answer": "True"},
    {"question": "A binary search tree is balanced by default.", "answer": "False"},
    {"question": "Queues follow the FIFO principle.", "answer": "True"},
    {"question": "Graphs can only have undirected edges.", "answer": "False"},

]

# GUI
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("True or False Quiz")
        self.root.geometry("500x400")

        self.username = ""
        self.current_question = 0
        self.score = 0

        # Frames
        self.main_menu_frame = tk.Frame(root)
        self.quiz_frame = tk.Frame(root)
        self.result_frame = tk.Frame(root)

        self.setup_main_menu()
        self.setup_quiz_frame()
        self.setup_result_frame()

        self.main_menu_frame.pack()

    def setup_main_menu(self):
        """Set up the main menu frame."""
        tk.Label(self.main_menu_frame, text="Welcome to the Quiz!", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.main_menu_frame, text="Enter your name:", font=("Arial", 14)).pack(pady=10)
        self.username_entry = tk.Entry(self.main_menu_frame, font=("Arial", 14))
        self.username_entry.pack(pady=10)
        tk.Button(self.main_menu_frame, text="Start Quiz", font=("Arial", 14,), bg="green", command=self.start_quiz).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Exit", font=("Arial", 14), bg="red" , command=self.root.quit).pack(pady=10)

    def setup_quiz_frame(self):
        """Set up the quiz frame."""
        self.question_label = tk.Label(self.quiz_frame, text="", font=("Arial", 35), wraplength=450)
        self.question_label.pack(pady=30)

        self.true_button = tk.Button(self.quiz_frame, text="True", font=("Arial", 22, "bold"),
                                     command=lambda: self.check_answer("True"), bg="green", fg="white")
        self.true_button.pack(side=tk.RIGHT, padx=178)

        self.false_button = tk.Button(self.quiz_frame, text="False", font=("Arial",22, "bold"),
                                      command=lambda: self.check_answer("False"), bg="red", fg="white")
        self.false_button.pack(side=tk.LEFT, padx=178)

    def setup_result_frame(self):
        """Set up the result frame."""
        self.result_label = tk.Label(self.result_frame, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)
        self.leaderboard_label = tk.Label(self.result_frame, text="", font=("Arial", 12))
        self.leaderboard_label.pack(pady=20)

        tk.Button(self.result_frame, text="Try Again", font=("Arial", 14), command=self.reset_quiz).pack(pady=10)
        tk.Button(self.result_frame, text="Exit", font=("Arial", 14), command=self.root.quit).pack(pady=10)

    def play_sound(self, sound_file):
        """Play a sound file."""
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def check_answer(self, answer):
        """Check if the user's answer is correct."""
        correct_answer = self.questions[self.current_question]["answer"]

        if answer == correct_answer:
            self.score += 1
            self.play_sound("corecttt.mp3")
            messagebox.showinfo("Result", "Correct!")
        else:
            self.play_sound("wronggg.mp3")
            messagebox.showinfo("Result", "Incorrect!")

        self.current_question += 1
        self.show_question()

    def start_quiz(self):
        """Start the quiz after validating the username."""
        self.username = self.username_entry.get().strip()
        if not self.username:
            messagebox.showerror("Error", "Please enter a valid name.")
            return

        self.main_menu_frame.pack_forget()
        self.current_question = 0
        self.score = 0
        self.questions = random.sample(questions, 15)  # Randomly select 15 questions
        self.show_question()

    def show_question(self):
        """Display the current question."""
        if self.current_question < len(self.questions):
            self.question_label.config(text=self.questions[self.current_question]["question"])
            self.quiz_frame.pack()
        else:
            self.end_quiz()

    def end_quiz(self):
        """Show the final score and end the quiz."""
        self.save_score()
        self.quiz_frame.pack_forget()
        self.show_leaderboard()

    def save_score(self):
        """Save the user's score to a JSON file."""
        scores = self.load_scores()
       # playsound("yay.mp3")
        scores.append({"username": self.username, "score": self.score})
        scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:5]  # Keep top 5 scores
        with open(SCORES_FILE, "w") as f:
            json.dump(scores, f, indent=4)

    def load_scores(self):
        """Load scores from a JSON file."""
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, "r") as f:
                return json.load(f)
        return []

    def show_leaderboard(self):
        """Display the leaderboard with the final score."""
        scores = self.load_scores()
        leaderboard_text = "\n".join([f"{entry['username']}: {entry['score']}" for entry in scores])
        self.result_label.config(text=f"Quiz Over!\n\n{self.username}, your score is {self.score}/{len(self.questions)}.")
        self.leaderboard_label.config(text=f"Top 5 Leaderboard:\n\n{leaderboard_text}")
        self.result_frame.pack()

    def reset_quiz(self):
        """Reset the quiz to start again."""
        self.result_frame.pack_forget()
        self.username_entry.delete(0, tk.END)
        self.main_menu_frame.pack()

# Create the main window
root = tk.Tk()
root.config(bg="white")

# Load the logo image
logo_image = Image.open("timequiz.jpg")
logo_image_tk = ImageTk.PhotoImage(logo_image)

# Create a label with the logo image
logo_label = tk.Label(root, image=logo_image_tk)
logo_label.image = logo_image_tk  # Keep a reference to the image
logo_label.pack()

# Start the app
if __name__ == "__main__":
    app = QuizApp(root)
    root.mainloop()