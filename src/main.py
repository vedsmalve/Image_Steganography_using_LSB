# main.py
from gui import SteganographyApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
