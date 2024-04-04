import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from tkinter import messagebox  # Importing messagebox for showing errors in the GUI
from ttkthemes import ThemedStyle
from encryption import encrypt_data, decrypt_data
from lsb_steganography import LSBSteganography  # Import the function
from about import AboutTab

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography App")
        self.root.geometry("700x450")
        self.tabControl = ttk.Notebook(self.root)

        # Apply ThemedStyle
        style = ThemedStyle(root)
        style.set_theme("elegance")

        self.tabControl = ttk.Notebook(self.root)

        # Hide Data tab
        self.hide_data_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.hide_data_tab, text="Hide Data")
        self.setup_hide_data_tab()

        # Extract Data tab
        self.extract_data_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.extract_data_tab, text="Extract Data")
        self.setup_extract_data_tab()

        self.tabControl.pack(expand=1, fill="both")

        # About tab
        self.about_developers = [
            {
                "name": "Ved Malve",
                "linkedin": "https://www.linkedin.com/in/vedsmalve/",
            },
            {
                "name": "Aditya Sonar",
                "linkedin": "https://www.linkedin.com/in/aditya-sonar-03afd/",
            },
            {
                "name": "Shashikant Kandekar",
                "linkedin": "https://www.linkedin.com/in/shashikantkandekar/",
            },
            {
                "name": "Samadhan Kardile",
                "linkedin": "https://www.linkedin.com/in/samadhan-kardile-5bb28526b?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app",
            },
        ]
        self.about_tab = AboutTab(self.tabControl, self.about_developers)

        self.tabControl.add(self.about_tab.about_tab, text="About")

        self.tabControl.pack(expand=1, fill="both")


    def setup_hide_data_tab(self):
        self.cover_label = tk.Label(self.hide_data_tab, text="Select Cover Image:", anchor="center")
        self.cover_label.grid(row=0, column=1, pady=20, padx=60)

        self.cover_path = tk.StringVar()
        self.cover_entry = tk.Entry(self.hide_data_tab, textvariable=self.cover_path, state="normal", width=60)
        self.cover_entry.grid(row=0, column=2, padx=11)

        self.cover_browse_button = tk.Button(self.hide_data_tab, text="Browse Image", command=self.browse_cover_image, width=50)
        self.cover_browse_button.grid(row=1, column=2)

        self.secret_label = tk.Label(self.hide_data_tab, text="Select Secret Image:")
        self.secret_label.grid(row=2, column=1,padx=19, pady=19)

        self.secret_path = tk.StringVar()
        self.secret_entry = tk.Entry(self.hide_data_tab, textvariable=self.secret_path, state="normal", width=60)
        self.secret_entry.grid(row=2, column=2, padx=11)

        self.secret_browse_button = tk.Button(self.hide_data_tab, text="Browse Image", command=self.browse_secret_image, width=50)
        self.secret_browse_button.grid(row=3, column=2)

        # Password Functionality
        self.password_label = tk.Label(self.hide_data_tab, text="Set AES Key:") # entering password once
        self.password_label.grid(row=4, column=1,padx=1, pady=19)

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.hide_data_tab, textvariable=self.password_var, show="*", width=50)
        self.password_entry.grid(row=4, column=2, padx=11)

        self.password_label2 = tk.Label(self.hide_data_tab, text="Confirm AES Key:") # confirming password
        self.password_label2.grid(row=5, column=1,padx=1, pady=19)

        self.password_var2 = tk.StringVar()  # Use a different StringVar for the second password entry
        self.password_entry2 = tk.Entry(self.hide_data_tab, textvariable=self.password_var2, show="*", width=50)
        self.password_entry2.grid(row=5, column=2, padx=11)

        # Button Functionality
        self.hide_button = tk.Button(self.hide_data_tab, text="Hide Data", background='lightblue', command=self.hide_data, activebackground='red')
        self.hide_button.grid(row=7, column=2, columnspan=3, pady=10)

        self.hide_button.bind("<Enter>", self.on_enter)
        self.hide_button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.hide_button['background'] = 'lightgreen'

    def on_leave(self, e):
        self.hide_button['background'] = 'lightblue'

    def setup_extract_data_tab(self):
        self.stego_label = tk.Label(self.extract_data_tab, text="Select Stego Image:", anchor="center")
        self.stego_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.stego_path = tk.StringVar()
        self.stego_entry = tk.Entry(self.extract_data_tab, textvariable=self.stego_path, state="disabled", width=40)
        self.stego_entry.grid(row=0, column=1, padx=10)

        self.stego_browse_button = tk.Button(self.extract_data_tab, text="Browse", command=self.browse_stego_image)
        self.stego_browse_button.grid(row=0, column=2)

        self.extract_password_label = tk.Label(self.extract_data_tab, text="Enter AES Key:")
        self.extract_password_label.grid(row=1, column=0, pady=10)

        self.extract_password_var = tk.StringVar()
        self.extract_password_entry = tk.Entry(self.extract_data_tab, textvariable=self.extract_password_var, show="*")
        self.extract_password_entry.grid(row=1, column=1, padx=10)

        self.extract_button = tk.Button(self.extract_data_tab, text="Extract Data", command=self.extract_data)
        self.extract_button.grid(row=2, column=0, columnspan=3, pady=10)

    def browse_cover_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.cover_path.set(file_path)

    def browse_secret_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.secret_path.set(file_path)

    def browse_stego_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.stego_path.set(file_path)

    def hide_data(self):
        try:
            cover_path = self.cover_path.get()
            secret_path = self.secret_path.get()
            password = self.password_var.get()

            if not all([cover_path, secret_path, password]):
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            # Check if the image files exist before trying to open them
            if not os.path.isfile(cover_path):
                messagebox.showerror("Error", "Cover image file does not exist.")
                return

            if not os.path.isfile(secret_path):
                messagebox.showerror("Error", "Secret image file does not exist.")
                return

            # Resize secret image to be smaller than cover image
            scale_factor = min(cover_img.size[0] / secret_img.size[0], cover_img.size[1] / secret_img.size[1]) * 0.9
            new_size = (int(secret_img.size[0] * scale_factor), int(secret_img.size[1] * scale_factor))
            secret_img = secret_img.resize(new_size, Image.ANTIALIAS)

            cover_img = Image.open(cover_path)
            secret_img = Image.open(secret_path)

            # Validate AES key
            if len(password) != 16:
                messagebox.showerror("Error", "AES key must be 16 characters long.")
                return

            # Update the encryption mode to CBC
            cipher = Cipher(algorithms.AES(password.encode("utf-8")), modes.CBC(os.urandom(16)), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(secret_img.tobytes()) + encryptor.finalize()

            # Check if cover image is large enough to hold secret data
            if cover_img.size[0] * cover_img.size[1] * 3 < len(ciphertext) * 8:
                raise ValueError("Cover image is not large enough to hold secret data.")

            # Pass secret_data to perform_lsb_steganography (correct usage)
            stego_img = LSBSteganography.perform_lsb_steganography(cover_img, ciphertext)

            # Save the steganographic result to the specified path
            stego_img_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if stego_img_path:
                stego_img.save(stego_img_path)
                messagebox.showinfo("Success", f"Data hidden successfully!\nStego image saved at: {stego_img_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing images: {str(e)}")

    def extract_data(self):
        try:
            stego_path = self.stego_path.get()
            password = self.extract_password_var.get()

            if not all([stego_path, password]):
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            stego_img = Image.open(stego_path)

            # Validate AES key
            if len(password) != 16:
                messagebox.showerror("Error", "AES key must be 16 characters long.")
                return

            # Perform LSB steganography extraction here
            binary_secret_data = self.extract_lsb_steganography(stego_img)

            # Perform AES decryption to get the original secret data
            secret_data = self.decrypt_data(binary_secret_data, password)

            # Save the extracted image to the specified path
            extracted_img_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if extracted_img_path:
                Image.frombytes('RGB', stego_img.size, secret_data).save(extracted_img_path)
                messagebox.showinfo("Success", f"Extracted image saved at: {extracted_img_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing stego image: {str(e)}")

    def extract_lsb_steganography(self, stego_img):
        stego_img = stego_img.convert("RGB")
        stego_pixels = stego_img.load()
        binary_secret_data = bytearray()
        current_byte = 0
        bit_count = 0

        for i in range(stego_img.size[0]):
            for j in range(stego_img.size[1]):
                r, g, b = stego_pixels[i, j]

                r_secret = (r & 1) << 7
                g_secret = (g & 1) << 6
                b_secret = (b & 1) << 5

                current_byte |= (r_secret | g_secret | b_secret) >> bit_count
                bit_count += 3

                if bit_count >= 8:
                    binary_secret_data.append(current_byte)
                    current_byte = 0
                    bit_count = 0

        return bytes(binary_secret_data)

    def decrypt_data(self, encrypted_data, key):
        return decrypt_data(encrypted_data, key)

    def run_application(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    app.run_application()
