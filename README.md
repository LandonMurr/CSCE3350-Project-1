# Project 1: JWKS Server

## Overview
This project implements a simple FastAPI server that:

1. Generates and manages RSA key pairs (with expiry timestamps).
2. Serves public keys in JWKS format via a RESTful endpoint.
3. Issues signed JWTs via a POST endpoint.

## Project Structure

Project-1/
├─ app/
│  ├─ __init__.py       # Empty
│  ├─ jwk_utils.py      # Helpers to convert public key to JWK format
│  ├─ keys.py           # Key manager: generate, store, and query RSA keys
│  ├─ main.py           # FastAPI app that provides JWKS and JWT
│  └─ settings.py       # Config constants for the JWKS server
├─ tests/
│  ├─ test_jwk_utils.py # Tests jwk_utils.py
│  ├─ test_keys.py      # Tests keys.py
│  └─ test_main.py      # Tests main.py
├─ README.md            # Overview / Project Documentation
└─ requirements.txt     # List of required dependencies

## Setup

1. Clone the repository
`git clone https://github.com/LandonMurr/Project-1.git`

2. Create and activate a virtual environment
```bash
python 3 -m venv .venv
source .venv/bin/activate # macOS / Linux
# .venv/Scripts/activate # Windows
```

3. Install dependencies
`pip install -r requirements.txt`

## Running the Server

Start the FastAPI server:
`uvicorn main:app --reload --port 8080`

- Server will generate one active key and one expired key on startup.

## REST Endpoints

| Endpoint               | Method | Description                                              |
| :--------------------- | :----- | :------------------------------------------------------- |
| /.well-known/jwks.json | GET    | Returns all active public keys in JWK format             |
| /auth                  | POST   | Returns a signed JWT. Add ?expired to use an expired key |

## Usage

**Fetch JWKS**
`curl http://localhost:8080/.well-known/jwks.json`

**Generate JWT**
`curl -X POST "http://localhost:8080/auth`

**Generate JWT with expired key**
`curl -X POST "http://localhost:8080/auth?expired`

## Functionality

1. **Key Management (`keys.py`)**
    - Generates RSA key pairs with unique IDs and expiry timestamps.
        - Provides helper functions to fetch expired or unexpired keys.

2. **Public Key Conversion (`jwk_utils.py`)**
    - Converts RSA public key objects into JWK dictionaries.
        - Encodes modulus and exponent as URL-safe base64 without padding.

3. **FastAPI App (`main.py`)**
    - Lifecycle generates initial keys on startup.
    - JWKS endpoint shows active public keys.
    - Auth endpoint issues JWTs with selected key.

# Notes

- Keys are stored in memory only; restarting the server resets them.
- Expired keys are included for testing JWT verification failures.
- Per the instructions, this project employs no real authentication functionality, nor are there realistic countermeasures (i.e. encryption) for many potential security vulernabilities.

## References

**Official Documentation**
    - [Cryptography - RSA Key Generation](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key)
    - [Cryptography — Public Key Objects](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#key-objects)
    - [Cryptography — Key Serialization](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/#serialization-of-keys)
    - [Python uuid module](https://docs.python.org/3/library/uuid.html#uuid.uuid4)
    - [Python time module](https://docs.python.org/3/library/time.html#time.time)
    - [Python base64 module](https://docs.python.org/3/library/base64.html#base64.urlsafe_b64encode)
    - [Python int.to_bytes](https://docs.python.org/3/library/stdtypes.html#int.to_bytes)
    - [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
    - [FastAPI Path & Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
    - [FastAPI Responses](https://fastapi.tiangolo.com/advanced/response-directly/)
    - [Python contextlib.asynccontextmanager](https://docs.python.org/3/library/contextlib.html#contextlib.asynccontextmanager)
    - [PyJWT — Encoding Tokens](https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens)
    - [Official unittest documentation](https://docs.python.org/3/library/unittest.html)
    - [Pytest documentation - assert](https://docs.pytest.org/en/stable/assert.html)
    - [Pytest documentation - monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)

**AI Assistance**
This project utilized AI assistance via Grok 4 Expert. Unfortunately, Grok has a distinct ability over other popular LLMs to maintain consideration of detailed list of requirements via its project instructions feature, which made it one of the better tools for this assignment. My goal was to complete this project in Python - a language am largely unfamiliar in - and this helped to supplement a lack of experience. AI assistance was used exclusively for the following categories:

    1. Research & Initial Project Structure

    After saving the Canvas project instructions to Grok's memory, I sent the following prompt:
    
    *"Based on instructions provided, what are some libraries I may find helpful to complete this school project in Python? Without showing me your solution, work through the project on your own, inform me of a general project structure, and procure a list of links to relevant sections of documentation within the libraries you use. My goal is to learn the process myself and write the code on my own."*

    This gave me the list of resources provided above, a basic description of project structure, and a brief description of expected functionality for each file (including the test suite).

    2. Debugging

    After running the test suite and struggling with failed tests, I uploaded my project files to the conversation, pasted the terminal output containing test status, and asked the following prompt:

    *"Help me interpret these error messages. I'm not looking for code; just provide a simple explanation of what the terminal is already saying."*

    To ensure the integrity of this practice, this prompt was used for each additional error message until no further assistance was needed.