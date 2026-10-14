import secrets

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


class MetaCrypt:

    def __init__(self):
        self.nonce_length = 12

    def encrypt_meta(self, plaintext:bytes, meta_key:bytes) -> bytes:
        nonce = secrets.token_bytes(self.nonce_length)
        cipher = ChaCha20Poly1305(meta_key)
        ciphertext = cipher.encrypt(nonce=nonce, data=plaintext, associated_data=None)
        return nonce + ciphertext

    def decrypt_meta(self, meta_key:str, encrypted:bytes) -> bytes:
        nonce = encrypted[:self.nonce_length]
        cipher = ChaCha20Poly1305(meta_key)
        cipher_text= encrypted[self.nonce_length:]
        return cipher.decrypt(nonce=nonce, data=cipher_text, associated_data=None)