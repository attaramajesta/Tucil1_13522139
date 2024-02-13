import time
import random
import numpy as np
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import main

# Auto fill matrix (rand)
def fill_matrix_randomly():
    tokens = ['BD', '1C', '7A', '55', 'E9']
    for i in range(rows):
        for j in range(cols):
            token = np.random.choice(tokens)
            text_var[i][j].set(token)

# Auto fill sequences (rand)
def fill_sequences():
    num_sequences = 3
    max_sequence_size = 3
    tokens = ['BD', '1C', '7A', '55', 'E9']
    
    additional_input.delete("1.0", END)

    for _ in range(num_sequences):
        sequence = ' '.join(random.choices(tokens, k=max_sequence_size))
        reward = random.choice([10, 20, 30])
        additional_input.insert(END, f"{sequence}\n{reward}\n")

# Solve path
def solve_path():
    buffer_size = int(buffsize_choosen.get())
    matrix = np.array([[text_var[i][j].get() for j in range(cols)] for i in range(rows)])
    sequences_text = additional_input.get("1.0", END).strip().split("\n")
    sequences = []

    for i in range(0, len(sequences_text), 2):
        sequence = ''.join(sequences_text[i].split())
        reward = int(sequences_text[i+1])
        sequences.append((sequence, reward))

    lps_cache = {}
    start_time = time.time()
    max_path = main.find_buffer(buffer_size, matrix, sequences, lps_cache)
    reward = main.calculate_reward([id for _, _, id in max_path], sequences, lps_cache)
    execution_time = f'{(time.time() - start_time) * 1000:.2f} ms'

    label_result = LabelFrame(root, text=f"Result (Execution Time: {execution_time})")
    label_result.pack(expand='yes', fill='both', side='left')

    if reward > 0:
        max_path_str = '\n'.join([f'{y + 1},{x + 1}' for x, y, _ in max_path])
        ids_str = ' '.join([id for _, _, id in max_path])

        reward_label = Label(label_result, text=f"REWARD: {reward}", font=('arial', 10))
        reward_label.grid(row=2, column=0, padx=10, pady=1, sticky='w')

        ids_label = Label(label_result, text=f"TOKENS: {ids_str}", font=('arial', 10))
        ids_label.grid(row=1, column=0, padx=10, pady=1, sticky='w')

        path_label = Label(label_result, text=f"\nPATH:\n{max_path_str}", font=('arial', 10))
        path_label.grid(row=0, column=0, padx=10, pady=1, sticky='w')

    else:
        path_label = Label(label_result, text="No path found", font=('arial', 10))
        path_label.grid(row=0, column=0, padx=10, pady=1, sticky='w')

    # Save result
    def save_result():
        result = f"Reward: {reward}\nTokens: {ids_str}\nPath:\n{max_path_str}"
        with open("result.txt", "w") as file:
            file.write(result)
        messagebox.showinfo("Save", "Result saved to 'result.txt'")

    # Save button
    save_btn = Button(label_main, text='Save', width=10, command=save_result)
    save_btn.grid(row=3, column=1, padx=10, pady=10, sticky='n')

# Master window
root = Tk()
root.geometry('800x600')

# Scroll bar
scrollbar = Scrollbar(root, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

# About
def display_about():
    about_info = "STRICTLY FOR TOKENS: BD 1C 7A 55 E9\n\nA program designed to find the optimal solution for Cyberpunk 2077's Breach Protocol mini-game. To generate new solution, exit and rerun the program.\nDeveloped by Attara Majesta A. (13522139)"
    messagebox.showinfo("About", about_info)

# Menu (exit)
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Exit', command=root.quit)
helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=display_about)

# Title
title = 'CYBERPUNK 777\nBeach Protocol Solver'
root.title(title)
messageVar = Message(root, text=title, font=('@Kozuka Mincho Pr6N L', 15, 'bold'))
messageVar.config(bg='lightgreen', fg='black', width=250, relief='raised', justify='center')
messageVar.pack(pady=10)

subtitle = 'STRICTLY FOR TOKENS: BD 1C 7A 55 E9'
message_sub = Message(root, text=subtitle, font=('@Kozuka Mincho Pr6N L', 10, 'bold'))
message_sub.config(bg='red', fg='black', width=500, relief='raised', justify='center')
message_sub.pack(pady=5)

# Select buffer size
label_buffer = LabelFrame(root, text="Buffer Size")
label_buffer.pack(expand='yes', fill='both')
label_buff_title = Label(label_buffer, text="Select the buffer size :", font=("Times New Roman", 10))
label_buff_title.grid(column=0, row=5, padx=10, pady=25)

n = StringVar()
buffsize_choosen = Combobox(label_buffer, width=27, textvariable=n)
buffsize_choosen['values'] = ('3', '4', '5', '6', '7')
buffsize_choosen.grid(column=1, row=5)
buffsize_choosen.current(0)

# Main label for matrix and sequences
label_main = LabelFrame(root, text="Main Path")
label_main.pack(expand='yes', fill='both', side='right')

label_matrix = Label(label_main, text="CODE MATRIX", font=('arial', 10, 'bold'))
label_matrix.grid(row=0, column=0, padx=10, pady=10, sticky='w')

frame_matrix = Frame(label_main)
frame_matrix.grid(row=1, column=0, padx=10, pady=10, sticky='w')

rows, cols = (6, 6)
text_var = []

for i in range(rows):
    text_var.append([])
    for j in range(cols):
        text_var[i].append(StringVar())
        entry = Entry(frame_matrix, width=5, font=('Arial', 10), textvariable=text_var[i][j])
        entry.grid(row=i, column=j, padx=3, pady=3)

# Random button
random_btn = Button(label_main, text='Random', width=10, command=fill_matrix_randomly)
random_btn.grid(row=2, column=0, padx=10, pady=10)

label_additional = Label(label_main, text="SEQUENCES", font=('arial', 10, 'bold'))
label_additional.grid(row=0, column=1, padx=10, pady=10, sticky='w')

frame_additional = Frame(label_main)
frame_additional.grid(row=1, column=1, padx=10, pady=10, sticky='w')

additional_input = Text(frame_additional, width=30, height=10, font=('Arial', 10))
additional_input.grid(row=0, column=0, padx=3, pady=3)

scrollbar.config(command=additional_input.yview)
additional_input.config(yscrollcommand=scrollbar.set)

random_seq_btn = Button(label_main, text='Random', width=10, command=fill_sequences)
random_seq_btn.grid(row=2, column=1, padx=10, pady=10)

# Solve button
solve_btn = Button(label_main, text='Solve', width=10, command=solve_path)
solve_btn.grid(row=3, column=0, padx=10, pady=10, sticky='n')

root.mainloop()
