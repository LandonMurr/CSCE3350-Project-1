from cryptography.hazmat.primitives.asymmetric import rsa
from app.jwk_utils import public_key_to_jwk


def test_public_key_to_jwk():
    """
    Tests the public_key_to_jwk function
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048
    )  # Make private key
    public_key = private_key.public_key()  # Make public key
    kid = "test-kid"  # Test key ID (insecure)
    jwk = public_key_to_jwk(public_key, kid)  # Call public_key_to_jwk
    assert jwk["kty"] == "RSA"  # Check for correct key type
    assert jwk["kid"] == kid  # Check for correct key ID
    assert "n" in jwk  # Check for correct modulus value
    assert "e" in jwk  # Check for correct exponent value
