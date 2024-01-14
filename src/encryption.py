# encryption.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

def encrypt_data(data, key):
    """
    Encrypts data using AES encryption algorithm.

    Parameters:
    - data: Bytes-like object to be encrypted.
    - key: Encryption key (16 characters).

    Returns:
    - Encrypted data in base64 encoding.
    """
    cipher = Cipher(algorithms.AES(key.encode("utf-8")), modes.CBC(os.urandom(16)), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return base64.b64encode(ciphertext)

def decrypt_data(encrypted_data, key):
    """
    Decrypts AES-encrypted data.

    Parameters:
    - encrypted_data: Base64-encoded encrypted data.
    - key: Decryption key (16 characters).

    Returns:
    - Decrypted data as bytes.
    """
    encrypted_data = base64.b64decode(encrypted_data)
    cipher = Cipher(algorithms.AES(key.encode("utf-8")), modes.CBC(os.urandom(16)), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return unpadded_data
    except Exception as e:
        messagebox.showerror("Error", f"Error decrypting data: {str(e)}")
        return b''
