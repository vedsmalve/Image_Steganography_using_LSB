import tkinter as tk

def on_enter(e):
    my_button['background'] = '#a6f6ed'

def on_leave(e):
    my_button['background'] = 'SystemButtonFace'

root = tk.Tk()

my_Label = tk.Label(root, text="Color changing button")
my_Label.grid(row=0, column=1, padx=10, pady=10)

my_button = tk.Button(root, text="Hover over me", width=50, activebackground='#08dfc7')
my_button.grid(row=1, column=1, padx=10, pady=10)

my_button.bind("<Enter>", on_enter)
my_button.bind("<Leave>", on_leave)

root.mainloop()