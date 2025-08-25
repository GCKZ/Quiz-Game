import tkinter as tk
import random
import pyttsx3
import speech_recognition as sr
import threading
import time

# Set up text-to-speech engine
engine = pyttsx3.init()

# Function to start the quiz for Easy level
def start_easy_level(root):
    root.destroy()  # Close the level selector screen
    start_quiz(level="easy")  # Start the easy level quiz

# Function to start the quiz for Medium level (can be expanded)
def start_medium_level(root):
    root.destroy()
    start_quiz(level="medium")

# Function to start the quiz for Hard level (can be expanded)
def start_hard_level(root):
    root.destroy()
    start_quiz(level="hard")

# Level selector screen
def level_selector_screen():
    root = tk.Tk()
    root.title("Voice Math - Multiplication Quiz")
    root.geometry("360x640")  # Android phone size for the level selector screen

    # Welcome label
    welcome_label = tk.Label(root, text="Welcome to Voice Math\nLet's Multiply", font=("Helvetica", 18))
    welcome_label.pack(pady=50)

    # Easy, Medium, Hard buttons
    easy_button = tk.Button(root, text="Easy", font=("Helvetica", 14), command=lambda: start_easy_level(root))
    easy_button.pack(pady=10)

    medium_button = tk.Button(root, text="Medium", font=("Helvetica", 14), command=lambda: start_medium_level(root))
    medium_button.pack(pady=10)

    hard_button = tk.Button(root, text="Hard", font=("Helvetica", 14), command=lambda: start_hard_level(root))
    hard_button.pack(pady=10)

    # Run the mainloop
    root.mainloop()

# Function to start the quiz
def start_quiz(level="easy"):
    quiz_window = tk.Tk()
    quiz_window.title(f"{level.capitalize()} Level Quiz")
    quiz_window.geometry("360x640")  # Android phone size for the quiz window

    # Timer and Score Labels
    timer_label = tk.Label(quiz_window, text="Time: 2:30", font=("Helvetica", 14))
    score_label = tk.Label(quiz_window, text="Score: 0", font=("Helvetica", 14))

    # Placing timer and score labels closer to each other
    timer_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")  # left-aligned
    score_label.grid(row=0, column=1, padx=100, pady=10, sticky="e")  # right-aligned

    # Question counter label (e.g., "Question 1 of 10")
    question_count_label = tk.Label(quiz_window, text="Question 1 of 10", font=("Helvetica", 18))
    question_count_label.grid(row=1, column=0, columnspan=2, pady=30, padx=90, sticky="w")

    # Make the problem label bigger, reduce padding on the sides
    problem_label = tk.Label(quiz_window, text="Problem: 0 x 0", font=("Helvetica", 24))  # Larger font size
    problem_label.grid(row=2, column=0, columnspan=2, pady=20, padx=80, sticky="w")

    # Define variables
    score = 0
    current_problem = 0  # Keep track of the current problem
    num_questions = 10  # Total number of questions
    time_left = 150  # Timer starts at 2:30 minutes (150 seconds)
    correct_answer = None
    timer_running = True  # Flag to track if the timer is still running

    # Create result label globally so we can access it from other functions
    result_label = tk.Label(quiz_window, text="", font=("Helvetica", 12))
    result_label.grid(row=3, column=0, columnspan=2, pady=10)

    # Timer function
    def update_timer():
        nonlocal time_left
        if time_left > 0:
            minutes, seconds = divmod(time_left, 60)
            timer_label.config(text=f"Time: {minutes:02}:{seconds:02}")
            time_left -= 1
            quiz_window.after(1000, update_timer)  # Decrease time by 1 second every second
        else:
            show_result(quiz_window, score)  # Show result when time runs out

    # Generate a new multiplication problem
    def new_problem():
        nonlocal correct_answer
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        correct_answer = num1 * num2
        problem_label.config(text=f"Problem: {num1} x {num2}")

    # Listen button function (Text-to-speech)
    def listen_problem():
        engine.say(f"{problem_label.cget('text').replace(' x ', ' times ')}")
        engine.runAndWait()

    # Speak button function (Speech recognition)
    def speak_answer():
        nonlocal score
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            result_label.config(text="Say your answer!")
            quiz_window.update()

            audio = recognizer.listen(source)
            try:
                answer = recognizer.recognize_google(audio)
                if answer.strip().isdigit() and int(answer.strip()) == correct_answer:
                    result_label.config(text="Correct!")
                    score += 1
                    score_label.config(text=f"Score: {score}")  # Update score
                    quiz_window.after(1000, next_question)  # Wait 1 second before moving to next question
                else:
                    result_label.config(text="Wrong! Try again.")
            except sr.UnknownValueError:
                result_label.config(text="Could not understand, please try again.")
            except sr.RequestError:
                result_label.config(text="Speech service error.")

    # Next question button function
    def next_question():
        nonlocal current_problem, time_left
        current_problem += 1
        # Update the question counter label
        question_count_label.config(text=f"Question {current_problem + 1} of {num_questions}")
        if current_problem < num_questions:
            new_problem()
            result_label.config(text="")  # Clear result label
        else:
            show_result(quiz_window, score)  # Show result when all questions are done

    # Create buttons and position them lower with reduced padding
    listen_button = tk.Button(quiz_window, text="Listen", font=("Helvetica", 14), command=listen_problem)
    listen_button.grid(row=4, column=0, padx=10, pady=10)

    speak_button = tk.Button(quiz_window, text="Speak", font=("Helvetica", 14), command=speak_answer)
    speak_button.grid(row=4, column=1, padx=10, pady=10)

    next_button = tk.Button(quiz_window, text="Next Question", font=("Helvetica", 14), command=next_question)
    next_button.grid(row=5, column=0, columnspan=2, pady=30, sticky="w", padx=110)

    new_problem()  # Start with the first question
    update_timer()  # Start the timer immediately

    quiz_window.mainloop()

# Function to show the result screen after quiz
def show_result(quiz_window, score):
    quiz_window.destroy()  # Close the quiz window

    result_window = tk.Tk()
    result_window.title("Quiz Finished")
    result_window.geometry("360x640")  # Android phone size for the result screen

    result_label = tk.Label(result_window, text=f"Your score: {score}", font=("Helvetica", 16))
    result_label.pack(pady=50)

    quit_button = tk.Button(result_window, text="Quit", font=("Helvetica", 14), command=result_window.quit)
    quit_button.pack(pady=10)

    result_window.mainloop()

# Start the level selector screen
level_selector_screen()
