# Functionally Dysfunctional Text Editor

It is a quirky, sentiment-aware text editor that adds a fun twist to saving files. It analyzes the sentiment of your text, detects programming languages for code files, and even makes you play a mini-game before saving! The editor also supports dark mode, word counting, and random text insertions during saves. It is using tkinter for GUI, Plyer for sending push notifications, TextBlob for sentiment analysis. 

## Features

- **Sentiment Analysis**: Analyzes the sentiment of your text and gives feedback through push notifications.
- **Programming Language Detection**: Automatically detects and saves files with the correct extension. Currently supported languages are Python, C, Arduino, and C++.
- **Save file**: A mini-game where you have to click button for five times has to be completed before your file is saved. After saving it will show some random phrases that will be scattered around, though it will not save that texts into the file.
- **Dark Mode**: Toggle between light and dark modes.
- **Word Count**: Real-time word counting to keep track of your progress.

Demo video link: https://youtu.be/gJ0JbgBYe0E?si=V6cOa3JdvctoyrCK

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ahnaf-nub/Functionally_Dysfunctional_Text_Editor.git
   cd functionally-dysfunctional-text-editor
2. **Install the dependencies**
   ```
   pip install -r requirements.txt
3. **Run the main file**
   ```
   python main.py
