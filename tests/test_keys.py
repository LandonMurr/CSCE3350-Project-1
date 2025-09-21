import time
from app.keys import generate_key_pair, get_unexpired_keys, get_expired_key
from app.settings import DEFAULT_KEY_LIFETIME_SECONDS, EXPIRED_KEY_LIFETIME_SECONDS


def test_generate_key_pair():
    """
    Tests the generate_key_pair function under normal conditions
    """
    key = generate_key_pair()  # Make key pair
    assert "kid" in key  # Check that key ID exists
    assert "expiry" in key  # Check that expiry time exists
    assert key["expiry"] > int(time.time())  # Check that expiry time is valid
    assert "private" in key  # Check that private key exists
    assert "public" in key  # Check that public key exists


def test_generate_expired_key_pair():
    """
    Tests the generate_expired_key_pair function with expired key
    """
    key = generate_key_pair(EXPIRED_KEY_LIFETIME_SECONDS)  # Make key pair
    assert key["expiry"] < int(time.time())  # Confirm that expiry time has passed


def test_get_unexpired_keys():
    """
    Tests the get_unexpired_keys function
    """
    generate_key_pair()  # Make unexpired key pair
    generate_key_pair(EXPIRED_KEY_LIFETIME_SECONDS)  # Make expired key pair
    unexpired = get_unexpired_keys()  # Get all unexpired keys
    assert len(unexpired) >= 1  # Confirm that at least one is still valid


def test_get_expired_key():
    """
    Tests the get_expired_key function
    """
    generate_key_pair(EXPIRED_KEY_LIFETIME_SECONDS)  # Make expired key pair
    expired = get_expired_key()  # Get all expired keys
    assert expired is not None  # Confirm that at least one is expired
