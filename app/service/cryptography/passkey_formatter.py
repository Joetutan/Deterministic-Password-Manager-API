import hashlib
import hmac
import string

from app.models.policy_data_model import AccountPolicy

char_set = {
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "digits": string.digits,
    "symbols": "!@#$%^&*()-_=+[]{}"
}

class KeyFormat:

    def generate_passkey(self, account_key:bytes, policy: AccountPolicy)->str:

        groups = []

        match policy:
            case policy.lower:
                groups.append(char_set["loser"])
            case policy.upper:
                groups.append(char_set["upper"])
            case policy.digits:
                groups.append(char_set["digits"])
            case policy.symbols:
                groups.append(char_set["symbols"])


        if not groups:
            raise ValueError("No charset selected")

        if policy.length < len(groups):
            raise ValueError("Password, length must be at least the number of enabled character classes")


        stream = self._byte_stream(account_key)

        password = []

        # step 1: Guarantee one character from each set.

        for group in groups:
            byte = next(stream)
            password.append(group[byte % len(group)])

         # step 2: Fill-in remaining characters.

        alphabet = "".join(groups)

        while len(password) <  policy.length:
            byte = next(stream)
            password.append(alphabet[byte % len(alphabet)])

        # step 3: Deterministic Fisher-Yates shuffle.

        for i in range(len(password) - 1, 0, -1):
            byte = next(stream)
            j = byte % (i + 1)

            password[i], password[j] = password[j], password[i]

        return "".join(password)


    def _byte_stream(self, key:bytes):

        counter= 0

        while True:
            block = hmac.new(key, counter.to_bytes(4, "big"),hashlib.sha256).digest()

            yield block

            counter += 1
         
