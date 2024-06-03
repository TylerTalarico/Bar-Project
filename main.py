import serial

import tkinter as tk
from tkinter import ttk
from HorizontalScrolledFrame import HorizontalScrolledFrame
from SizedButton import SizedButton

from Bar import Bar
from Drink import Drink, IngredientType

from Keyboard import get_usr_inp, get_num_inp

NUM_GRID_ROWS = 4
NUM_GRID_COLS = 4
BLOCK_WIDTH = int(1024/NUM_GRID_COLS)
BLOCK_HEIGHT = int(600/NUM_GRID_ROWS)

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings

# Bar object
bar = Bar()

# List of drinks
drink_list = [
    Drink("Rum and Coke", [("Rum", 1.5, IngredientType.LIQUOR), ("Coke", 8, IngredientType.MIXER)]),
    Drink("Gin and Tonic", [("Gin", 1.5, IngredientType.LIQUOR), ("Seltzer", 8, IngredientType.MIXER)]),
    Drink("Dirty Shirley", [("Vodka", 2, IngredientType.LIQUOR),
                            ("Grenadine", 1, IngredientType.MIXER), ("Sprite", 8, IngredientType.MIXER)])
]
num_drinks = 3
selected_drink: Drink

ser = serial.Serial("/dev/ttyS0", 9600)    #Open port with baud rate

# Main window
root = tk.Tk()
root.geometry("1024x600")

# Style configuration
style = ttk.Style()
style.configure("Mix.TButton", background='green', foreground='green', font='Calibri 14')
style.configure("Normal.TButton", font='Calibri 14')


def select_drink(desired_drink: Drink):
    global selected_drink_label, selected_drink
    selected_drink = desired_drink
    selected_drink_label.config(text=desired_drink.to_string())


s = ttk.Style()
s.configure('Scroll.TButton', font='Calibri 14')

scroll_frame = HorizontalScrolledFrame(root, bg="white", width=BLOCK_WIDTH*2)
scroll_frame.grid(row=0, column=1, columnspan=2, pady=30)


for index, drink in enumerate(drink_list):
    def func(x=drink):
        return select_drink(x)
    SizedButton(scroll_frame.interior,
                width=BLOCK_WIDTH-50,
                height=BLOCK_HEIGHT-20,
                text=drink.get_name(),
                command=func,
                style='Scroll.TButton').grid(row=0, column=index, sticky='ns')


# Edit Bar Logic
def edit_bar():
    global bar
    bar_window = tk.Tk()
    bar_window.geometry('1024x600')
    liquor_btns: list[SizedButton] = []
    mixer_btns: list[SizedButton] = []
    btn_height = 100
    btn_width = 150
    for i in range(6):
        def set_liquor(x=i):
            liquor_name = get_usr_inp("Liquor name")
            bar.set_liquor(x, liquor_name)
            liquor_btns[x].set_text("Dispenser " + str(x+1) + ":\n" + bar.get_liquor(x))

        liquor_btns.append(SizedButton(bar_window,
                           height=btn_height,
                           width=btn_width,
                           text="Dispenser " + str(i+1) + ":\n" + bar.get_liquor(i),
                           command=set_liquor))
        liquor_btns[i].grid(row=0, column=i)

    for i in range(4):
        def set_mixer(x=i):
            mixer_name = get_usr_inp("Mixer name")
            bar.set_mixer(x, mixer_name)
            mixer_btns[x].set_text("Mixer " + str(x+1) + ":\n" + bar.get_mixer(x))

        mixer_btns.append(SizedButton(bar_window,
                                      height=btn_height,
                                      width=btn_width,
                                      text="Mixer " + str(i + 1) + ":\n" + bar.get_mixer(i),
                                      command=set_mixer))
        mixer_btns[i].grid(row=1, column=i)

    def edit_done():
        bar_window.destroy()

    done_btn = SizedButton(bar_window,
                           height=btn_height,
                           width=btn_width,
                           text="Done",
                           command=edit_done,
                           style='Mix.TButton')
    done_btn.grid(row=2, column=0)

    bar_window.mainloop()


edit_bar_btn = SizedButton(root, text="Edit Bar 🔧", style='Normal.TButton',
                           width=BLOCK_WIDTH, height=BLOCK_HEIGHT,
                           command=edit_bar)
edit_bar_btn.grid(row=1, column=0)


