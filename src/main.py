import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography App")

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

    def setup_hide_data_tab(self):
        self.cover_label = tk.Label(self.hide_data_tab, text="Select Cover Image:")
        self.cover_label.grid(row=0, column=0, pady=10)

        self.cover_path = tk.StringVar()
        self.cover_entry = tk.Entry(self.hide_data_tab, textvariable=self.cover_path, state="disabled", width=40)
        self.cover_entry.grid(row=0, column=1, padx=10)

        self.cover_browse_button = tk.Button(self.hide_data_tab, text="Browse", command=self.browse_cover_image)
        self.cover_browse_button.grid(row=0, column=2)

        self.secret_label = tk.Label(self.hide_data_tab, text="Select Secret Image:")
        self.secret_label.grid(row=1, column=0, pady=10)

        self.secret_path = tk.StringVar()
        self.secret_entry = tk.Entry(self.hide_data_tab, textvariable=self.secret_path, state="disabled", width=40)
        self.secret_entry.grid(row=1, column=1, padx=10)

        self.secret_browse_button = tk.Button(self.hide_data_tab, text="Browse", command=self.browse_secret_image)
        self.secret_browse_button.grid(row=1, column=2)

        self.password_label = tk.Label(self.hide_data_tab, text="Set AES Key:")
        self.password_label.grid(row=2, column=0, pady=10)

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.hide_data_tab, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=2, column=1, padx=10)

        self.hide_button = tk.Button(self.hide_data_tab, text="Hide Data", command=self.hide_data)
        self.hide_button.grid(row=3, column=0, columnspan=3, pady=10)

    def setup_extract_data_tab(self):
        self.stego_label = tk.Label(self.extract_data_tab, text="Select Stego Image:")
        self.stego_label.grid(row=0, column=0, pady=10)

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
        cover_path = self.cover_path.get()
        secret_path = self.secret_path.get()
        password = self.password_var.get()

        if not all([cover_path, secret_path, password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            cover_img = Image.open(cover_path)
            secret_img = Image.open(secret_path)
            
            # Validate AES key
            if len(password) != 16:
                messagebox.showerror("Error", "AES key must be 16 characters long.")
                return

            # Perform AES encryption on secret data
            encrypted_secret_data = self.encrypt_data(secret_img.tobytes(), password)
            
            # Perform LSB image steganography here
            stego_img = self.perform_lsb_steganography(cover_img, encrypted_secret_data)
            
            # Save the steganographic result to the specified path
            stego_img_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if stego_img_path:
                stego_img.save(stego_img_path)
                messagebox.showinfo("Success", f"Data hidden successfully!\nStego image saved at: {stego_img_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing images: {str(e)}")

    def perform_lsb_steganography(self, cover_img, secret_data):
        # Convert secret data to binary string
        binary_secret_data = ''.join(format(byte, '08b') for byte in secret_data)

        # Convert cover image to RGB mode
        cover_img = cover_img.convert("RGB")

        # Get the pixel data from the cover image
        cover_pixels = cover_img.load()

        # Embed secret data into the least significant bits of the cover image
        binary_data_index = 0
        for i in range(cover_img.size[0]):
            for j in range(cover_img.size[1]):
                r, g, b = cover_pixels[i, j]

                # Modify the least significant bit of each color component
                r = (r & 0b11111110) | int(binary_secret_data[binary_data_index])
                binary_data_index += 1
                g = (g & 0b11111110) | int(binary_secret_data[binary_data_index])
                binary_data_index += 1
                b = (b & 0b11111110) | int(binary_secret_data[binary_data_index])
                binary_data_index += 1

                # Update the pixel in the cover image
                cover_pixels[i, j] = (r, g, b)

                # Check if all secret data is embedded
                if binary_data_index >= len(binary_secret_data):
                    break

            if binary_data_index >= len(binary_secret_data):
                break

        return cover_img

    def extract_data(self):
        stego_path = self.stego_path.get()
        password = self.extract_password_var.get()

        if not all([stego_path, password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
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
            extracted_img_path = os.path.join("C:\\Users\\vedsm\\Downloads", "extracted_image.png")
            Image.frombytes('RGB', stego_img.size, secret_data).save(extracted_img_path)
            messagebox.showinfo("Success", f"Extracted image saved at: {extracted_img_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing stego image: {str(e)}")

    def extract_lsb_steganography(self, stego_img):
        # Convert stego image to RGB mode
        stego_img = stego_img.convert("RGB")

        # Get the pixel data from the stego image
        stego_pixels = stego_img.load()

        # Extract the least significant bits from the stego image
        binary_secret_data = ''
        for i in range(stego_img.size[0]):
            for j in range(stego_img.size[1]):
                r, g, b = stego_pixels[i, j]

                # Extract the least significant bit from each color component
                r_secret = (r & 1)
                g_secret = (g & 1)
                b_secret = (b & 1)

                # Combine the extracted bits to form the binary data
                binary_secret_data += str(r_secret) + str(g_secret) + str(b_secret)

        return binary_secret_data

    def encrypt_data(self, data, key):
        cipher = Cipher(algorithms.AES(key.encode("utf-8")), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return base64.b64encode(ciphertext)

    def decrypt_data(self, encrypted_data, key):
        encrypted_data = base64.b64decode(encrypted_data)
        cipher = Cipher(algorithms.AES(key.encode("utf-8")), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        return decrypted_data

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
