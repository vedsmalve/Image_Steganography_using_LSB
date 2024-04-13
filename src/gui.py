import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from steganography import hide_image, extract_image
import customtkinter as ctk
from PIL import ImageTk, Image
                            
class SteganographyApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Steganography App")
        master.geometry("700x620")
        master.iconbitmap('icon.ico')  # Add this line

        # Set background image
        self.background_image = ImageTk.PhotoImage(Image.open('bg_pattern.png'))  # Replace with your image path
        background_label = tk.Label(master, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame in the center
        self.frame = ctk.CTkFrame(master, width=400, height=int(master.winfo_screenheight() * 0.7))
        self.frame.place(relx=0.5, rely=0.5, anchor='center')
        self.frame.grid_propagate(False)

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.frame)  # Use ttk.Notebook
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.hide_tab = ctk.CTkFrame(self.notebook)
        self.extract_tab = ctk.CTkFrame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.hide_tab, text="Hide Data")
        self.notebook.add(self.extract_tab, text="Extract Data")

        # Initialize StringVars
        self.cover_image_path_var = tk.StringVar()
        self.secret_image_path_var = tk.StringVar()
        self.stego_image_path_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.extract_password_var = tk.StringVar()  # Add this line

        # Initialize GUI elements in each tab
        self.init_hide_tab()
        self.init_extract_tab()

    def init_hide_tab(self):
        # Elements for the 'Hide Data' tab
        hide_data_label = ctk.CTkLabel(self.hide_tab, text="Hide Data Section", font=('Century Gothic',20), width=400)
        hide_data_label.pack(pady=10)

        cover_label = ctk.CTkLabel(self.hide_tab, text="Choose Cover image")
        cover_label.pack(pady=5)
        cover_placeholder = ctk.CTkEntry(self.hide_tab, state='readonly', width=200, textvariable=self.cover_image_path_var)
        cover_placeholder.pack(pady=5)
        browse_cover_button = ctk.CTkButton(self.hide_tab, text="Browse", command=self.browse_cover_image)
        browse_cover_button.pack(pady=5)

        secret_label = ctk.CTkLabel(self.hide_tab, text="Choose Secret image")
        secret_label.pack(pady=5)
        secret_placeholder = ctk.CTkEntry(self.hide_tab, state='readonly', width=200, textvariable=self.secret_image_path_var)
        secret_placeholder.pack(pady=5)
        browse_secret_button = ctk.CTkButton(self.hide_tab, text="Browse", command=self.browse_secret_image)
        browse_secret_button.pack(pady=5)

        password_label = ctk.CTkLabel(self.hide_tab, text="Enter password")
        password_label.pack(pady=5)
        password_entry = ctk.CTkEntry(self.hide_tab, show='*', width=200, textvariable=self.password_var)
        password_entry.pack(pady=5)

        confirm_password_label = ctk.CTkLabel(self.hide_tab, text="Confirm Password")
        confirm_password_label.pack(pady=5)
        confirm_password_entry = ctk.CTkEntry(self.hide_tab, show='*', width=200, textvariable=self.confirm_password_var)
        confirm_password_entry.pack(pady=5)

        hide_data_button = ctk.CTkButton(self.hide_tab, text="Hide Data", command=self.hide_data,corner_radius=32)
        hide_data_button.pack(pady=10)

        clear_button = ctk.CTkButton(self.hide_tab, text="Clear", command=self.clear_hide_data_fields,corner_radius=32)
        clear_button.pack(pady=5)

    def init_extract_tab(self):
        # Elements for the 'Extract Data' tab
        extract_data_label = ctk.CTkLabel(self.extract_tab, text="Extract Data Section", font=('Century Gothic',20))
        extract_data_label.pack(pady=10)

        stego_label = ctk.CTkLabel(self.extract_tab, text="Choose Stego image")
        stego_label.pack(pady=5)
        stego_placeholder = ctk.CTkEntry(self.extract_tab, state='readonly', width=200, textvariable=self.stego_image_path_var)
        stego_placeholder.pack(pady=5)
        browse_stego_button = ctk.CTkButton(self.extract_tab, text="Browse", command=self.browse_stego_image)
        browse_stego_button.pack(pady=5)

        extract_password_label = ctk.CTkLabel(self.extract_tab, text="Enter Password")
        extract_password_label.pack(pady=5)
        extract_password_entry = ctk.CTkEntry(self.extract_tab, show='*', width=200, textvariable=self.extract_password_var)  # Use extract_password_var here
        extract_password_entry.pack(pady=5)

        extract_data_button = ctk.CTkButton(self.extract_tab, text="Extract Data", command=self.extract_data, corner_radius=32)
        extract_data_button.pack(pady=10)

        clear_button = ctk.CTkButton(self.extract_tab, text="Clear", command=self.clear_extract_data_fields, corner_radius=32)
        clear_button.pack(pady=5)

    def browse_cover_image(self):
        cover_image_path = filedialog.askopenfilename(title="Select Cover Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.cover_image_path_var.set(cover_image_path)

    def browse_secret_image(self):
        secret_image_path = filedialog.askopenfilename(title="Select Secret Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.secret_image_path_var.set(secret_image_path)

    def browse_stego_image(self):
        stego_image_path = filedialog.askopenfilename(title="Select Stego Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.stego_image_path_var.set(stego_image_path)

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
            # Call hide_image with all required arguments
            save_path = hide_image(cover_image_path, secret_image_path, password)
            messagebox.showinfo("Success", "Data hidden successfully!\nImage saved at: {}".format(save_path))

    def extract_data(self):
        stego_image_path = self.stego_image_path_var.get()
        password = self.extract_password_var.get()  # Use extract_password_var here

        if not stego_image_path or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
        else:
            try:
                # Provide a default save_path for the extracted image
                save_path = filedialog.asksaveasfilename(title="Save Extracted Image", filetypes=[("Image files", "*.png")], defaultextension=".png", initialfile="secret")
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
        self.extract_password_var.set("")  # Clear extract_password_var here

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
