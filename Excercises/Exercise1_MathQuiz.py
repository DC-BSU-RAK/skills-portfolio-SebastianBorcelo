import tkinter as tk
from tkinter import messagebox
import random

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')  # Dark blue background
        
        # Quiz variables
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.current_attempt = 1
        self.num1 = 0
        self.num2 = 0
        self.operation = ''
        self.correct_answer = 0
        
        # Create widgets
        self.create_widgets()
        self.show_difficulty_menu()
    
    def create_widgets(self):
        # Main container with dark blue background
        self.main_container = tk.Frame(self.root, bg='#1a1a2e')
        self.main_container.pack(expand=True, fill='both')
        
        # Side panel for score and progress
        self.side_panel = tk.Frame(self.main_container, width=200, bg='#16213e', 
                                  relief='raised', bd=2)
        self.side_panel.pack(side='left', fill='y', padx=5, pady=5)
        self.side_panel.pack_propagate(False)
        
        # Content area for questions and interface
        self.content_area = tk.Frame(self.main_container, bg='#1a1a2e')
        self.content_area.pack(side='right', expand=True, fill='both', padx=5, pady=5)
        
        # Setup side panel widgets
        self.setup_side_panel()
        
        # Setup content area frames
        self.setup_content_frames()
    
    def setup_side_panel(self):
        """Setup the side panel with score and progress info"""
        # Title
        title_label = tk.Label(self.side_panel, text="QUIZ STATS", 
                              font=('Impact', 16, 'bold'), 
                              fg='#e94560', bg='#16213e')
        title_label.pack(pady=20)
        
        # Score display
        self.score_frame = tk.Frame(self.side_panel, bg='#0f3460', relief='sunken', bd=2)
        self.score_frame.pack(pady=10, padx=10, fill='x')
        
        score_title = tk.Label(self.score_frame, text="SCORE", 
                              font=('Impact', 14, 'bold'), 
                              fg='#4cc9f0', bg='#0f3460')
        score_title.pack(pady=5)
        
        self.score_label = tk.Label(self.score_frame, text="0", 
                                   font=('Impact', 24, 'bold'), 
                                   fg='#4ade80', bg='#0f3460')
        self.score_label.pack(pady=10)
        
        # Progress display
        self.progress_frame = tk.Frame(self.side_panel, bg='#0f3460', relief='sunken', bd=2)
        self.progress_frame.pack(pady=10, padx=10, fill='x')
        
        progress_title = tk.Label(self.progress_frame, text="PROGRESS", 
                                 font=('Impact', 14, 'bold'), 
                                 fg='#4cc9f0', bg='#0f3460')
        progress_title.pack(pady=5)
        
        self.progress_label = tk.Label(self.progress_frame, 
                                      text="0/10", 
                                      font=('Impact', 18, 'bold'), 
                                      fg='#fbbf24', bg='#0f3460')
        self.progress_label.pack(pady=10)
        
        # Difficulty display
        self.diff_frame = tk.Frame(self.side_panel, bg='#0f3460', relief='sunken', bd=2)
        self.diff_frame.pack(pady=10, padx=10, fill='x')
        
        diff_title = tk.Label(self.diff_frame, text="DIFFICULTY", 
                             font=('Impact', 14, 'bold'), 
                             fg='#4cc9f0', bg='#0f3460')
        diff_title.pack(pady=5)
        
        self.diff_label = tk.Label(self.diff_frame, text="-", 
                                  font=('Impact', 16, 'bold'), 
                                  fg='#a855f7', bg='#0f3460')
        self.diff_label.pack(pady=10)
    
    def setup_content_frames(self):
        """Setup the main content area frames"""
        # Difficulty selection frame
        self.difficulty_frame = tk.Frame(self.content_area, bg='#1a1a2e')
        
        # Quiz frame
        self.quiz_frame = tk.Frame(self.content_area, bg='#1a1a2e')
        
        # Results frame
        self.results_frame = tk.Frame(self.content_area, bg='#1a1a2e')
        
        # Setup difficulty frame
        self.setup_difficulty_frame()
        
        # Setup quiz frame
        self.setup_quiz_frame()
        
        # Setup results frame
        self.setup_results_frame()
    
    def setup_difficulty_frame(self):
        """Setup the difficulty selection interface"""
        title_label = tk.Label(self.difficulty_frame, 
                              text="SELECT DIFFICULTY LEVEL", 
                              font=('Impact', 24, 'bold'), 
                              fg='#e94560', bg='#1a1a2e')
        title_label.pack(pady=40)
        
        self.easy_btn = tk.Button(self.difficulty_frame, text="EASY", 
                                 font=('Impact', 18), width=15, height=2,
                                 bg='#4ade80', fg='white',
                                 activebackground='#22c55e', activeforeground='white',
                                 command=lambda: self.set_difficulty("easy"))
        self.easy_btn.pack(pady=15)
        
        self.moderate_btn = tk.Button(self.difficulty_frame, text="MODERATE", 
                                     font=('Impact', 18), width=15, height=2,
                                     bg='#fbbf24', fg='white',
                                     activebackground='#f59e0b', activeforeground='white',
                                     command=lambda: self.set_difficulty("moderate"))
        self.moderate_btn.pack(pady=15)
        
        self.advanced_btn = tk.Button(self.difficulty_frame, text="ADVANCED", 
                                     font=('Impact', 18), width=15, height=2,
                                     bg='#e94560', fg='white',
                                     activebackground='#dc2626', activeforeground='white',
                                     command=lambda: self.set_difficulty("advanced"))
        self.advanced_btn.pack(pady=15)
    
    def setup_quiz_frame(self):
        """Setup the quiz interface"""
        self.question_label = tk.Label(self.quiz_frame, text="", 
                                      font=('Impact', 36, 'bold'), 
                                      fg='#ffffff', bg='#1a1a2e')
        self.question_label.pack(pady=60)
        
        self.answer_entry = tk.Entry(self.quiz_frame, font=('Impact', 24), 
                                    width=10, justify='center', bd=3, relief='sunken',
                                    bg='#0f3460', fg='white', insertbackground='white')
        self.answer_entry.pack(pady=30)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
        
        self.submit_btn = tk.Button(self.quiz_frame, text="SUBMIT ANSWER", 
                                   font=('Impact', 16), width=15, height=2,
                                   bg='#4cc9f0', fg='white',
                                   activebackground='#3b82f6', activeforeground='white',
                                   command=self.check_answer)
        self.submit_btn.pack(pady=20)
        
        self.feedback_label = tk.Label(self.quiz_frame, text="", 
                                      font=('Impact', 14), 
                                      fg='#e94560', bg='#1a1a2e')
        self.feedback_label.pack(pady=10)
    
    def setup_results_frame(self):
        """Setup the results interface"""
        self.results_label = tk.Label(self.results_frame, text="", 
                                     font=('Impact', 28, 'bold'), 
                                     fg='#ffffff', bg='#1a1a2e')
        self.results_label.pack(pady=40)
        
        self.rank_label = tk.Label(self.results_frame, text="", 
                                  font=('Impact', 24), 
                                  fg='#a855f7', bg='#1a1a2e')
        self.rank_label.pack(pady=20)
        
        self.play_again_btn = tk.Button(self.results_frame, text="PLAY AGAIN", 
                                       font=('Impact', 18), width=15, height=2,
                                       bg='#4ade80', fg='white',
                                       activebackground='#22c55e', activeforeground='white',
                                       command=self.restart_quiz)
        self.play_again_btn.pack(pady=30)
    
    def flash_screen(self, color):
        """Flash the entire screen with the specified color"""
        flash_frame = tk.Frame(self.root, bg=color)
        flash_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        def remove_flash():
            flash_frame.destroy()
        
        self.root.after(200, remove_flash)  # Flash for 200ms
    
    def displayMenu(self):
        """Display the difficulty level menu"""
        self.hide_all_frames()
        self.difficulty_frame.pack(expand=True, fill='both')
    
    def show_difficulty_menu(self):
        """Wrapper function to show difficulty menu"""
        self.displayMenu()
    
    def hide_all_frames(self):
        """Hide all frames"""
        self.difficulty_frame.pack_forget()
        self.quiz_frame.pack_forget()
        self.results_frame.pack_forget()
    
    def set_difficulty(self, level):
        """Set the difficulty level and start the quiz"""
        self.difficulty = level
        # Update difficulty label in side panel
        difficulty_text = level.upper()
        self.diff_label.config(text=difficulty_text)
        self.start_quiz()
    
    def randomInt(self):
        """Generate random numbers based on difficulty level"""
        if self.difficulty == "easy":
            return random.randint(0, 9), random.randint(0, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99), random.randint(10, 99)
        else:  # advanced
            return random.randint(1000, 9999), random.randint(1000, 9999)
    
    def decideOperation(self):
        """Randomly decide whether it's addition or subtraction"""
        return '+' if random.choice([True, False]) else '-'
    
    def displayProblem(self):
        """Display the current arithmetic problem"""
        self.num1, self.num2 = self.randomInt()
        self.operation = self.decideOperation()
        
        # Ensure subtraction doesn't give negative results
        if self.operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1
        
        # Calculate correct answer
        if self.operation == '+':
            self.correct_answer = self.num1 + self.num2
        else:
            self.correct_answer = self.num1 - self.num2
        
        # Update display
        self.question_label.config(text=f"{self.num1} {self.operation} {self.num2} = ?")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        
        # Update side panel
        self.progress_label.config(text=f"{self.current_question + 1}/{self.total_questions}")
        self.score_label.config(text=f"{self.score}")
        
        self.current_attempt = 1
        self.feedback_label.config(text="")
    
    def isCorrect(self, user_answer):
        """Check if the user's answer is correct"""
        try:
            return int(user_answer) == self.correct_answer
        except ValueError:
            return False
    
    def check_answer(self):
        """Check the user's answer and provide feedback"""
        user_answer = self.answer_entry.get().strip()
        
        if not user_answer:
            messagebox.showwarning("Input Required", "Please enter an answer!")
            return
        
        if self.isCorrect(user_answer):
            points = 10 if self.current_attempt == 1 else 5
            self.score += points
            self.flash_screen('#4ade80')  # Green flash for correct
            self.feedback_label.config(text=f"Correct! +{points} points", fg='#4ade80')
            self.root.after(1000, self.next_question)  # Wait 1 second before next question
        else:
            if self.current_attempt == 1:
                self.current_attempt = 2
                self.flash_screen('#e94560')  # Red flash for incorrect
                self.feedback_label.config(text="Try again!", fg='#e94560')
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
            else:
                self.flash_screen('#e94560')  # Red flash for incorrect
                self.feedback_label.config(text=f"Correct answer: {self.correct_answer}", fg='#e94560')
                self.root.after(1500, self.next_question)  # Wait 1.5 seconds before next question
        
        # Update score in side panel
        self.score_label.config(text=f"{self.score}")
    
    def next_question(self):
        """Move to the next question or end quiz"""
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.displayProblem()
        else:
            self.end_quiz()
    
    def start_quiz(self):
        """Start the quiz with selected difficulty"""
        self.score = 0
        self.current_question = 0
        self.hide_all_frames()
        self.quiz_frame.pack(expand=True, fill='both')
        self.displayProblem()
    
    def end_quiz(self):
        """End the quiz and show results"""
        self.hide_all_frames()
        self.results_frame.pack(expand=True, fill='both')
        
        # Calculate percentage
        percentage = (self.score / 100) * 100
        
        # Display results
        self.results_label.config(text=f"FINAL SCORE: {self.score}/100")
        
        # Determine rank
        rank = self.determine_rank(percentage)
        self.rank_label.config(text=f"RANK: {rank}")
        
        # Update side panel with final score
        self.score_label.config(text=f"{self.score}")
        self.progress_label.config(text="COMPLETED!")
        
        # Show congratulatory message
        if percentage >= 80:
            messagebox.showinfo("Congratulations!", f"Excellent work! You earned a {rank}")
        elif percentage >= 60:
            messagebox.showinfo("Good Job!", f"Well done! You earned a {rank}")
        else:
            messagebox.showinfo("Quiz Complete", f"Keep practicing! You earned a {rank}")
    
    def determine_rank(self, percentage):
        """Determine the rank based on percentage score"""
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B"
        elif percentage >= 60:
            return "C"
        elif percentage >= 50:
            return "D"
        else:
            return "F"
    
    def displayResults(self):
        """Display final results"""
        pass
    
    def restart_quiz(self):
        """Restart the quiz by showing difficulty menu again"""
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.diff_label.config(text="-")
        self.progress_label.config(text="0/10")
        self.score_label.config(text="0")
        self.show_difficulty_menu()

def main():
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()

if __name__ == "__main__":
    main()