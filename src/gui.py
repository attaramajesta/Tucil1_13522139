from tkinter import *
from tkinter.ttk import *
import main
import numpy as np
import random
import time

def fill_matrix_randomly():
    tokens = ['BD', '1C', '7A', '55', 'E9']
    for i in range(rows):
        for j in range(cols):
            token = np.random.choice(tokens)
            text_var[i][j].set(token)

def fill_sequences():
    num_sequences = 3
    max_sequence_size = 3
    tokens = ['BD', '1C', '7A', '55', 'E9']
    
    additional_input.delete("1.0", END)

    for _ in range(num_sequences):
        sequence = ' '.join(random.choices(tokens, k=max_sequence_size))
        reward = random.choice([10, 20, 30])
        additional_input.insert(END, f"{sequence}\n{reward}\n")

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
    print(f'Execution time: {execution_time}')

    max_path_str = ' : '.join([f'{y + 1},{x + 1}' for x, y, _ in max_path])
    ids_str = ' '.join([id for _, _, id in max_path])

    label_result = LabelFrame(root, text="Result")
    label_result.pack(expand='yes', fill='both')

    path_label = Label(label_result, text=f"Path: {max_path_str}", font=('arial', 10))
    path_label.grid(row=0, column=0, padx=10, pady=1, sticky='w')

    ids_label = Label(label_result, text=f"IDs: {ids_str}", font=('arial', 10))
    ids_label.grid(row=1, column=0, padx=10, pady=1, sticky='w')

    reward_label = Label(label_result, text=f"Reward: {reward}", font=('arial', 10))
    reward_label.grid(row=2, column=0, padx=10, pady=1, sticky='w')

root = Tk()
root.geometry('580x500')

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Exit', command=root.quit)
helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About')

title = 'CYBERPUNK 777\nBeach Protocol Solver'
root.title(title)
messageVar = Message(root, text=title, font=('arial', 10, 'bold'))
messageVar.config(bg='lightgreen', fg='black', width=200, relief='raised', justify='center')
messageVar.pack()

label_buffer = LabelFrame(root, text="Buffer Size")
label_buffer.pack(expand='yes', fill='both')
label_buff_title = Label(label_buffer, text="Select the buffer size :", font=("Times New Roman", 10))
label_buff_title.grid(column=0, row=5, padx=10, pady=25)

n = StringVar()
buffsize_choosen = Combobox(label_buffer, width=27, textvariable=n)
buffsize_choosen['values'] = ('1', '2', '3', '4', '5', '6', '7')
buffsize_choosen.grid(column=1, row=5)
buffsize_choosen.current(0)

label_main = LabelFrame(root, text="Main Path")
label_main.pack(expand='yes', fill='both')

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

random_btn = Button(label_main, text='Random', width=10, command=fill_matrix_randomly)
random_btn.grid(row=2, column=0, padx=10, pady=10)

label_additional = Label(label_main, text="SEQUENCES", font=('arial', 10, 'bold'))
label_additional.grid(row=0, column=1, padx=10, pady=10, sticky='w')

frame_additional = Frame(label_main)
frame_additional.grid(row=1, column=1, padx=10, pady=10, sticky='w')

additional_input = Text(frame_additional, width=30, height=10, font=('Arial', 10))
additional_input.grid(row=0, column=0, padx=3, pady=3)

random_seq_btn = Button(label_main, text='Random', width=10, command=fill_sequences)
random_seq_btn.grid(row=2, column=1, padx=10, pady=10)

solve_btn = Button(label_main, text='Solve', width=10, command=solve_path)
solve_btn.grid(row=3, column=1, padx=10, pady=10)

root.mainloop()
