import tkinter as tk
from tkinter import ttk
from SizedButton import SizedButton

NUM_COLS = 10
NUM_ROWS = 5

KEY_LEN = 60

NAME_MAX_LEN = 20

out_str = ''
letter_buttons = []
shift_on = True
keys = '1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
usr_done = False


def get_usr_inp(prompt):
    global out_str, letter_buttons, keys, usr_done, shift_on
    shift_on = True
    out_str = ''
    letter_buttons = []
    keys = '1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
    usr_done = False

    kb = tk.Tk()
    kb.geometry('720x360')
    kb.grid_propagate(False)

    curr_text = ttk.Label(kb, text=prompt + ":")
    curr_text.grid(row=0, column=0, columnspan=10)

    def shift_toggle():
        global letter_buttons, shift_on

        shift_on = not shift_on
        for letter_btn in letter_buttons:
            if shift_on:
                new_char: str = letter_btn.get_text().upper()
            else:
                new_char: str = letter_btn.get_text().lower()

            def shift_char(x=new_char):
                global out_str
                if len(out_str) <= NAME_MAX_LEN:
                    out_str += x
                    curr_text.config(text=prompt + ": " + out_str)

                if shift_on and not x.isnumeric():
                    shift_toggle()

            letter_btn.set_text(new_char)
            letter_btn.set_cmd(shift_char)

    for char in keys:

        def add_char(x=char):
            global out_str
            if len(out_str) <= NAME_MAX_LEN:
                out_str += x
                curr_text.config(text=prompt + ": " + out_str)

            if shift_on and not x.isnumeric():
                shift_toggle()

        letter_buttons.append(SizedButton(kb,
                                          height=KEY_LEN,
                                          width=KEY_LEN,
                                          text=char,
                                          command=add_char))

    for i, btn in enumerate(letter_buttons[0:10]):
        btn.grid(row=1, column=i)

    for i, btn in enumerate(letter_buttons[10:20]):
        btn.grid(row=2, column=i)

    for i, btn in enumerate(letter_buttons[20:29]):
        btn.grid(row=3, column=i)

    def delete_char():
        global out_str
        if len(out_str) > 0:
            out_str = out_str[0:len(out_str)-1]
            curr_text.config(text=prompt + ": " + out_str)

    SizedButton(kb,
                height=KEY_LEN,
                width=KEY_LEN,
                text='<-',
                command=delete_char).grid(row=3, column=9)

    for i, btn in enumerate(letter_buttons[29:37]):
        btn.grid(row=4, column=i)

    def press_enter():
        global usr_done
        usr_done = True

    SizedButton(kb,
                height=KEY_LEN,
                width=KEY_LEN*2,
                text='Enter',
                command=press_enter).grid(row=4, column=7, columnspan=2)

    def add_space():
        global out_str
        if len(out_str) <= NAME_MAX_LEN:
            out_str += ' '
            curr_text.config(text=out_str)

    SizedButton(kb,
                height=KEY_LEN,
                width=KEY_LEN * 2,
                text='Space',
                command=add_space).grid(row=5, column=2, columnspan=5)

    SizedButton(kb,
                height=KEY_LEN,
                width=KEY_LEN * 2,
                text='Shift',
                command=shift_toggle).grid(row=5, column=7, columnspan=2)

    while not usr_done:
        kb.update_idletasks()
        kb.update()
    kb.destroy()
    return out_str


def get_num_inp(prompt, type_int=False):
    global out_str, keys, usr_done
    out_str = ''
    keys = '123456789.0'
    usr_done = False

    kb = tk.Tk()
    kb.geometry('180x360')
    kb.grid_propagate(False)

    curr_text = ttk.Label(kb, text=prompt + ":")
    curr_text.grid(row=0, column=0, columnspan=10)

    for i in range(len(keys)):
        if type_int and keys[i] == '.':
            continue

        def add_char(x=keys[i]):
            global out_str
            out_str = out_str + x
            curr_text.config(text=prompt + ": " + out_str)

        SizedButton(kb,
                    height=KEY_LEN,
                    width=KEY_LEN,
                    text=keys[i],
                    command=add_char).grid(row=int(i/3)+1, column=i % 3)

    def del_char():
        global out_str
        if len(out_str) > 0:
            out_str = out_str[0:len(out_str) - 1]
            curr_text.config(text=prompt + ": " + out_str)

    SizedButton(kb,
                height=KEY_LEN,
                width=KEY_LEN,
                text='<-',
                command=del_char).grid(row=4, column=2)

    def press_enter():
        global usr_done
        usr_done = True

    SizedButton(kb,
                height=KEY_LEN,
                width=KEY_LEN*3,
                text='Enter',
                command=press_enter).grid(row=5, column=0, columnspan=3)

    while not usr_done:
        kb.update_idletasks()
        kb.update()
    kb.destroy()

    if type_int:
        return int(out_str)
    else:
        return float(out_str)






