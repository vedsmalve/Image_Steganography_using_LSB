import webbrowser
import tkinter as tk
from tkinter import ttk

class AboutTab:
    def __init__(self, parent_tab, developers_info):
        self.about_tab = ttk.Frame(parent_tab)
        self.developers_info = developers_info
        self.setup_about_tab()

    def setup_about_tab(self):
        about_frame = ttk.Frame(self.about_tab)

        about_label = tk.Label(about_frame, text="About Image Steganography App", font=("Helvetica", 16, "bold"))
        about_label.grid(row=0, column=0, pady=10)

        about_text = tk.Text(about_frame, height=10, width=60, wrap=tk.WORD, padx=10, pady=10)
        about_text.grid(row=1, column=0)

        about_text.insert(tk.END, "This Image Steganography App allows you to hide and extract data within images using the LSB method.\n\n")
        
        for developer in self.developers_info:
            about_text.insert(tk.END, f"Developer: {developer['name']}\n")
            about_text.insert(tk.END, f"LinkedIn: {developer['linkedin']}\n\n")

        about_text.config(state=tk.DISABLED)

        about_frame.pack(expand=True, fill='both')

    def open_linkedin_profile(self, developer):
        linkedin_url = f"https://www.linkedin.com/in/{developer['linkedin']}/"
        webbrowser.open(linkedin_url)
