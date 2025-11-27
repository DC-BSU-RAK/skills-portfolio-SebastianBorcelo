import tkinter as tk
from tkinter import messagebox
import random
import pygame

class JokeTellingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Joke Teller")
        self.root.geometry("700x450")
        self.root.resizable(True, True)
        self.root.configure(bg='darkblue')
        
        pygame.mixer.init()
        
        # List of Jokes
        self.jokes = [
            "Why did the chicken cross the road?To get to the other side.",
            "What happens if you boil a clown?You get a laughing stock.",
            "Why did the car get a flat tire?Because there was a fork in the road!",
            "How did the hipster burn his mouth?He ate his pizza before it was cool.",
            "What did the janitor say when he jumped out of the closet?SUPPLIES!!!!",
            "Have you heard about the band 1023MB?It's probably because they haven't got a gig yet…",
            "Why does the golfer wear two pants?Because he's afraid he might get a Hole-in-one.",
            "Why should you wear glasses to maths class?Because it helps with division.",
            "Why does it take pirates so long to learn the alphabet?Because they could spend years at C.",
            "Why did the woman go on the date with the mushroom?Because he was a fun-ghi.",
            "Why do bananas never get lonely?Because they hang out in bunches.",
            "What did the buffalo say when his kid went to college?Bison.",
            "Why shouldn't you tell secrets in a cornfield?Too many ears.",
            "What do you call someone who doesn't like carbs?Lack-Toast Intolerant.",
            "Why did the can crusher quit his job?Because it was soda pressing.",
            "Why did the birthday boy wrap himself in paper?He wanted to live in the present.",
            "What does a house wear?A dress.",
            "Why couldn't the toilet paper cross the road?Because it got stuck in a crack.",
            "Why didn't the bike want to go anywhere?Because it was two-tired!",
            "Want to hear a pizza joke?Nahhh, it's too cheesy!",
            "Why are chemists great at solving problems?Because they have all of the solutions!",
            "Why is it impossible to starve in the desert?Because of all the sand which is there!",
            "What did the cheese say when it looked in the mirror?Halloumi!",
            "Why did the developer go broke?Because he used up all his cache.",
            "Did you know that ants are the only animals that don't get sick?It's true! It's because they have little antibodies.",
            "Why did the donut go to the dentist?To get a filling.",
            "What do you call a bear with no teeth?A gummy bear!",
            "What does a vegan zombie like to eat?Graaains.",
            "What do you call a dinosaur with only one eye?A Do-you-think-he-saw-us!",
            "Why should you never fall in love with a tennis player?Because to them... love means NOTHING!",
            "What did the full glass say to the empty glass?You look drunk.",
            "What's a potato's favorite form of transportation?The gravy train",
            "What did one ocean say to the other?Nothing, they just waved.",
            "What did the right eye say to the left eye?Honestly, between you and me something smells.",
            "What do you call a dog that's been run over by a steamroller?Spot!",
            "What's the difference between a hippo and a zippo?One's pretty heavy and the other's a little lighter",
            "Why don't scientists trust Atoms?They make up everything."
        ]
        
        self.current_joke = None
        self.jokes_used = []  
        
        # Create GUI elements
        self.create_widgets()
    
    def play_random_punchline_sound(self):
        """Play a random punchline sound from available audio files"""
        try:
            # List of available audio files
            audio_files = ['punchline1.mp3', 'punchline2.mp3', 'punchline3.mp3']
            
            # Randomly select one audio file
            selected_audio = random.choice(audio_files)
            audio_path = f"audio/{selected_audio}"
            
            # Load and play the sound
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
        except pygame.error as e:
            print(f"Audio error: {e}")
        except FileNotFoundError:
            print("Audio files not found. Please make sure the 'audio' folder exists with punchline1.mp3, punchline2.mp3, and punchline3.mp3")
    
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main title
        title_label = tk.Label(self.root, text="Alexa Joke Teller", 
                              font=("Impact", 24, "bold"), fg="cyan",
                              bg='darkblue')
        title_label.pack(pady=20)
        
        # Joke setup display
        self.setup_label = tk.Label(self.root, text="Click 'Tell me a Joke' to start!", 
                                   font=("Impact", 18), wraplength=600, justify="center",
                                   bg="white", relief="solid", padx=20, pady=20,
                                   fg="darkblue")
        self.setup_label.pack(pady=25, padx=40, fill="both")
        
        # Punchline display
        self.punchline_label = tk.Label(self.root, text="", 
                                       font=("Impact", 18, "italic"), 
                                       fg="purple", wraplength=600, justify="center",
                                       bg="lightyellow", relief="solid", padx=20, pady=20)
        self.punchline_label.pack(pady=20, padx=40, fill="both")
        
        # Create a frame for the bottom button section
        bottom_frame = tk.Frame(self.root, bg='darkblue')
        bottom_frame.pack(side='bottom', fill='x', pady=15)
        
        # Create 4 equal button boxes using grid
        button_frame = tk.Frame(bottom_frame, bg='darkblue')
        button_frame.pack(expand=True, fill='both', padx=25)
        
        # Configure equal column weights for 4 buttons
        for i in range(4):
            button_frame.columnconfigure(i, weight=1, uniform="equal")
        
        # Tell Joke button
        self.tell_joke_btn = tk.Button(button_frame, text="Alexa tell me a Joke", 
                                      font=("Impact", 16, "bold"), 
                                      bg="lightblue", fg="darkblue",
                                      command=self.tell_joke,
                                      height=3, relief='raised', bd=4)
        self.tell_joke_btn.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')
        
        # Show Punchline button
        self.punchline_btn = tk.Button(button_frame, text="Show Punchline", 
                                      font=("Impact", 16), 
                                      bg="lightgreen", fg="darkgreen",
                                      command=self.show_punchline,
                                      state="disabled", height=3, relief='raised', bd=4)
        self.punchline_btn.grid(row=0, column=1, padx=8, pady=8, sticky='nsew')
        
        # Next Joke button
        self.next_joke_btn = tk.Button(button_frame, text="Next Joke", 
                                      font=("Impact", 16), 
                                      bg="yellow", fg="darkorange",
                                      command=self.next_joke,
                                      state="disabled", height=3, relief='raised', bd=4)
        self.next_joke_btn.grid(row=0, column=2, padx=8, pady=8, sticky='nsew')
        
        # Quit button
        self.quit_btn = tk.Button(button_frame, text="Quit", 
                                 font=("Impact", 16), 
                                 bg="lightcoral", fg="darkred",
                                 command=self.root.quit,
                                 height=3, relief='raised', bd=4)
        self.quit_btn.grid(row=0, column=3, padx=8, pady=8, sticky='nsew')
    
    def tell_joke(self):
        """Select and display a random joke setup"""
        if not self.jokes:
            messagebox.showwarning("No Jokes", "No jokes available to tell!")
            return
        
        # If all jokes have been used, reset the used list
        if len(self.jokes_used) >= len(self.jokes):
            self.jokes_used = []
        
        # Select random joke that hasn't been used recently
        available_jokes = [joke for joke in self.jokes if joke not in self.jokes_used]
        if not available_jokes:
            available_jokes = self.jokes  # Fallback to all jokes
        
        self.current_joke = random.choice(available_jokes)
        self.jokes_used.append(self.current_joke)
        
        # Split joke into setup and punchline
        if '?' in self.current_joke:
            setup, punchline = self.current_joke.split('?', 1)
            self.current_setup = setup + "?"
            self.current_punchline = punchline
        else:
            # Fallback if no question mark is found
            self.current_setup = self.current_joke
            self.current_punchline = "No punchline available"
        
        # Update display
        self.setup_label.config(text=self.current_setup)
        self.punchline_label.config(text="")
        
        # Enable/disable buttons
        self.punchline_btn.config(state="normal")
        self.next_joke_btn.config(state="normal")
        self.tell_joke_btn.config(state="disabled")
    
    def show_punchline(self):
        """Display the punchline of the current joke and play random audio"""
        if hasattr(self, 'current_punchline'):
            self.punchline_label.config(text=self.current_punchline)
            self.punchline_btn.config(state="disabled")
            
            # Play random punchline sound
            self.play_random_punchline_sound()
    
    def next_joke(self):
        """Reset for the next joke"""
        self.punchline_label.config(text="")
        self.punchline_btn.config(state="disabled")
        self.next_joke_btn.config(state="disabled")
        self.tell_joke_btn.config(state="normal")
        self.setup_label.config(text="Click 'Tell me a Joke' for another joke!")

def main():
    root = tk.Tk()
    app = JokeTellingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()