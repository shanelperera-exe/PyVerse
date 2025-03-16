from tkinter import *
import random
from tkinter import messagebox

FONT_NAME = "Monospace"
TIME_LIMIT = 60

time_left = TIME_LIMIT
started = False
characters_typed = 0
total_words = 0
correct_characters = 0

word_list = [
    "apple", "banana", "cherry", "dog", "elephant", "flower", "guitar", "house", "island", "jungle",
    "kite", "lemon", "mountain", "notebook", "ocean", "pencil", "queen", "rainbow", "sunshine", "tiger",
    "umbrella", "violin", "waterfall", "xylophone", "yogurt", "zebra"
]

words_to_display = []  # Stores words for the train effect

def load_initial_words():
    global words_to_display
    words_to_display = [(random.choice(word_list), "gray") for _ in range(7)]  # Start with 7 words
    words_to_display[3] = (words_to_display[3][0], "blue")  # Make the middle word blue

def load_new_word():
    new_word = random.choice(word_list)
    words_to_display.append((new_word, "gray"))  # New words start gray
    update_display()
    typing_entry.delete(0, END)

def update_display():
    text_display.config(state=NORMAL)
    text_display.delete("1.0", END)
    
    for i, (word, color) in enumerate(words_to_display[-7:]):
        tag_name = f"tag_{i}"
        text_display.insert(END, word + " ", tag_name)
        text_display.tag_config(tag_name, foreground=color)
    
    text_display.config(state=DISABLED)

def countdown():
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time: {time_left}s")
        window.after(1000, countdown)
    else:
        typing_entry.config(state=DISABLED)
        calculate_results()

def check_typing(event):
    global started, characters_typed, correct_characters, total_words
    if not started:
        started = True
        countdown()
    
    typed_text = typing_entry.get().strip()
    
    if words_to_display:
        expected_word, _ = words_to_display[3]  # Always check the middle word
        
        if typed_text == expected_word:
            words_to_display[3] = (expected_word, "black")  # Correct turns black
            total_words += 1
            characters_typed += len(typed_text)
            correct_characters += len(typed_text)
        else:
            words_to_display[3] = (expected_word, "red")  # Incorrect turns red
        
        words_to_display.pop(0)  # Remove the first word
        load_new_word()
    
    update_display()
    update_stats()

def update_stats():
    wpm = (total_words / (TIME_LIMIT - time_left) * 60) if time_left > 0 else 0
    cpm = (characters_typed / (TIME_LIMIT - time_left) * 60) if time_left > 0 else 0
    accuracy = (correct_characters / characters_typed * 100) if characters_typed > 0 else 0
    
    wpm_label.config(text=f"WPM: {int(wpm)}")
    cpm_label.config(text=f"CPM: {int(cpm)}")
    accuracy_label.config(text=f"Accuracy: {int(accuracy)}%")

def calculate_results():
    update_stats()
    speed_msg = "Fast!" if int(wpm_label.cget("text").split()[1]) > 40 else "Slow!"
    messagebox.showinfo("Typing Test Results", f"{wpm_label.cget('text')}\n{cpm_label.cget('text')}\n{accuracy_label.cget('text')}\n{speed_msg}")

window = Tk()
window.title("Typing Speed Test")
window.config(padx=25, pady=25, bg="white")

title_label = Label(text="Typing Speed Test", font=(FONT_NAME, 25, "bold"), bg="white")
title_label.grid(column=1, row=0, columnspan=2)
subtitle_label = Label(text="Test your typing skills", font=(FONT_NAME, 15), bg="white")
subtitle_label.grid(column=1, row=1, columnspan=2)

timer_label = Label(text=f"Time: {TIME_LIMIT}s", font=(FONT_NAME, 15, "bold"), bg="white", fg="red")
timer_label.grid(column=0, row=2, pady=30, padx=20)
wpm_label = Label(text=f"WPM: 0", font=(FONT_NAME, 15, "bold"), bg="white", fg="navy blue")
wpm_label.grid(column=1, row=2, pady=30, padx=20)
cpm_label = Label(text=f"CPM: 0", font=(FONT_NAME, 15, "bold"), bg="white", fg="navy blue")
cpm_label.grid(column=2, row=2, pady=30, padx=20)
accuracy_label = Label(text=f"Accuracy: 0%", font=(FONT_NAME, 15, "bold"), bg="white", fg="green")
accuracy_label.grid(column=3, row=2, pady=30, padx=20)

text_display = Text(window, font=(FONT_NAME, 20), height=1, width=50, bg="white")
text_display.grid(column=0, row=3, columnspan=4, pady=20)
text_display.config(state=DISABLED)

typing_entry = Entry(window, font=(FONT_NAME, 15), width=20, justify='center')
typing_entry.grid(column=0, row=4, columnspan=4, pady=20)
typing_entry.bind("<Return>", check_typing)

load_initial_words()
update_display()
window.mainloop()