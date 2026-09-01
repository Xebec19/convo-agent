from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def createHash(password) -> str:
    return password_hash.hash(password=password)


def verifyHash(password, hash) -> bool:
    return password_hash.verify(password=password, hash=hash)
