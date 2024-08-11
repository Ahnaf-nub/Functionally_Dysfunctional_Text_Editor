import tkinter as tk
from tkinter import filedialog
from textblob import TextBlob
import re

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def edit_based_on_sentiment(text):
    polarity = analyze_sentiment(text)
    if polarity > 0:
        return f"Positive: {text}"
    elif polarity < 0:
        return f"Negative: {text}"
    else:
        return text

def detect_code(text):
    code_patterns_python = [r'\bprint\b', r'\bdef\b', r'\bclass\b', r'\bif\b', r'{|}', r';', r'\bwith\b', r'\bimport\b', r'\bin\b', r'\breturn\b', r'\bfrom\b', r'\bas\b', r'\bglobal\b', r'\bnonlocal\b', r'\bassert\b', r'\byield\b', r'\btry\b', r'\bexcept\b', r'\bfinally\b', r'\braise\b', r'\bcontinue\b', r'\bbreak\b', r'\bpass\b', r'\bwhile\b', r'\blambda\b', r'\band\b', r'\bor\b', r'\bnot\b', r'\bis\b', r'\bin\b', r'\bNone\b', r'\bTrue\b', r'\bFalse\b', r'\bself\b']
    code_patterns_c = [r'\b#include\b', r'\b#define\b', r'\btypedef\b', r'\bstruct\b', r'\bunion\b', r'\benum\b', r'\bif\b', r'{|}', r';', r'\belse\b', r'\bwhile\b', r'\bdo\b', r'\breturn\b', r'\bcontinue\b', r'\bbreak\b', r'\bgoto\b', r'\bswitch\b', r'\bcase\b', r'\bdefault\b', r'\bsizeof\b', r'\bauto\b', r'\bregister\b', r'\bstatic\b', r'\bextern\b', r'\bconst\b', r'\bvolatile\b', r'\bchar\b', r'\blong\b', r'\bfloat\b', r'\bdouble\b', r'\bsigned\b', r'\bunsigned\b', r'\bbool\b', r'\btrue\b', r'\bfalse\b']
    code_patterns_arduino = [r'\bvoid setup\b', r'\bvoid bloop\b', r'\bpinMode\b', r'\bdigitalWrite\b', r'\bdigitalRead\b', r'\banalogRead\b', r'\banalogWrite\b', r'\bSerial.begin\b', r'\bSerial.print\b', r'\bSerial.println\b', r'\bdelay\b', r'\bdelayMicroseconds\b', r'\battachInterrupt\b', r'\bdetachInterrupt\b', r'\bmillis\b', r'\bmicros\b', r'\bLOW\b', r'\bHIGH\b', r'\bINPUT\b', r'\bOUTPUT\b', r'\bINPUT_PULLUP\b', r'\bLED_BUILTIN\b', r'\btrue\b', r'\bfalse\b']
    return any(re.search(pattern, text) for pattern in code_patterns_python and code_patterns_c and code_patterns_arduino)

def save_file():
    text = text_area.get("1.0", tk.END).strip()
    
    if detect_code(text):
        # Save as Python file
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
        if file_path:
            with open(file_path, "w") as new_file:
                new_file.write(text)
            print(f"Code detected and saved in {file_path}.")
    else:
        edited_text = edit_based_on_sentiment(text)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(edited_text)
            print(f"Text saved in {file_path}.")

root = tk.Tk()
root.title("Functionally Dysfunctional Text Editor")

text_area = tk.Text(root, wrap="word")
text_area.pack(expand=True, fill='both')

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=save_file)

root.mainloop()
