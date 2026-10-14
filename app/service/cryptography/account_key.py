#import threading

#import pyperclip
from app.models.account_base_model import Account
from app.service.cryptography.passkey_formatter import KeyFormat
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def gen_account_key( master_key:bytes, account: Account) -> str:

        info = (f"{account.system_name}:{account.version}".encode())

        hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=info)

        account_key = hkdf.derive(master_key)

        password = KeyFormat().generate_passkey(account_key, account.policy)

        return password

        #pyperclip.copy(password)
        #threading.Timer(20, lambda: pyperclip.copy("")).start()