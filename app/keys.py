# Key manager: generate, store, and query RSA keys

from cryptography.hazmat.primitives.asymmetric import rsa
from .settings import DEFAULT_KEY_LIFETIME_SECONDS, EXPIRED_KEY_LIFETIME_SECONDS
import uuid  # For generating unique IDs
import time  # For expiry timestamps

keys_store = []  # List to hold all key info


def generate_key_pair():
    """
    Generates RSA key pair with unique key ID; sets expiry timestamp

    Returns a dict with:
    - 'kid': unique key ID
    - 'expiry': when the key expires (Unix timestamp)
    - 'private': private key object
    - 'public': public key object
    """
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Common choice for RSA
        key_size=2048,  # Secure key size
    )

    # Generate public key
    public_key = private_key.public_key()

    # Generate key info
    key_info = {
        "kid": str(uuid.uuid4()),  # unique key ID
        "expiry": int(time.time())
        + DEFAULT_KEY_LIFETIME_SECONDS,  # Current time + lifetime
        "private": private_key,
        "public": public_key,
    }

    # Store key info
    keys_store.append(key_info)

    return key_info


def get_unexpired_keys():
    """
    Returns unexpired keys in a list
    """
    current_time = int(time.time())
    return [key for key in keys_store if key["expiry"] > current_time]


def get_expired_key():
    """
    Returns one key that has expired, or None if none exist
    """
    current_time = int(time.time())
    expired = [key for key in keys_store if key["expiry"] <= current_time]
    return expired[0] if expired else None
