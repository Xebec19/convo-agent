from services.auth_service import createHash, verifyHash


def test_password_hash():
    """
    test_password_hash tests password hashing
    and verification methods
    """

    passwd = "secret-password"

    hash = createHash(password=passwd)

    assert verifyHash(password=passwd, hash=hash) == True
