# lsb_steganography.py
from PIL import Image

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

