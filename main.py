from tkinter import *
import pandas as pd
from random import randint

BG_COLOR = "#B1DDC6"
TITLE = ("courier", 30, "italic")

to_learn = {}

try:
    data = pd.read_csv("./data/to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


window = Tk()
window.title("Flash cards")
window.config(padx=150, pady=50, bg=BG_COLOR)

word_pair = {}


### ---------- FUNCTIONS ----------  ###

def next_card():
    global word_pair, flip_timer
    window.after_cancel(flip_timer)
    word_pair = to_learn[randint(0,len(to_learn) - 1)]
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=word_pair["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)

def is_known():
    global to_learn, word_pair
    to_learn.remove(word_pair)
    data = pd.DataFrame(to_learn)
    data.to_csv('data/to_learn.csv', index=False)
    next_card()


def flip_card():
    global word_pair
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=word_pair["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back)


flip_timer = window.after(3000, func=flip_card)

### ---------- ELEMENTS ----------  ###
# Card
canvas = Canvas(width=800, height=626, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BG_COLOR)
canvas.grid(column=0, row=0, columnspan=2)

# Text
title = canvas.create_text(400, 175, text="", fill="black", font=TITLE)
word = canvas.create_text(400, 263, text="", fill="black", font=("ariel", 40, "bold"))

next_card()

# Buttons
unknown = PhotoImage(file="./images/wrong.png")
button_unknown = Button(image=unknown, highlightthickness=0, command=next_card)
button_unknown.grid(row=2, column=0)

right = PhotoImage(file="./images/right.png")
button_right = Button(image=right,  highlightthickness=0, command=is_known)
button_right.grid(row=2, column=1)



window.mainloop()