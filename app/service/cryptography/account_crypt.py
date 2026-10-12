'''
import base64
import json
import secrets
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305




import os
from cryptography.hazmat.primitives.ciphers.aead import (ChaCha20Poly1305)


class VaultCrypt:

    NONCE_LENGTH = 12

    def encrypt_vault(self, data:dict , master_key:bytes)->bytes:
        payload = {
        "system_name": system_name,
        "user_name": user_name,
        "version": version,
        "policy": policy,
        "metadata": metadata,
    }
        plaintext = json.dumps(payload,separators=(",", ":"),sort_keys=True,).encode("utf-8")

        nonce = secrets.token_bytes(12)
        cipher = ChaCha20Poly1305(master_key)
        ciphertext = cipher.encrypt(nonce=nonce,data=plaintext,associated_data=None,)
        return  base64.b64encode(nonce + ciphertext).decode("ascii")
    
    def decrypt_vault(self, master_key, encrypted_vault) ->bytes:
        nonce = encrypted_vault[:self.NONCE_LENGTH]
        cipher = ChaCha20Poly1305(master_key)
        cipher_text = encrypted_vault[self.NONCE_LENGTH:]
        return cipher.decrypt(nonce=nonce, data=cipher_text,associated_data=None,)

'
def encrypt_account_payload(
    *,
    key: bytes,
    system_name: str,
    user_name: str,
    version: int,
    policy: dict[str, Any],
    metadata: dict[str, Any],
) -> dict[str, str]:
    """
    Encrypt account data using ChaCha20-Poly1305.

    key must be a securely derived 32-byte encryption key.
    """

    if len(key) != 32:
        raise ValueError("Encryption key must be exactly 32 bytes")

    payload = {
        "system_name": system_name,
        "user_name": user_name,
        "version": version,
        "policy": policy,
        "metadata": metadata,
    }

    plaintext = json.dumps(payload,separators=(",", ":"),sort_keys=True,).encode("utf-8")
    nonce = secrets.token_bytes(12)
    cipher = ChaCha20Poly1305(key)
    ciphertext = cipher.encrypt(nonce, plaintext, None)

    return {
        "algorithm": "ChaCha20-Poly1305",
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    }

'''