from tkinter import *
from tkinter import messagebox
import pandas
from random import choice
BACKGROUND_COLOR = "#B1DDC6"
chosen_word = {}

try:
    data_frame = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data_frame = pandas.read_csv("data/german.csv")
words_list = data_frame.to_dict(orient="records")


# ------------------------------ UPDATE -------------------------------------
def update():
    words_list.remove(chosen_word)
    new_data_frame = pandas.DataFrame(words_list)
    new_data_frame.to_csv("data/words_to_learn.csv", index=False)
    new_card()


# ------------------------------ FLIP CARD ----------------------------------
def flip_card():
    canvas.itemconfig(canvas_image, image=back_image)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=f"{chosen_word['English']}", fill="white")


# ------------------------------ NEW CARD -----------------------------------
def new_card():
    global chosen_word, flip_timer
    window.after_cancel(flip_timer)
    if words_list:
        chosen_word = choice(words_list)
        canvas.itemconfig(title, text="German", fill="black")
        canvas.itemconfig(word, text=f"{chosen_word['German']}", fill="black")
        canvas.itemconfig(canvas_image, image=front_image)
        flip_timer = window.after(3000, flip_card)
    else:
        messagebox.showinfo("Yaaaay!", "Great!! You've learnt all of the words in the app.")


# ------------------------------ SETUP UI -----------------------------------
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

back_image = PhotoImage(file="images/card_back.png")
front_image = PhotoImage(file="images/card_front.png")
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=front_image)
title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
btn_wrong = Button(image=wrong_image, highlightthickness=0, bd=0, command=new_card)
btn_wrong.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
btn_right = Button(image=right_image, highlightthickness=0, bd=0, command=update)
btn_right.grid(row=1, column=1)

new_card()

window.mainloop()
