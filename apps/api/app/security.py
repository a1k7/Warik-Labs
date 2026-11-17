"""Small security helpers; secrets must never be logged or sent to the model."""

import hashlib
import hmac
import secrets


def generate_approval_token() -> str:
    """Generate a URL-safe, one-time approval token."""
    return secrets.token_urlsafe(32)


def hash_approval_token(token: str) -> str:
    """Hash an approval token before storing it in the database."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_approval_token(token: str, expected_hash: str) -> bool:
    """Compare a token to its stored digest in constant time."""
    actual_hash = hash_approval_token(token)
    return hmac.compare_digest(actual_hash, expected_hash)