# New Drink Logic
def new_drink():
    global bar, drink_list, scroll_frame, num_drinks
    drink_name = get_usr_inp("Drink name")
    bar_window = tk.Tk()
    bar_window.geometry('1024x600')
    liquor_btns: list[SizedButton] = []
    mixer_btns: list[SizedButton] = []
    ingredients = []
    btn_height = 100
    btn_width = 150
    for i in range(6):
        if bar.get_liquor(i) == "":
            continue

        def add_liquor(x=i):
            amt = get_num_inp("Number of shots", type_int=True)
            volume = 0
            for m in range(len(ingredients)):
                if ingredients[m][2] is IngredientType.LIQUOR:
                    volume += ingredients[m][1]*1.7
                else:
                    volume += ingredients[m][1]
            if 0 < volume + amt*1.7 <= 15.0:
                ingredients.append((bar.get_liquor(x), amt, IngredientType.LIQUOR))
            else:
                print("Too much stuff: volume exceeds cup limits")

        liquor_btns.append(SizedButton(bar_window,
                                       height=btn_height,
                                       width=btn_width,
                                       text="Dispenser " + str(i + 1) + ":\n" + bar.get_liquor(i),
                                       command=add_liquor))
        liquor_btns[-1].grid(row=0, column=i)

    for i in range(4):
        if bar.get_mixer(i) == "":
            continue

        def add_mixer(x=i):
            amt = get_num_inp("Amount in oz")
            volume = 0
            for m in range(len(ingredients)):
                if ingredients[m][2] is IngredientType.LIQUOR:
                    volume += ingredients[m][1] * 1.7
                else:
                    volume += ingredients[m][1]
            if 0 < volume + amt <= 15.0:
                ingredients.append((bar.get_mixer(x), amt, IngredientType.MIXER))
            else:
                print("Too much stuff: volume exceeds cup limits")

        mixer_btns.append(SizedButton(bar_window,
                                      height=btn_height,
                                      width=btn_width,
                                      text="Mixer " + str(i + 1) + ":\n" + bar.get_mixer(i),
                                      command=add_mixer))
        mixer_btns[-1].grid(row=1, column=i)

    def drink_done(name=drink_name):
        global num_drinks
        created_drink = Drink(name, ingredients)
        drink_list.append(created_drink)

        def sel_drink(x=created_drink):
            return select_drink(x)

        SizedButton(scroll_frame.interior,
                    width=BLOCK_WIDTH - 50,
                    height=BLOCK_HEIGHT - 20,
                    text=name,
                    command=sel_drink,
                    style='Scroll.TButton').grid(row=0, column=num_drinks, sticky='ns')
        num_drinks += 1
        bar_window.destroy()

    done_btn = SizedButton(bar_window,
                           height=btn_height,
                           width=btn_width,
                           text="Done",
                           command=drink_done,
                           style='Mix.TButton')
    done_btn.grid(row=2, column=0)
    bar_window.mainloop()


new_drink_btn = SizedButton(root, text="New Drink 🍹", style='Normal.TButton', width=BLOCK_WIDTH, height=BLOCK_HEIGHT,
                            command=new_drink)
new_drink_btn.grid(row=0, column=0)


selected_drink_label_frame = ttk.Frame(root, width=BLOCK_WIDTH, height=BLOCK_HEIGHT)
selected_drink_label = ttk.Label(selected_drink_label_frame, text="Select a Drink!")
selected_drink_label_frame.grid(row=1, column=1, columnspan=2)
selected_drink_label_frame.pack_propagate(False)
selected_drink_label.pack()


def mix_drink():
    global selected_drink
    if selected_drink is None:
        return None
    
    command = []

    for gred in selected_drink.get_ingredients():
        if gred[2] == IngredientType.LIQUOR:
            try:
                idx = bar.liquors.index(gred[0])
                command.append(108)
                command.append(idx)
                command.append(int(gred[1]))
            except IndexError:
                print(gred[0], ' could not be found')

        elif gred[2] == IngredientType.MIXER:
            try:
                idx = bar.mixers.index(gred[0])
                command.append(109)
                command.append(idx)
                command += list(int(gred[1]*1000).to_bytes(4))
            except IndexError:
                print(gred[0], ' could not be found')

    command.append(4)
    #print(bytearray(command))
    ser.write(bytearray(command))

    

mix_btn = SizedButton(root, text="Mix!", style="Mix.TButton", width=BLOCK_WIDTH, height=BLOCK_HEIGHT, command=mix_drink)
mix_btn.grid(row=0, column=3)


# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
