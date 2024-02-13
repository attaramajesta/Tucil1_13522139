from tkinter import *
from tkinter.ttk import *
import main

root = Tk()

# Default Display
root.geometry('580x500')

# Menu Bar
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Exit', command=root.quit)
helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About')

# Root Title
title = 'CYBERPUNK 777\nBeach Protocol Solver'
root.title(title)
messageVar = Message(root, text=title, font=('arial', 10, 'bold'))
messageVar.config(bg='lightgreen', fg='black', width=200, relief='raised', justify='center')
messageVar.pack()

# Scroll bar
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

# Buffer label
label_buffer = LabelFrame(root, text="Buffer Size")
label_buffer.pack(expand='yes', fill='both')
label_buff_title = Label(label_buffer, text="Select the buffer size :", font=("Times New Roman", 10))
label_buff_title.grid(column=0, row=5, padx=10, pady=25)

# Combobox creation
n = StringVar()
buffsize_choosen = Combobox(label_buffer, width=27, textvariable=n)
# Adding combobox drop down list
buffsize_choosen['values'] = ('1', '2', '3', '4', '5', '6', '7')
buffsize_choosen.grid(column=1, row=5)
buffsize_choosen.current(0)

# Main label
label_main = LabelFrame(root, text="Main Path")
label_main.pack(expand='yes', fill='both')

# Code Matrix label
label_matrix = Label(label_main, text="CODE MATRIX", font=('arial', 10, 'bold'))
label_matrix.grid(row=0, column=0, padx=10, pady=10, sticky='w')

# Create a container frame for the matrix input
frame_matrix = Frame(label_main)
frame_matrix.grid(row=1, column=0, padx=10, pady=10, sticky='w')

# Input Matrix
rows, cols = (6, 6)
text_var = []
entries = []

for i in range(rows):
    text_var.append([])
    for j in range(cols):
        text_var[i].append(StringVar())
        entry = Entry(frame_matrix, width=5, font=('Arial', 10))
        entry.grid(row=i, column=j, padx=3, pady=3)

# Text widget for additional input
label_additional = Label(label_main, text="SEQUENCES", font=('arial', 10, 'bold'))
label_additional.grid(row=0, column=1, padx=10, pady=10, sticky='w')

frame_additional = Frame(label_main)
frame_additional.grid(row=1, column=1, padx=10, pady=10, sticky='w')

additional_input = Text(frame_additional, width=30, height=10, font=('Arial', 10))
additional_input.grid(row=0, column=0, padx=3, pady=3)

# Save label
label_save = LabelFrame(root, text="Save Path")
label_save.pack(expand='yes', fill='both')

# Save button
save_btn = Button(label_save, text='Save', width=10, command=main.save_all_paths)
save_btn.pack(side=BOTTOM, pady=10, padx=100)

mainloop()
