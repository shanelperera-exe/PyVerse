from tkinter import *
import random
from tkinter import messagebox
from tkinter import PhotoImage

FONT_NAME = "Monospace"
TIME_LIMIT = 60

time_left = TIME_LIMIT
started = False
characters_typed = 0
total_words = 0
correct_characters = 0

def load_words_from_file():
    try:
        with open("assets/word_list.txt", "r") as file:
            words = [line.strip() for line in file if line.strip()]
        return words
    except FileNotFoundError:
        messagebox.showerror("Error", "word_list.txt not found!")
        return []

word_list = load_words_from_file()

if not word_list:
    word_list = [
        "apple", "banana", "cherry", "dog", "elephant", "flower", "guitar", "house", "island", "jungle",
        "kite", "lemon", "mountain", "notebook", "ocean", "pencil", "queen", "rainbow", "sunshine", "tiger",
        "umbrella", "violin", "waterfall", "xylophone", "yogurt", "zebra", "adventure", "butterfly", "chocolate", "dolphin"
    ]

words_to_display = []

def load_initial_words():
    global words_to_display
    words_to_display = [("      ", "white")] * 3
    middle_word = random.choice(word_list)
    words_to_display.append((middle_word, "blue"))
    words_to_display.extend([(random.choice(word_list), "gray") for _ in range(3)])

def load_new_word():
    new_word = random.choice(word_list)
    words_to_display.append((new_word, "gray"))
    update_display()
    typing_entry.delete(0, END)

def update_display():
    text_display.config(state=NORMAL)
    text_display.delete("1.0", END)
    
    for i, (word, color) in enumerate(words_to_display[-7:]):
        if i == 3:
            color = "blue"
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
        expected_word, _ = words_to_display[3]
        
        if typed_text == expected_word:
            words_to_display[3] = (expected_word, "black")
            total_words += 1
            correct_characters += len(typed_text)
        else:
            words_to_display[3] = (expected_word, "red")
        
        characters_typed += len(typed_text)
        
        words_to_display.pop(0)
        load_new_word()
    
    update_display()
    update_stats()

def update_stats():
    elapsed_time = TIME_LIMIT - time_left
    
    if elapsed_time > 0:
        wpm = (total_words / elapsed_time) * 60
        cpm = (characters_typed / elapsed_time) * 60
    else:
        wpm = 0
        cpm = 0
    
    accuracy = (correct_characters / characters_typed * 100) if characters_typed > 0 else 0
    
    wpm_label.config(text=f"WPM: {int(wpm)}")
    cpm_label.config(text=f"CPM: {int(cpm)}")
    accuracy_label.config(text=f"Accuracy: {int(accuracy)}%")

def calculate_results():
    update_stats()
    speed_msg = "Fast!" if int(wpm_label.cget("text").split()[1]) > 40 else "Slow!"
    
    result_window = Toplevel(window)
    result_window.title("Typing Test Results")
    
    result_label = Label(result_window, text=f"{wpm_label.cget('text')}\n{cpm_label.cget('text')}\n{accuracy_label.cget('text')}\n{speed_msg}", font=(FONT_NAME, 15), padx=20, pady=20)
    result_label.pack()
    
    if speed_msg == "Slow!":
        animal_image = PhotoImage(file="assets/tortoise.png").subsample(3, 3)
    elif speed_msg == "Fast!":
        animal_image = PhotoImage(file="assets/cheetah.png").subsample(3, 3)

    animal_label = Label(result_window, image=animal_image)
    animal_label.image = animal_image
    animal_label.pack(pady=10, padx=10)

    close_button = Button(result_window, text="Close", font=(FONT_NAME, 12), command=result_window.destroy)
    close_button.pack(pady=10)

    result_window.mainloop()

def restart_test():
    global time_left, started, characters_typed, total_words, correct_characters, words_to_display
    
    time_left = TIME_LIMIT
    started = False
    characters_typed = 0
    total_words = 0
    correct_characters = 0
    words_to_display = []
    
    # Update UI
    timer_label.config(text=f"Time: {TIME_LIMIT}s")
    wpm_label.config(text=f"WPM: 0")
    cpm_label.config(text=f"CPM: 0")
    accuracy_label.config(text=f"Accuracy: 0%")
    
    load_initial_words()
    update_display()
    typing_entry.config(state=NORMAL)
    typing_entry.delete(0, END)
    typing_entry.focus_set()

def start_timer(event):
    global started
    if not started:
        started = True
        start_label.grid_remove()
        countdown()

window = Tk()
window.title("Typing Speed Test")
window.config(padx=25, pady=25, bg="skyblue")

title_label = Label(text="Typing Speed Test", font=(FONT_NAME, 25, "bold"), bg="skyblue")
title_label.grid(column=0, row=0, columnspan=4, sticky="nsew")

subtitle_label = Label(text="Test your typing skills", font=(FONT_NAME, 15), bg="skyblue")
subtitle_label.grid(column=0, row=1, columnspan=4, sticky="nsew")

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

typing_entry = Entry(
    window, 
    font=(FONT_NAME, 15), 
    width=20, 
    justify='center'
)
typing_entry.grid(column=0, row=4, columnspan=4, pady=20)
typing_entry.bind("<Key>", start_timer)
typing_entry.bind("<space>", check_typing)
typing_entry.focus_set()

start_label = Label(window, text="Start Typing!", font=(FONT_NAME, 12, "bold"), bg="skyblue", fg="black")
start_label.grid(column=0, row=5, columnspan=4)

restart_button = Button(
    window, 
    text="Restart", 
    font=(FONT_NAME, 12, "bold"), 
    command=restart_test,
    activebackground="pink",
    activeforeground="black",
    anchor="center",
    cursor="hand2",
    overrelief="raised",
    padx=10,
    pady=10,
    highlightthickness=0,
    bg="white"
)
restart_button.grid(column=0, row=6, columnspan=4, pady=10)

load_initial_words()
update_display()
window.mainloop()
