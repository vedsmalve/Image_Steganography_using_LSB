# steganography.py
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

def hide_image(cover_image_path, secret_image_path):
    # Open cover and secret images
    cover_image = Image.open(cover_image_path)
    secret_image = Image.open(secret_image_path)

    # Ensure the images have the same size
    secret_image = secret_image.resize(cover_image.size)

    # Convert images to RGB mode
    cover_image = cover_image.convert('RGB')
    secret_image = secret_image.convert('RGB')

    # Get the pixel data from each image
    cover_pixels = list(cover_image.getdata())
    secret_pixels = list(secret_image.getdata())

    # Perform LSB algorithm to hide the secret image in the cover image
    new_pixels = []
    for cover_pixel, secret_pixel in zip(cover_pixels, secret_pixels):
        new_pixel = tuple([(cover_channel & 0b11111110) | (secret_channel >> 7) for cover_channel, secret_channel in zip(cover_pixel, secret_pixel)])
        new_pixels.append(new_pixel)

    # Create a new image with the modified pixel data
    new_image = Image.new('RGB', cover_image.size)
    new_image.putdata(new_pixels)

     # Save the new image
    save_path = 'hidden_image.png'
    new_image.save(save_path)
    print("Image hidden successfully!")
    return save_path

def extract_image(cover_image_path, save_path, password):
    # Open the cover image
    cover_image = Image.open(cover_image_path)

    # Convert the cover image to RGB mode
    cover_image = cover_image.convert('RGB')

    # Get the pixel data from the cover image
    cover_pixels = list(cover_image.getdata())

    # Extract the secret image using LSB algorithm
    extracted_pixels = [tuple([(cover_channel & 1) << 7 for cover_channel in cover_pixel]) for cover_pixel in cover_pixels]

    # Create a new image with the extracted pixel data
    extracted_image = Image.new('RGB', cover_image.size)
    extracted_image.putdata(extracted_pixels)

    # Save the extracted image
    extracted_image.save(save_path)
    print("Image extracted successfully!")

    # Validate password and decrypt using AES
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted_data = unpad(cipher.decrypt(extracted_image.tobytes()), AES.block_size)
        decrypted_image = Image.frombytes('RGB', extracted_image.size, decrypted_data)
        save_path = 'extracted_image.png'
        decrypted_image.save(save_path)
        print("Image decrypted and saved successfully!")
        return save_path
    except ValueError:
        raise ValueError("Incorrect password. Extraction failed.")
