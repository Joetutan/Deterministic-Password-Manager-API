import secrets

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


class AccountCrypt:

    def __init__(self):
        self.nonce_length = 12

    def encrypt_account(self, plaintext:bytes, master_key:bytes) -> bytes:
        nonce = secrets.token_bytes(self.nonce_length)
        cipher = ChaCha20Poly1305(master_key)
        ciphertext = cipher.encrypt(nonce=nonce, data=plaintext, associated_data=None)
        return nonce + ciphertext

    def decrypt_account(self, master_key:str, encrypted:bytes) -> bytes:
        nonce = encrypted[:self.nonce_length]
        cipher = ChaCha20Poly1305(master_key)
        cipher_text= encrypted[self.nonce_length:]
        return cipher.decrypt(nonce=nonce, data=cipher_text, associated_data=None)