from tkinter import *
import pandas
import random

# ____________________________________________________CONSTANTS_______________________________________________________#
BACKGROUND_COLOR = "#B1DDC6"
WHITE = "#FFFFFF"
TEAL = "#008080"
FONT_LANGUAGE = ("Berlin Sans FB", 40, "italic")
FONT_WORD = ("Scrypta Personal Use Bold Italic", 90)
to_learn = {}
current_card = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/german_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ___________________________________________________ FLIP CARD _____________________________________________________#
def flip_card():
    canvas.itemconfig(card_title, text="English", fill=WHITE)
    canvas.itemconfig(card_word, text=current_card["ENGLISH"], fill=WHITE)
    canvas.itemconfig(card_background, image=card_back_img)


# ___________________________________________________ NEXT CARD _____________________________________________________#

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    new_word = current_card["GERMAN"]
    canvas.itemconfig(card_title, text="German", fill=TEAL)
    canvas.itemconfig(card_word, text=new_word, fill=TEAL)
    canvas.itemconfig(card_background, image=card_frt_img)
    flip_timer = window.after(3000, flip_card)


# __________________________________________________  IS KNOWN  _____________________________________________________#
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# _____________________________________________________  UI  ________________________________________________________#

# WINDOW:======>
window = Tk()
window.title("Inosuke")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

# CANVAS:======>
canvas = Canvas(width=800, height=526)
# image
card_frt_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_frt_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
# text
card_title = canvas.create_text(400, 100, text="Language", font=FONT_LANGUAGE, fill=TEAL)
card_word = canvas.create_text(400, 263, text="Word", font=FONT_WORD, fill=TEAL)
canvas.grid(row=0, column=0, columnspan=2)

# BUTTONS:======>
# 1
unknown_button = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=unknown_button, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)
# 2
known_button = PhotoImage(file="images/right.png")
right_button = Button(image=known_button, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

next_card()
window.mainloop()
