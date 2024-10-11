import hashlib
import secrets


def generate_token() -> str:
    raw_token = secrets.token_hex(32)

    checksum = hashlib.sha256(raw_token.encode()).hexdigest()[:8]
    opaque_token = f"{raw_token}.{checksum}"

    return opaque_token


def verify_token_checksum(token: str) -> bool:
    if len(token) != 73: # Token must be 73 chars long
        return False

    raw_token = token[:-9] # Obtain raw token, minus the seperator
    checksum = token[-8:] # Obtain checksum

    expected_checksum = hashlib.sha256(raw_token.encode()).hexdigest()[:8]

    return expected_checksum == checksum
