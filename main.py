import tkinter as tk
from tkinter import filedialog
from textblob import TextBlob
import re
import random
import plyer

# Patterns for different programming languages
python_patterns = [r'\bprint\b', r'\bdef\b', r'\bclass\b', r'\bif\b', r'\bwith\b', r'\bimport\b', r'\bin\b', r'\bfrom\b', r'\bas\b', r'\bglobal\b', r'\bnonlocal\b', r'\bassert\b', r'\byield\b', r'\btry\b', r'\bexcept\b', r'\bfinally\b', r'\braise\b', r'\bcontinue\b', r'\bbreak\b', r'\bpass\b', r'\bwhile\b', r'\blambda\b', r'\band\b', r'\bor\b', r'\bnot\b', r'\bis\b', r'\bin\b', r'\bNone\b', r'\bself\b']
c_patterns = [r'\b#include\b',r'\b#define\b', r'\btypedef\b', r'\benum\b', r'\bif\b', r'{|}', r';', r'\belse\b', r'\bdo\b', r'\bbreak\b', r'\bgoto\b', r'\bswitch\b', r'\bcase\b', r'\bdefault\b', r'\bsizeof\b', r'\bauto\b', r'\bregister\b', r'\bstatic\b', r'\bextern\b', r'\bconst\b', r'\bvolatile\b', r'\bchar\b', r'\blong\b', r'\bfloat\b', r'\bdouble\b', r'\bsigned\b', r'\bunsigned\b', r'\bbool\b']
arduino_patterns = [r'\bvoid setup\b', r'\bvoid loop\b', r'\bpinMode\b', r'\bdigitalWrite\b', r'\bdigitalRead\b', r'\banalogRead\b', r'\banalogWrite\b', r'\bSerial.begin\b', r'\bSerial.print\b', r'\bSerial.println\b', r'\bdelay\b', r'\bdelayMicroseconds\b', r'\battachInterrupt\b', r'\bdetachInterrupt\b', r'\bmillis\b', r'\bmicros\b', r'\bLOW\b', r'\bHIGH\b', r'\bINPUT\b', r'\bOUTPUT\b', r'\bINPUT_PULLUP\b', r'\bLED_BUILTIN\b']
cpp_patterns = [r'\busing namespace std\b', r'\bcout\b', r'\bcin\b', r'\bendl\b', r'\bdo\b', r'\bbreak\b', r'\bgoto\b', r'\bswitch\b', r'\bcase\b', r'\bdefault\b', r'\bsizeof\b', r'\bstatic\b']

#sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def edit_based_on_sentiment(text):
    polarity = analyze_sentiment(text)
    if polarity > 0:
        notify("Sentiment:", "Seems Positive!")
    elif polarity < 0:
        notify("Sentiment:", "Seems Negative, what are you writing?!")
    else:
        notify("Sentiment:", "Neutral huh, you're a robot!")
    return text

def open_file():
    # Open file dialog to select the file
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"), 
                                                      ("Python Files", "*.py"),
                                                      ("C files", "*.c"),
                                                      ("Arduino files", "*.ino"), 
                                                      ("C++ files", "*.cpp")])

#Detecting the programming language
def detect_code(text, patterns):
    return any(re.search(pattern, text) for pattern in patterns)

def notify(title: str, message: str):
    plyer.notification.notify(
        app_name= "Analysis for your text",
        title=title,
        message=message,
        timeout=8,    
    )


def open_file(event=None):
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"), 
                                                      ("Python Files", "*.py"),
                                                      ("C files", "*.c"),
                                                      ("Arduino files", "*.ino"), 
                                                      ("C++ files", "*.cpp")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                
            text_area.delete(1.0, tk.END)  # Clear the text area
            text_area.insert(tk.END, content)  # Load the file content into the text area

            if detect_code(content, python_patterns):
                notify("Python Code Detected", "Loaded a Python file")
            elif detect_code(content, c_patterns):
                notify("C Code Detected", "Loaded a C file")
            elif detect_code(content, arduino_patterns):
                notify("Arduino Code Detected", "Loaded an Arduino file")
            elif detect_code(content, cpp_patterns):
                notify("C++ Code Detected", "Loaded a C++ file")
            else:
                edited_text = edit_based_on_sentiment(content)
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, edited_text)
        except Exception as e:
            notify("Error", f"Failed to open file: {str(e)}")
            update_word_count()

