# FastAPI app that provides JWKS and JWT

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from contextlib import asynccontextmanager
from .keys import generate_key_pair, get_unexpired_keys, get_expired_key
from .jwk_utils import public_key_to_jwk
from .settings import ALGORITHM, ISSUER
from .settings import EXPIRED_KEY_LIFETIME_SECONDS
from .settings import DEFAULT_KEY_LIFETIME_SECONDS
from cryptography.hazmat.primitives import serialization
import jwt
import time

# Create FastAPI app
app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs when the server starts and stops
    Generates one active key and one expired key for testing
    """
    generate_key_pair()  # Generate active key
    generate_key_pair(EXPIRED_KEY_LIFETIME_SECONDS)  # Expired key
    yield  # Shutdown code would go here if needed


# Starts the app with lifespan (^^^generates keys on startup^^^)
app = FastAPI(lifespan=lifespan)


# JWKS endpoint
@app.get("/.well-known/jwks.json")
async def jwks_endpoint():
    """
    JWKS endpoint that returns public keys in JWK format
    """
    unexpired_keys = get_unexpired_keys()  # Get all unexpired keys

    # Convert each public key to JWK format
    jwks = {
        "keys": [public_key_to_jwk(key["public"], key["kid"]) for key in unexpired_keys]
    }
    return JSONResponse(content=jwks, status_code=200)


# Auth endpoint
@app.post("/auth")
async def auth_endpoint(request: Request):
    """
    Auth endpoint that returns a signed JWT
    """
    query_params = request.query_params
    use_expired = "expired" in query_params  # Use expired key?

    # Choose key (expired or unexpired)
    if use_expired:
        key_info = get_expired_key()
        if not key_info:
            return JSONResponse(
                content={"error": "No expired key exists"}, status_code=500
            )
        expiry = key_info["expiry"]
    else:
        unexpired_keys = get_unexpired_keys()
        if not unexpired_keys:
            return JSONResponse(
                content={"error": "No unexpired key exists"}, status_code=500
            )
        key_info = unexpired_keys[0]
        expiry = int(time.time()) + DEFAULT_KEY_LIFETIME_SECONDS

    # Generate payload for JWT
    payload = {
        "sub": "notta-raelporsohn",  # Fake user ID
        "iss": ISSUER,  # Issuer string (from settings)
        "exp": expiry,  # Expiration time
        "iat": int(time.time()),  # Issuing time
    }
    headers = {"kid": key_info["kid"]}  # Add key ID to header

    # Convert private key to PEM format for PyJWT (if PyJWT needs bytes)
    private_pem = key_info["private"].private_bytes(
        encoding=serialization.Encoding.PEM,  # PEM encoding method
        format=serialization.PrivateFormat.PKCS8,  # PKCS8 format
        encryption_algorithm=serialization.NoEncryption(),  # No encryption
    )

    # Add JWT signature using the private key
    token = jwt.encode(
        payload, key_info["private"], algorithm=ALGORITHM, headers=headers
    )

    # Return JWT as plaintext
    return Response(content=token, media_type="text/plain")
