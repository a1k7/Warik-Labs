from app.security import generate_approval_token, hash_approval_token, verify_approval_token


def test_approval_token_is_not_stored_as_plaintext() -> None:
    token = generate_approval_token()
    digest = hash_approval_token(token)

    assert token
    assert digest != token
    assert len(digest) == 64
    assert verify_approval_token(token, digest)
    assert not verify_approval_token("different-token", digest)