def save_file(event=None):
    text = text_area.get("1.0", tk.END).strip()

    if detect_code(text, python_patterns):
        notify("Python Code Detected", "Your code is going to be saved as a Python file")
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
    elif detect_code(text, c_patterns):
        notify("C Code Detected", "Your code is going to be saved as a C file")
        file_path = filedialog.asksaveasfilename(defaultextension=".c", filetypes=[("C files", "*.c")])
    elif detect_code(text, arduino_patterns):
        notify("Arduino Code Detected", "Your code is going to be saved as an ino file")
        file_path = filedialog.asksaveasfilename(defaultextension=".ino", filetypes=[("Arduino files", "*.ino")])
    elif detect_code(text, cpp_patterns):
        notify("C++ Code Detected", "Your code is going to be saved as a C++ file")
        file_path = filedialog.asksaveasfilename(defaultextension=".cpp", filetypes=[("C++ files", "*.cpp")])
    else:
        edited_text = edit_based_on_sentiment(text)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        text = edited_text

    if file_path:
        with open(file_path, "w") as new_file:
            new_file.write(text)
        print(f"File saved in {file_path}.")

#Change Theme of the editor
def toggle_dark_mode():
    current_bg = text_area.cget("background")
    if current_bg == "white":
        text_area.config(background="black", foreground="white", insertbackground="white")
        root.config(bg="black")
        menu.config(bg="black", fg="white")
        status_bar.config(bg="black", fg="white")
    else:
        text_area.config(background="white", foreground="black", insertbackground="black")
        root.config(bg="white")
        menu.config(bg="white", fg="black")
        status_bar.config(bg="white", fg="black")

#count the number of words in the text
def update_word_count(event=None):
    text = text_area.get("1.0", tk.END).strip()
    word_count = len(text.split())
    status_bar.config(text=f"Words: {word_count}")

# click me game
def start_game():
    game_window = tk.Toplevel(root)
    game_window.title("Click the Target")
    game_window.geometry("400x400")

    target = tk.Button(game_window, text="Click Me!", bg="red", fg="white", command=lambda: on_target_click(game_window))
    target.place(x=random.randint(0, 350), y=random.randint(0, 350))

    def move_target():
        target.place(x=random.randint(0, 350), y=random.randint(0, 350))
        game_window.after(1000, move_target)

    move_target()

def on_target_click(game_window):
    global clicks
    clicks += 1
    if clicks >= 5: # 5 click is required to save the file
        game_window.destroy()
        save_file() 

def save_with_game(event=None):
    global clicks
    clicks = 0
    start_game()  
    for i in range(10):  # Add 10 random texts
        random_texts = ["Huh?", "Done?", "Saved!", "seems legit!", "Good Job!", "Congo!", "Bro cooked.", "The World Shall Know Pain.", "Peace was never an option.", "Giving up is not an option."]
        colors = ["red", "green", "blue", "yellow", "purple", "orange", "magenta", "brown"]
        random_word = random.choice(random_texts)
        random_color = random.choice(colors)
        random_position = f"{random.randint(1, 20)}.{random.randint(0, 40)}"
        text_area.insert(random_position, random_word)
        text_area.tag_add(f"color{random_position}", random_position, f"{random_position} + {len(random_word)}c")
        text_area.tag_config(f"color{random_position}", foreground=random_color)

def close_editor(event=None):
    root.destroy()

root = tk.Tk()
root.title("Functionally Dysfunctional Text Editor")

text_area = tk.Text(root, wrap="word", background="white", foreground="black", insertbackground="black")
text_area.pack(expand=True, fill='both')
text_area.bind("<KeyRelease>", update_word_count)

menu = tk.Menu(root)
root.config(menu=menu, bg="white")

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_with_game)

root.bind('<Control-s>', save_with_game)
root.bind('<Control-o>', open_file)
root.bind('<Control-q>', close_editor)

view_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)

status_bar = tk.Label(root, text="Words: 0", anchor="e")
status_bar.pack(fill="x", side="bottom")
clicks = 0
root.mainloop()
