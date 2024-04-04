# gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from steganography import hide_image, extract_image

class SteganographyApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Steganography App")
        master.geometry("700x500")

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.hide_tab = ttk.Frame(self.notebook)
        self.extract_tab = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.hide_tab, text="Hide Data")
        self.notebook.add(self.extract_tab, text="Extract Data")

        # Initialize GUI elements in each tab
        self.init_hide_tab()
        self.init_extract_tab()

    def init_hide_tab(self):
        # Elements for the 'Hide Data' tab
        #hide_label = tk.Label(self.hide_tab, text="Hide Data Section", font=('Helvetica', 16))
        #hide_label.pack(pady=10)

        # Placeholders and buttons for 'Hide Data' tab
        self.cover_image_path_var = tk.StringVar()
        self.secret_image_path_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        cover_label = tk.Label(self.hide_tab, text="Choose Cover image")
        cover_label.pack(pady=5)
        cover_placeholder = tk.Entry(self.hide_tab, textvariable=self.cover_image_path_var, state='readonly')
        cover_placeholder.pack(pady=5)
        browse_cover_button = tk.Button(self.hide_tab, text="Browse", command=self.browse_cover_image)
        browse_cover_button.pack(pady=5)

        secret_label = tk.Label(self.hide_tab, text="Choose Secret image", font=('Helvetica', 15))
        secret_label.pack(pady=5)
        secret_placeholder = tk.Entry(self.hide_tab, textvariable=self.secret_image_path_var, state='readonly')
        secret_placeholder.pack(pady=5)
        browse_secret_button = tk.Button(self.hide_tab, text="Browse", command=self.browse_secret_image)
        browse_secret_button.pack(pady=5)

        password_label = tk.Label(self.hide_tab, text="Enter password")
        password_label.pack(pady=5)
        password_entry = tk.Entry(self.hide_tab, textvariable=self.password_var, show='*')
        password_entry.pack(pady=5)

        confirm_password_label = tk.Label(self.hide_tab, text="Confirm Password")
        confirm_password_label.pack(pady=5)
        confirm_password_entry = tk.Entry(self.hide_tab, textvariable=self.confirm_password_var, show='*')
        confirm_password_entry.pack(pady=5)

        hide_data_button = tk.Button(self.hide_tab, text="Hide Data", command=self.hide_data, bg="blue", fg="white")
        hide_data_button.pack(pady=10)

        clear_button = tk.Button(self.hide_tab, text="Clear", command=self.clear_hide_data_fields, bg="red", fg="white")
        clear_button.pack(pady=5)

    def init_extract_tab(self):
        # Elements for the 'Extract Data' tab
        extract_label = tk.Label(self.extract_tab, text="Extract Data Section", font=('Helvetica', 16))
        extract_label.pack(pady=10)

        # Placeholders and buttons for 'Extract Data' tab
        self.stego_image_path_var = tk.StringVar()
        self.extract_password_var = tk.StringVar()

        stego_label = tk.Label(self.extract_tab, text="Choose Stego image")
        stego_label.pack(pady=5)
        stego_placeholder = tk.Entry(self.extract_tab, textvariable=self.stego_image_path_var, state='readonly')
        stego_placeholder.pack(pady=5)
        browse_stego_button = tk.Button(self.extract_tab, text="Browse", command=self.browse_stego_image)
        browse_stego_button.pack(pady=5)

        extract_password_label = tk.Label(self.extract_tab, text="Enter Password")
        extract_password_label.pack(pady=5)
        extract_password_entry = tk.Entry(self.extract_tab, textvariable=self.extract_password_var, show='*')
        extract_password_entry.pack(pady=5)

        extract_data_button = tk.Button(self.extract_tab, text="Extract Data", command=self.extract_data, bg="blue", fg="white")
        extract_data_button.pack(pady=10)

        clear_button = tk.Button(self.extract_tab, text="Clear", command=self.clear_extract_data_fields, bg="red", fg="white")
        clear_button.pack(pady=5)

    def browse_cover_image(self):
        self.cover_image_path_var.set(filedialog.askopenfilename(title="Select Cover Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]))

    def browse_secret_image(self):
        self.secret_image_path_var.set(filedialog.askopenfilename(title="Select Secret Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]))

    def browse_stego_image(self):
        self.stego_image_path_var.set(filedialog.askopenfilename(title="Select Stego Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]))

    def hide_data(self):
        cover_image_path = self.cover_image_path_var.get()
        secret_image_path = self.secret_image_path_var.get()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        if not cover_image_path or not secret_image_path or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields.")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
        else:
            save_path = hide_image(cover_image_path, secret_image_path)
            messagebox.showinfo("Success", "Data hidden successfully!\nImage saved at: {}".format(save_path))

    def extract_data(self):
        stego_image_path = self.stego_image_path_var.get()
        password = self.extract_password_var.get()

        if not stego_image_path or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
        else:
            try:
                # Provide a default save_path for the extracted image
                save_path = filedialog.asksaveasfilename(title="Save Extracted Image", filetypes=[("Image files", "*.png")])
                if save_path:
                    extract_image(stego_image_path, save_path, password)
                    messagebox.showinfo("Success", "Data extracted successfully!\nImage saved at: {}".format(save_path))
                else:
                    messagebox.showinfo("Info", "Extraction canceled.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def clear_hide_data_fields(self):
        self.cover_image_path_var.set("")
        self.secret_image_path_var.set("")
        self.password_var.set("")
        self.confirm_password_var.set("")

    def clear_extract_data_fields(self):
        self.stego_image_path_var.set("")
        self.extract_password_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
